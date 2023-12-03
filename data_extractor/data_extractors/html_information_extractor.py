#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path
from typing import Any, List

import torch
from span_marker import SpanMarkerModel

from data_extractor.data_extractors.abstract_extractor import AbstractExtractor
from data_extractor.data_preparations.html_page import HtmlPageExtended

MODELS_FOLDER = Path(__file__).parent.parent / "models"

SINGLETON_EXTRACTOR_MODELS_FACTORIES = {
    "html_extractor_small": lambda: SpanMarkerModel.from_pretrained(
        MODELS_FOLDER / "html_extractor_small"),
    "attribute_extractor_small": lambda: SpanMarkerModel.from_pretrained(
        MODELS_FOLDER / "attribute_extractor_small"),
}

MODELS = {
}


class HtmlInformationExtractor(AbstractExtractor):
    def __init__(
            self,
            model_name_or_path: str = "html_extractor_small",
            attribute_model_name_or_path: str = "attribute_extractor_small",
            device: str = "cpu",
            **kwargs,
    ) -> None:
        if model_name_or_path not in MODELS:
            MODELS[model_name_or_path] = SINGLETON_EXTRACTOR_MODELS_FACTORIES[
                model_name_or_path]()
        if attribute_model_name_or_path not in MODELS:
            MODELS[attribute_model_name_or_path] = SINGLETON_EXTRACTOR_MODELS_FACTORIES[
                attribute_model_name_or_path]()

        self.ner_model = MODELS[model_name_or_path]
        if device == "cuda" and torch.cuda.is_available():
            self.ner_model = self.ner_model.cuda()

        self.attribute_model = MODELS[attribute_model_name_or_path]
        if device == "cuda" and torch.cuda.is_available():
            self.attribute_model = self.attribute_model.cuda()

    def _featurize(self, html_string: str, **kwargs) -> List:
        page = HtmlPageExtended(html_string)
        features_list = []
        for node, features in page.flattenize():
            features.pop("span", None)
            features.pop("label", None)
            path = ".".join(features.pop("path", []))
            text = str(node)
            features_text = ' '.join(f'[{k.upper()}] {v}' for k, v in features.items())
            features_text = f"{text} [SEP] {features_text}"
            features_list.append(
                {"html": str(node), "path": path, "features_text": features_text}
            )
        return features_list

    def __call__(self, *args, **kwargs) -> Any:
        return self._extract(*args, **kwargs)

    def _extract(self, html_string: str, threshold: float = 0.5, **kwargs) -> List:
        ret = []
        features_list = list(self._featurize(html_string))
        all_offsets = self.ner_model.predict([features["features_text"].title() for features in features_list])
        for features, offsets in zip(features_list, all_offsets):
            if not offsets: continue
            offsets = sorted(offsets, key=lambda x: x["score"], reverse=True)[:1]
            for offset in offsets:
                if offset["score"] < threshold:
                    continue
                if offset["label"] == "header.table_id":
                    continue
                elif offset["label"] in ["header.text", "footer.text"]:
                    attr_offsets = self.attribute_model.predict(offset["span"])
                    attr_offsets = sorted(attr_offsets, key=lambda x: x["score"], reverse=True)[:1]
                    if attr_offsets:
                        for attr_offset in attr_offsets:
                            if attr_offset["score"] < threshold:
                                continue
                            # I made a mistake in the label name, small ad-hoc fix
                            if attr_offset["label"] == "header.table_creation_date":
                                attr_offset["label"] = "footer.table_creation_date:"
                            ret.append(
                                {
                                    "key": attr_offset["label"],
                                    "score": attr_offset["score"],
                                    "value": attr_offset["span"],
                                    # "html": features["html"],
                                }
                            )
                ret.append(
                    {
                        "key": offset["label"],
                        "score": offset["score"],
                        "value": features["features_text"][offset["char_start_index"]:offset["char_end_index"]],
                        # "html": features["html"],
                    }
                )
        return ret


if __name__ == '__main__':
    from pprint import pprint

    file = "../../data/tables/10020_table.html"
    html_string = open(file, "r").read()

    extractor = HtmlInformationExtractor()
    pprint(extractor(html_string))
#    [{'html': '<caption>Table 12.3.94.68.40.22 Biochemist, clinical</caption>',
#  'key': 'header.text',
#  'score': 0.7144958972930908,
#  'value': 'Table 12.3.94.68.40.22 Biochemist, clinical'},
# {'html': '<table id=Table12394684022Biochemistclinical>',
#  'key': 'header.table_id',
#  'score': 0.9376177191734314,
#  'value': 'Table12394684022Biochemistclinical'},
# {'html': '<th> Bradley Scott </th>',
#  'key': 'body.headers.row',
#  'score': 0.996218740940094,
#  'value': 'Bradley Scott'},
# {'html': '<td align="right"> Moore PLC </td>',
#  'key': 'body.headers.col',
#  'score': 0.9695820808410645,
#  'value': 'Moore PLC'},
# {'html': '<td align="left" style="font-weight:bold; font-style:italic"> 53 '
#          '</td>',
#  'key': 'body.content',
#  'score': 0.9908156394958496,
#  'value': '53'},
# {'html': '<tr><td>Creation: 29Aug2008 Tanzania</td></tr>',
#  'key': 'footer.text',
#  'score': 0.9483703374862671,
#  'value': 'Creation: 29Aug2008 Tanzania'}]
