
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
    # ['font_name', 'font_pth', 'missing', 'fake']
    dst_json = dict()
    s = '您今天吃了吗为打分卡哭了染发大杀四方抢位置婆牛网'
    for font_json in font_missing_json:
        font_json_new = dict()
        font_json_new['path'] = font_json['font_pth']
        font_json_new['charlist'] = list(s)
        dst_json[font_json['font_name']] = font_json_new
    with open(args.dst_json, 'w', encoding='utf-8') as fp:
        json.dump(dst_json, fp)
