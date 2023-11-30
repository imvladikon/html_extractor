#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path
from typing import Optional, Union

import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm

from data_extractor.data_transformers import JsonTransformer

DATA_FOLDER = Path(__file__).resolve().parent.parent / 'data'


def count_html_tables(html: str) -> int:
    soup = BeautifulSoup(html, 'html.parser')
    return len(soup.find_all('table'))


def validate_one_table_in(folder):
    more_than_one_table = []
    for file in Path(folder).glob('*.html'):
        with open(file, 'r') as f:
            html = f.read()
            if count_html_tables(html) != 1:
                more_than_one_table.append(file)
    if len(more_than_one_table) > 0:
        print(more_than_one_table)
        raise Exception('More than one table in files')


def extract_info_for(html_file: Union[str, Path]) -> dict:
    page_info = {
        "n_rows": None,
        "n_cols": None,
        "n_header_cols": None,
        "n_cells": None,
        "table_id": None,
        "has_caption": None,
        "footer_text": None,
        "n_tables": None,
        "file_id": Path(html_file).stem,
    }

    with open(html_file, 'r') as f:
        html = f.read()
        soup = BeautifulSoup(html, 'html.parser')
        page_info["n_rows"] = len(soup.select('tbody tr'))
        # expected that the columns are not empty for our data
        page_info["n_header_cols"] = len(
            [n for n in soup.select('thead th') if n.text.strip()]
        )
        page_info["n_cols"] = len(soup.select('tbody tr:first-child td'))
        page_info["n_cells"] = len(soup.select('tbody td'))

        page_info["table_id"] = soup.select_one('table').get('id')
        page_info["has_caption"] = int(len(soup.select('caption')) > 0)
        page_info["footer_text"] = soup.select_one('tfoot').text.strip()
        page_info["n_tables"] = len(soup.select('table'))

    return page_info


def exract_tables_info_from(
    folder: str, metadata_folder: Optional[str] = None
) -> pd.DataFrame:
    use_metadata = metadata_folder is not None
    tables_info = []
    files = list(Path(folder).glob('*.html'))
    for file in tqdm(files, desc='Extracting tables info', total=len(files)):
        features = extract_info_for(file)
        if use_metadata:
            metadata_file = Path(metadata_folder) / (
                Path(file).stem.replace("_table", "_metadata") + '.json'
            )
            flatten_json = JsonTransformer().transform_from(str(metadata_file))
            features.update(flatten_json)
        tables_info.append(features)
    return pd.DataFrame(tables_info)


if __name__ == '__main__':
    import argparse

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--folder', type=str, required=True)
    arg_parser.add_argument('--metadata_folder', type=str, required=False)
    arg_parser.add_argument(
        '--output', type=str, default='tables_info.csv', required=False
    )

    args = arg_parser.parse_args()
    info_df = exract_tables_info_from(args.folder, args.metadata_folder)
    info_df.to_csv(args.output, index=False)
