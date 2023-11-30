#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
from pathlib import Path

import torch
from bs4 import BeautifulSoup, NavigableString


class HtmlPage:

    def __init__(self, html):
        self.html = html

    @classmethod
    def from_file(cls, file):
        with open(file, 'r') as f:
            return cls(f.read())

    def flattenize(self):
        """
        convert html to flatten structure
        like this:
        tr[0].td[0].a[0].text
        :return:
        """
        soup = BeautifulSoup(self.html, 'html.parser')

        def _iter_nodes(node, path=None):
            if path is None:
                path = []
            if hasattr(node, 'children'):
                for subnode in node.children:
                    if isinstance(subnode, NavigableString) and subnode == '\n':
                        continue
                    if hasattr(subnode, 'attrs') and 'id' in subnode.attrs:
                        yield subnode.attrs['id'], path + [subnode.name + '.id']
                    if hasattr(subnode, "name") and subnode.name is not None:
                        yield from _iter_nodes(subnode, path + [subnode.name])
                    else:
                        yield from _iter_nodes(subnode, path)
            else:
                yield node.strip(), path

        # assing unique order id to each node with the same path
        seen_paths = {}
        for node, path in _iter_nodes(soup):
            whole_path = '.'.join(map(str, path))
            seen_paths.setdefault(whole_path, []).append(node)

        for path, nodes in seen_paths.items():
            yield path, nodes


class HtmlPageExtended(HtmlPage):

    def flattenize(self):
        # thead, tbody, tfoot
        soup = BeautifulSoup(self.html, 'html.parser')
        # table caption
        table_caption = soup.find('table').find('caption')
        if table_caption is not None:
            table_caption_value = table_caption.text
            # find start and end position of table caption
            table_caption_start = str(table_caption).find(table_caption_value)
            table_caption_end = table_caption_start + len(table_caption_value)
            yield table_caption, {
                'path': ['table', 'caption'],
                'label': 'header.text',
                'span': [table_caption_start, table_caption_end]
            }
        # table id
        table_id = soup.find('table').attrs.get('id', None)
        if table_id is not None:
            yield f"""<table id={table_id}>""", {
                'path': ['table'],
                'label': 'header.table_id',
                'span': [len("<table id="), len(f"<table id={table_id}")]
            }
        for i, node in enumerate(soup.select('thead th')):
            node_value = node.text
            node_start = str(node).find(node_value)
            node_end = node_start + len(node_value)
            yield node, {
                'path': ['thead', 'th'],
                'column_number': i,
                'label': "" if i == 0 else "body.headers.row",
                'span': [node_start, node_end]
            }

        for i, node in enumerate(soup.select('tbody tr')):
            for j, td in enumerate(node.select('td')):
                node_value = td.text
                node_start = str(td).find(node_value)
                node_end = node_start + len(node_value)
                yield td, {
                    'path': ['tbody', 'tr', 'td'],
                    'row_number': i,
                    'column_number': j,
                    'label': "body.headers.col" if j == 0 else "body.content",
                    'span': [node_start, node_end]
                }

        for i, node in enumerate(soup.select('tfoot tr')):
            node_value = node.text
            node_start = str(node).find(node_value)
            node_end = node_start + len(node_value)
            yield node, {
                'path': ['tfoot', 'tr'],
                'row_number': i,
                'label': "footer.text",
                'span': [node_start, node_end]
            }


if __name__ == '__main__':
    from transformers import BertTokenizer, BertForTokenClassification

    labels = [
        'body.content',
        'body.headers.col',
        'body.headers.row',
        'footer.table_creation_date',
        'footer.text',
        'header.table_id',
        'header.text'
    ]
    label2id = {label: i for i, label in enumerate(labels)}
    id2label = {i: label for i, label in enumerate(labels)}

    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    model = BertForTokenClassification.from_pretrained('bert-base-uncased', num_labels=len(labels))
    model.config.id2label = id2label
    model.config.label2id = label2id

    text = """<td align="left" style="font-style:italic">    1459    </td>"""
    # encode addtional information with [PROP] VALUE  and add it to the text
    features = {'path': 'tbody.tr.td', 'row': 3, 'column': 3}
    features_text = ' '.join([f'[{k.upper()}] {v}' for k, v in features.items()])
    text = text + ' [SEP] ' + features_text + ' [SEP]'

    tokens = tokenizer.tokenize(text)
    # tokens = ['[CLS]'] + tokens + ['[SEP]'] + tokenizer.tokenize(features_text) + ['[SEP]']
    token_ids = tokenizer.convert_tokens_to_ids(tokens)
    token_ids = torch.tensor([token_ids])
    outputs = model(token_ids)






    from spacy.training import offsets_to_biluo_tags
    from spacy.lang.en import English

    nlp = English()
    # nlp = spacy.blank("en")
    # nlp.tokenizer = create_html_tokenizer()(nlp)

    with open("/media/robert/BC7CA8E37CA899A2/dev/tasks/dataset/generated_tables/ner_dataset.jsonl", "w") as f:
        for file in Path("/media/robert/BC7CA8E37CA899A2/dev/tasks/dataset/generated_tables/tables/").glob("*.html"):
            page = HtmlPageExtended.from_file(file)
            for node, path in page.flattenize():
                offsets = [[*path.pop("span"), path.pop("label")]]
                text = str(node)

                features = path
                features_text = ' '.join([f'[{k.upper()}] {v}' for k, v in features.items()])
                text = text + ' [SEP] ' + features_text + ' [SEP]'

                all_tags = []
                all_tokens = []
                current_pos = 0
                for start, end, label in offsets:
                    if (current_pos == 0 or start > current_pos) and text[
                                                                     current_pos:start].strip():
                        doc = nlp.tokenizer(text[current_pos:start].strip())
                        tags = offsets_to_biluo_tags(doc, [])
                        all_tags.extend(tags)
                        all_tokens.extend([token.text for token in doc])

                    doc = nlp.tokenizer(text[start:end].strip())
                    tags = offsets_to_biluo_tags(doc, [(0, len(text[start:end].strip()), label)])
                    all_tags.extend(tags)
                    all_tokens.extend([token.text for token in doc])
                    current_pos = end

                if current_pos < len(text):
                    doc = nlp.tokenizer(text[current_pos:])
                    tags = offsets_to_biluo_tags(doc, [])
                    all_tags.extend(tags)
                    all_tokens.extend([token.text for token in doc])

                tokens = []
                raw_tags = []
                for token, tag in zip(all_tokens, all_tags):
                    tokens.append(token)
                    raw_tags.append(tag)

                tags = {
                    "doc_id": file.stem,
                    "tokens": tokens,
                    "raw_tags": raw_tags,
                    "ner_tags": raw_tags,
                }
                f.write(json.dumps(tags) + "\n")

