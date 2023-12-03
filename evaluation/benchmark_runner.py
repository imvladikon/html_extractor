#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import timeit
from pathlib import Path
from typing import Union

import numpy as np
import pandas as pd
from tqdm import tqdm

from data_extractor.data_transformers import (RuleBasedHtml2JsonTransformer,
                                              ExtractiveHtml2JsonTransformer)
from data_extractor.data_transformers.abstract_transformer import AbstractTransformer

DATA_FOLDER = Path(__file__).parent.parent / "data"
METADATA_FOLDER = DATA_FOLDER / "metadata"
HTML_FOLDER = DATA_FOLDER / "tables"


class CasesCatcher:
    """
    helper class to catch cases of FP and FN
    """

    def __init__(self):
        self.cases = {
            "FP": [],
            "FN": [],
        }

    def __call__(self, y_pred, y_golden, key):
        self.cases[key].append((y_pred, y_golden))


class TransformerFactory:

    @classmethod
    def create(cls, string_factory, device="cpu", **kwargs):
        if string_factory == "rule":
            return RuleBasedHtml2JsonTransformer(**kwargs)
        elif string_factory == "extractive":
            return ExtractiveHtml2JsonTransformer(device=device, **kwargs)
        else:
            raise ValueError("Unknown transformer type")


class BenchmarkRunner:

    def __init__(self, table_folder, metadata_folder, **kwargs):
        self.report = None
        self.table_folder = table_folder
        self.metadata_folder = metadata_folder
        # report metrics and aggregation functions, -> in future possible to separate it to specific classes as it's done by torchmetrics
        self.report_metrics = {'TP': sum, 'FP': sum, 'FN': sum, 'TN': sum,
                               'precision': np.mean, 'recall': np.mean, 'f1': np.mean,
                               'accuracy': np.mean}
        self.overall_time = None
        self.ops_per_second = None
        self.device = kwargs.get("device", "cpu")

    @classmethod
    def from_path(cls, table_folder, metadata_folder, **kwargs):
        return cls(table_folder, metadata_folder, **kwargs)

    def run(self, predictor: Union[str, AbstractTransformer]):
        self.report = {}
        start_time = timeit.default_timer()

        if isinstance(predictor, str):
            predictor = TransformerFactory.create(predictor, device=self.device)

        report_data = []
        html_files = list(Path(self.table_folder).glob('*.html'))
        for file in tqdm(html_files, desc=f"Benchmarking {predictor}",
                         total=len(html_files)):
            table_id = file.stem
            metadata_file = Path(self.metadata_folder,
                                 table_id.replace("_table", "_metadata") + '.json')
            y_golden = json.load(open(metadata_file, "r"))
            y_pred = predictor(open(file).read())
            predictions = self.compare_predictions(y_pred, y_golden)
            report_data.append(predictions)
        report_data = pd.DataFrame(report_data)
        for key, agg_fn in self.report_metrics.items():
            self.report[key] = agg_fn(report_data[key])
        self.overall_time = timeit.default_timer() - start_time
        self.ops_per_second = len(html_files) / self.overall_time
        return self.report

    def compare_predictions(self, predictions, ground_truth):
        """
        calculate TP, FP, FN, TN, precision, recall, f1, accuracy
        for two sets: golden standard and predictions
        """
        metadata_keys = list(ground_truth.keys())

        # TODO: it seems that better just flatten dicts and compare them. since such function is already implemented in json_transformer.py
        def calc_metrics_matrix():
            TP, FP, FN, TN = 0, 0, 0, 0

            def _calc(predictions, ground_truth, keys):
                nonlocal TP, FP, FN, TN
                for key in keys:
                    if key in predictions:
                        if isinstance(predictions[key], dict):
                            _calc(predictions[key], ground_truth[key],
                                  predictions[key].keys())
                        elif isinstance(predictions[key], list):
                            gt = ground_truth[key]
                            for pred in predictions[key]:
                                if pred in gt:
                                    TP += 1
                                else:
                                    FP += 1
                            for gt in ground_truth[key]:
                                if gt not in predictions[key]:
                                    FN += 1
                        else:
                            if predictions[key] == ground_truth[key]:
                                TP += 1
                            else:
                                FP += 1
                    else:
                        FN += 1
                for key in predictions.keys():
                    if key not in keys:
                        TN += 1

            _calc(predictions, ground_truth, metadata_keys)
            return TP, FP, FN, TN

        TP, FP, FN, TN = calc_metrics_matrix()

        precision = TP / (TP + FP)
        recall = TP / (TP + FN)
        f1 = 2 * precision * recall / (precision + recall)
        accuracy = (TP + TN) / (TP + FP + FN + TN)

        return {
            'TP': TP,
            'FP': FP,
            'FN': FN,
            'TN': TN,
            'precision': precision,
            'recall': recall,
            'f1': f1,
            'accuracy': accuracy
        }


if __name__ == '__main__':
    import argparse

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--predictor", type=str, default="extractive")
    arg_parser.add_argument("--device", type=str, default=None)

    args = arg_parser.parse_args()
    device = args.device
    if device is None:
        import torch

        device = "cuda" if torch.cuda.is_available() else "cpu"

    runner = BenchmarkRunner.from_path(
        table_folder=HTML_FOLDER,
        metadata_folder=METADATA_FOLDER,
        device=device
    )
    extractive_report = runner.run(args.predictor)
    print(extractive_report)
