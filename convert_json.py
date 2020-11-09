
import json
import argparse
from pprint import pprint


if __name__ == '__main__':
    parse = argparse.ArgumentParser()
    parse.add_argument('--src_json', type=str, required=True)
    parse.add_argument('--dst_json', type=str, required=True)
    args = parse.parse_args()
    with open(args.src_json, 'r', encoding='utf-8') as fp:
        font_missing_json = json.load(fp)
    dst_json = dict()
    pprint(font_missing_json[0].keys())