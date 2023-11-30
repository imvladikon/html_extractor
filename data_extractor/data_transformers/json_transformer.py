#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
from typing import Dict, Any

from data_extractor.data_transformers.abstract_transformer import AbstractTransformer


class JsonTransformer(AbstractTransformer):
    """
    Transform json to flatten dict
    e.g. {"body": {"content": 1}} -> {"body.content": 1}
    """

    def _transform(self, json_dict, **kwargs) -> Dict[str, Any]:
        def _iter_nodes(node, path=None):
            if path is None:
                path = []
            if isinstance(node, dict):
                for key, value in node.items():
                    if isinstance(value, dict):
                        yield from _iter_nodes(value, path + [key])
                    elif isinstance(value, list):
                        for i, subnode in enumerate(value):
                            yield from _iter_nodes(subnode, path + [key])
                    else:
                        yield value, path + [key]
            elif isinstance(node, list):
                for i, subnode in enumerate(node):
                    yield from _iter_nodes(subnode, path + [i])
            else:
                yield node, path

        seen_paths = {}
        for node, path in _iter_nodes(json_dict):
            whole_path = '.'.join(map(str, path))
            seen_paths.setdefault(whole_path, []).append(node)
        return seen_paths

    def transform_from(self, file, **kwargs) -> Dict[str, Any]:
        with open(file, 'r') as f:
            json_dict = json.load(f)
        return self._transform(json_dict, **kwargs)
