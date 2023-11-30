#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class AbstractExtractor:
    def __call__(self, *args, **kwargs):
        return self._extract(*args, **kwargs)

    def _extract(self, *args, **kwargs):
        raise NotImplementedError