#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from data_extractor.data_extractors.abstract_extractor import AbstractExtractor


class RuleBasedTableIdExtractor(AbstractExtractor):
    def _extract(self, string: str, **kwargs) -> str:
        "Table 62.72.88 Surveyor, mining => 62.72.88"
        string = string.replace('Table ', '', 1)
        values = string.split(' ')
        if len(values) > 1:
            return values[0]
        else:
            return ''
