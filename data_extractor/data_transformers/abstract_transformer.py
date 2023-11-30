#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Any


class AbstractTransformer:

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        pass

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        return self._transform(*args, **kwargs)

    def _transform(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError

    def convert(self, source_file: str, target_file: str, **kwargs) -> None:
        with open(source_file, 'r') as f:
            html_string = f.read()
        ret = self(html_string, **kwargs)
        with open(target_file, 'w') as f:
            f.write(ret.to_json())

    def transform_from(self, file: str, **kwargs: Any) -> Any:
        raise NotImplementedError
