#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re

import dateparser

from data_extractor.data_extractors.abstract_extractor import AbstractExtractor

DATE_PATTERNS = [
    re.compile("\d{1,2}[A-Za-z]{3}\d{4}")
]


class RuleBasedDateExtractor(AbstractExtractor):
    def _extract(self, text):
        span_text = text.replace('Creation:', '').strip()
        for pattern in DATE_PATTERNS:
            for match in pattern.finditer(span_text):
                start, end = match.span()
                return span_text[start:end]

        dt = dateparser.parse(text)
        if dt is None:
            is_detected = False
            for i in range(1, len(span_text.split())):
                span_text = ' '.join(span_text.split()[:-i])
                dt = dateparser.parse(span_text)
                if dt is not None:
                    return span_text
            # if not is_detected:
            #     logger.warning(f'Cannot parse date: {text}')
        else:
            return span_text


if __name__ == '__main__':
    # cases that were caught by FP catcher in benchmark
    print(RuleBasedDateExtractor()('Creation: 2019-01-01'))
    print(RuleBasedDateExtractor()('Creation: 29Mar2009 Russian Federation'))
    print(RuleBasedDateExtractor()('Creation: 30Apr2009 Sri Lanka'))
    print(RuleBasedDateExtractor()('Creation: 5Jun2010 Holy See (Vatican City State)'))
