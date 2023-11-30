#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from dataclasses import dataclass
from typing import Optional, Dict
import json

from data_extractor.utils import flatten_setattr

FLATTEN_TYPES_DEFINITIONS: Dict = {
    'body.content': list,
    'body.headers.col': list,
    'body.headers.row': list,
    'footer.text': str,
    'header.table_id': str,
    'header.text': str
}


class DictMixin:
    def to_dict(self):
        return {
            k: v.to_dict() if hasattr(v, 'to_dict') else v
            for k, v in self.__dict__.items()
            if v is not None
        }

    def to_json(self, **kwargs):
        return json.dumps(self.to_dict(), **kwargs)


@dataclass
class TableBodyHeader(DictMixin):
    col: Optional[list] = None
    row: Optional[list] = None


@dataclass
class TableBody(DictMixin):
    headers: Optional[TableBodyHeader] = None
    content: Optional[list] = None


@dataclass
class TableFooter(DictMixin):
    table_creation_date: Optional[str] = None
    text: Optional[str] = None


@dataclass
class TableHeader(DictMixin):
    table_id: Optional[str] = None
    text: Optional[str] = None


@dataclass
class TableSchema(DictMixin):
    body: Optional[TableBody] = None
    header: Optional[TableHeader] = None
    footer: Optional[TableFooter] = None

    def flatten_dict(self):
        ret = {}
        for k, v in self.to_dict().items():
            if isinstance(v, dict):
                for k2, v2 in v.items():
                    if isinstance(v2, dict):
                        for k3, v3 in v2.items():
                            ret[f"{k}.{k2}.{k3}"] = v3
                    else:
                        ret[f"{k}.{k2}"] = v2
            else:
                ret[k] = v
        return ret

    @staticmethod
    def get_default_type(key):
        return FLATTEN_TYPES_DEFINITIONS.get(key, str)

    @classmethod
    def from_flatten_dict(cls, **kwargs):
        body = TableBody(
            headers=TableBodyHeader(),
            content=None
        )
        header = TableHeader()
        footer = TableFooter()
        self = cls(body=body, header=header, footer=footer)
        for k, v in kwargs.items():
            flatten_setattr(self, k, v)
        return self
