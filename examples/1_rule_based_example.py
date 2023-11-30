#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
from pathlib import Path

from data_extractor.data_transformers import RuleBasedHtml2JsonTransformer

DATA_FOLDER = Path(__file__).parent.parent / "data"
METADATA_FOLDER = DATA_FOLDER / "metadata"
HTML_FOLDER = DATA_FOLDER / "tables"


def recursive_sort_dict(d):
    if isinstance(d, dict):
        return {k: recursive_sort_dict(d[k]) for k in sorted(d.keys())}
    elif isinstance(d, list):
        return [recursive_sort_dict(x) for x in d]
    else:
        return d


if __name__ == '__main__':
    file = HTML_FOLDER / "10020_table.html"
    meta_file = METADATA_FOLDER / "10020_metadata.json"
    html_string = open(file, "r").read()

    extractor = RuleBasedHtml2JsonTransformer()
    print("Extracted information:")
    json_dict = extractor(html_string)
    json_dict = recursive_sort_dict(json_dict)
    print(json_dict)
    print("Expected information:")
    json_dict_expected = json.loads(open(meta_file, "r").read())
    json_dict_expected = recursive_sort_dict(json_dict_expected)
    print(json_dict_expected)
