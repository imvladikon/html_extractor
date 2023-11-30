#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Just a draft

# import numpy as np
# from scipy.optimize import linear_sum_assignment
# from rapidfuzz import fuzz
# from sentence_transformers import SentenceTransformer, util
#
# encoder = SentenceTransformer('paraphrase-distilroberta-base-v1')
#
# synonyms = {
#     "tfoot": "footer",
#     "thead": "header",
#     "tbody": "body",
#     "tr": "row",
#     "td": "content"
# }
#
# def semantic_similarity(encoder, path1, path2):
#     # encode sentences
#     embeddings1 = encoder.encode([path1, path2])
#     cosine_scores = util.cos_sim(embeddings1[0], embeddings1[1])
#     return cosine_scores.item()
#
# def pairwise_comparison(path1, path2):
#     # replace synonyms
#     for key, value in synonyms.items():
#         path1 = path1.replace(key, value)
#         path2 = path2.replace(key, value)
#
#     blend_weight = 0.2
#     semantic_score = semantic_similarity(encoder, path1, path2)
#     score = blend_weight * semantic_score + (1 - blend_weight) * fuzz.ratio(path1, path2) / 100
#     return score
#
#
# class AbstractSchemaMatcher:
#     pass
#
#
# class BipartiteSchemaMatcher(AbstractSchemaMatcher):
#
#     def compare(self, schema1, schema2, threshold=0.8):
#         """
#         Compare two schemas
#         :param schema1:
#         :param schema2:
#         :return:
#         """
#         schema1_by_index = {i: key for i, key in enumerate(schema1)}
#         schema2_by_index = {i: key for i, key in enumerate(schema2)}
#         # create bipartite graph
#         sim_matrix = np.zeros((len(schema1), len(schema2)))
#         for i, key1 in enumerate(schema1):
#             for j, key2 in enumerate(schema2):
#                 score = pairwise_comparison(key1, key2)
#                 if score > 0.5:
#                     sim_matrix[i, j] = score
#         # solve assignment problem
#         row_ind, col_ind = linear_sum_assignment(-sim_matrix)
#         # return result
#         return {
#             schema1_by_index[i]: schema2_by_index[j]
#             for i, j in zip(row_ind, col_ind)
#             # if sim_matrix[i, j] > threshold
#         }
#
# if __name__ == '__main__':
#     html_schema = {
#         "table.id.0": {},
#         "table.caption.0": {},
#         "table.thead.tr.th.1": {},
#         "table.thead.tr.th.2": {},
#         "table.thead.tr.th.3": {},
#         "table.thead.tr.th.4": {},
#         "table.thead.tr.th.5": {},
#         "table.thead.tr.th.6": {},
#         "table.thead.tr.th.7": {},
#         "table.tbody.tr.td.0": {},
#         "table.tbody.tr.td.1": {},
#         "table.tbody.tr.td.2": {},
#         "table.tbody.tr.td.3": {},
#         "table.tbody.tr.td.4": {},
#         "table.tbody.tr.td.5": {},
#         "table.tbody.tr.td.6": {},
#         "table.tbody.tr.td.7": {},
#         "table.tfoot.tr.td.0": {}
#     }
#     json_schema = {
#         "body.content.0": {},
#         "body.content.1": {},
#         "body.content.2": {},
#         "body.content.3": {},
#         "body.content.4": {},
#         "body.content.5": {},
#         "body.content.6": {},
#         "body.headers.col.0": {},
#         "body.headers.row.0": {},
#         "body.headers.row.1": {},
#         "body.headers.row.2": {},
#         "body.headers.row.3": {},
#         "body.headers.row.4": {},
#         "body.headers.row.5": {},
#         "body.headers.row.6": {},
#         "footer.table_creation_date": {},
#         "footer.text": {},
#         "header.table_id": {},
#         "header.text": {}
#     }
#
#     matcher = BipartiteSchemaMatcher()
#     print(matcher.compare(html_schema, json_schema))
