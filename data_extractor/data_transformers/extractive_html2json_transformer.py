#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from data_extractor.data_schemes import TableSchema
from data_extractor.data_extractors import HtmlInformationExtractor
from data_extractor.data_transformers.abstract_transformer import AbstractTransformer


class ExtractiveHtml2JsonTransformer(AbstractTransformer):
    def __init__(self, extractor_kwargs: dict = {}, **kwargs):
        self.extractor = HtmlInformationExtractor(**extractor_kwargs)

    def _transform(self, html_string: str, **kwargs) -> dict:
        offsets = self.extractor(html_string)
        flatten_dict = {}
        for offsets_dict in offsets:
            key = offsets_dict["key"]
            value = offsets_dict["value"]
            if key not in flatten_dict:
                default_type = TableSchema.get_default_type(key)
                if default_type == list:
                    flatten_dict[key] = [value]
                else:
                    flatten_dict[key] = value
            else:
                if isinstance(flatten_dict[key], list):
                    flatten_dict[key].append(value)
                else:
                    flatten_dict[key] = [flatten_dict[key], value]
        return TableSchema.from_flatten_dict(**flatten_dict).to_dict()
