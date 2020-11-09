
import json
import argparse
from pprint import pprint
from fontTools.ttLib import TTFont
import random


def processGlyphNames(GlyphNames):
    res = set()
    for char in GlyphNames:
        if char.startswith('uni'):
            char = char[3:]
        elif char.startswith('u'):
            char = char[1:]
        else:
            continue
        if char:
            try:
                char_int = int(char, base=16)
            except ValueError:
                continue
            try:
                char = chr(char_int)
            except ValueError:
                continue
            res.add(char)
    return res


if __name__ == '__main__':
    parse = argparse.ArgumentParser()
    parse.add_argument('--src_json', type=str, required=True)
    parse.add_argument('--dst_json', type=str, required=True)
    args = parse.parse_args()
    with open(args.src_json, 'r', encoding='utf-8') as fp:
        font_missing_json = json.load(fp)
    # ['font_name', 'font_pth', 'missing', 'fake']
    dst_json = dict()

    for font_json in font_missing_json:
        font_json_new = dict()
        font_path = font_json['font_pth']
        ttfont = TTFont(font_path)
        font_list = list(processGlyphNames(ttfont.getGlyphNames()))
        random.shuffle(font_list)
        sample_cnt = min(200, len(font_list))
        font_json_new['path'] = font_path
        font_json_new['charlist'] = font_list[:sample_cnt]
        dst_json[font_json['font_name']] = font_json_new
    with open(args.dst_json, 'w', encoding='utf-8') as fp:
        json.dump(dst_json, fp, ensure_ascii=False)
