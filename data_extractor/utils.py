#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Any, Dict

import functools


def flatten_setattr(obj: Any, attr: str, val: Any) -> None:
    pre, _, post = attr.rpartition('.')
    return setattr(flatten_getattr(obj, pre) if pre else obj, post, val)


def flatten_getattr(obj: Any, attr: str, *args: Any) -> Any:
    def _getattr(obj, attr):
        return getattr(obj, attr, *args)

    return functools.reduce(_getattr, [obj] + attr.split('.'))


def flatten_hasattr(obj: Any, attr: str) -> bool:
    if hasattr(obj, attr):
        return True
    try:
        flatten_getattr(obj, attr)
    except AttributeError:
        return False
    else:
        return True


def nupdateattrs(obj: Any, properties: Dict) -> None:
    for k, v in properties.items():
        if flatten_hasattr(obj, k):
            flatten_setattr(obj, k, v)


def load_examples():
    import os, json

    current_dir = os.path.dirname(os.path.abspath(__file__))
    examples_dir = os.path.join(current_dir, "assets")
    html_string = open(os.path.join(examples_dir, "example_table.html")).read()
    metadata = json.load(open(os.path.join(examples_dir, "example_metadata.json")))
    return {
        "html": html_string,
        "metadata": metadata,
    }
