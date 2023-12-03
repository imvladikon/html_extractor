#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from argparse import ArgumentParser

import tiktoken
from pathlib import Path
from tqdm import tqdm

PROJECT_DIR = Path(__file__).parent.parent
DATA_DIR = PROJECT_DIR / "data"

costs_usd_per_model = {
    "gpt-3.5-turbo": {
        "input": 0.0010 / 1000,
        "output": 0.0020 / 1000,
    }
}

if __name__ == '__main__':
    arg_parser = ArgumentParser()
    arg_parser.add_argument("--model", type=str, default="gpt-3.5-turbo")
    arg_parser.add_argument("--folder", type=str, required=False,
                            default=str(DATA_DIR / "tables"))
    args = arg_parser.parse_args()

    all_lengths = 0
    files = list(Path(args.folder).glob("*.html"))
    for file in tqdm(files, total=len(files)):
        doc = open(file, "r").read()
        enc = tiktoken.encoding_for_model(args.model)
        tokens = enc.encode(doc)
        all_lengths += len(tokens)

    print("Total tokens:\n", all_lengths)
    cost_per_token_usd = costs_usd_per_model[args.model]["input"] + \
                         costs_usd_per_model[args.model]["output"]
    print("Cost, USD:\n", all_lengths * cost_per_token_usd)
