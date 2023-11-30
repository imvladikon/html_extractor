#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
from typing import Optional

from bs4 import BeautifulSoup

from data_extractor.data_schemes import (
    TableSchema,
    TableHeader,
    TableFooter,
    TableBodyHeader,
    TableBody,
)
from data_extractor.data_extractors import (RuleBasedDateExtractor,
                                            RuleBasedTableIdExtractor)
from data_extractor.data_transformers.abstract_transformer import AbstractTransformer

logger = logging.getLogger(__name__)


class RuleBasedHtml2JsonTransformer(AbstractTransformer):

    def _transform(self, html_string, **kwargs) -> Optional[TableSchema]:
        soup = BeautifulSoup(html_string, 'html.parser')

        # header
        table_soup = soup.find('table')
        if table_soup is None:
            logger.info('No table found')
            return None

        # header
        caption_text = (None if table_soup.find('caption') is None else table_soup.find(
            'caption').text)
        table_header = TableHeader(
            table_id=RuleBasedTableIdExtractor()(caption_text),
            text=caption_text,
        )

        # footer
        table_footer = None
        tfoot = table_soup.find('tfoot')
        if tfoot is not None:
            footer_text = tfoot.text
            footer_table_creation_date = RuleBasedDateExtractor()(tfoot.text)
            table_footer = TableFooter(
                text=footer_text, table_creation_date=footer_table_creation_date
            )

        # body
        # parse header of table
        table_header_col = None
        table_header_row = None
        table_content = None
        if table_soup.find('thead') is not None:
            table_header_row = [
                node.text.strip() for node in table_soup.select('thead th')
            ]
            # skip first column if it is empty
            if table_header_row and table_header_row[0] == '':
                table_header_row = table_header_row[1:]
        for tr in table_soup.select('tbody tr'):
            for i, td in enumerate(tr.select('td')):
                if i == 0:
                    if table_header_col is None:
                        table_header_col = []
                    table_header_col.append(td.text.strip())
                else:
                    if table_content is None:
                        table_content = []
                    table_content.append(td.text.strip())
        table_body_header = TableBodyHeader(col=table_header_col, row=table_header_row)
        table_body = TableBody(headers=table_body_header, content=table_content)
        ret = TableSchema(header=table_header,
                          body=table_body,
                          footer=table_footer).to_dict()

        # I didn't use pydantic, or smt like that, so, there is no alias for fields
        # adhoc solution for "table_creation_date:"
        if ret['footer'] is not None:
            ret['footer']['table_creation_date:'] = ret['footer'].pop(
                'table_creation_date', None)
        return ret
