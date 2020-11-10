
import json
import argparse
from pprint import pprint
from fontTools.ttLib import TTFont
import random
from tqdm import tqdm


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
    parser = argparse.ArgumentParser()
    parser.add_argument('--src_json', type=str, required=True)
    parser.add_argument('--dst_json', type=str, required=True)
    args = parser.parse_args()

    with open(args.src_json, 'r', encoding='utf-8') as fp:
        font_missing_json = json.load(fp)
    # ['font_name', 'font_pth', 'missing', 'fake']
    dst_json = dict()
    font_names = [f['font_name'] for f in font_missing_json]
    random.shuffle(font_names)
    train_font = set(font_names[20:])
    val_font = set(font_names[:20])

    val_chars = '鑫燚丝绸摩羯钨棒网抑云音乐'
    val_chars_set = set(list(val_chars))
    for font_json in tqdm(font_missing_json):
        font_json_new = dict()
        font_name = font_json['font_name']
        font_path = font_json['font_pth']
        font_json_new['path'] = font_path
        if font_name in val_font:
            font_json_new['charlist'] = list(val_chars)
        else:
            ttfont = TTFont(font_path)
            font_list = list(processGlyphNames(ttfont.getGlyphNames()))
            random.shuffle(font_list)
            sample_cnt = min(200, len(font_list))
            charlist = []
            i = 0
            for i in range(sample_cnt):
                if font_list[i] not in val_chars_set:
                    charlist.append(font_list[i])
            font_json_new['charlist'] = charlist
        dst_json[font_name] = font_json_new
    content_font_path = 'content_font/FZSONG_ZhongHuaSongPlane00_2020051520200519101119.TTF'
    fzsong_ttfont = TTFont(content_font_path)
    dst_json['FZSong'] = {'path': content_font_path, 'charlist': list(processGlyphNames(fzsong_ttfont.getGlyphNames()))}
    with open(args.dst_json, 'w', encoding='utf-8') as fp:
        json.dump(dst_json, fp, ensure_ascii=False)
    with open('meta/train_list.txt', 'w', encoding='utf-8') as fp:
        for font in train_font:
            fp.write(font + '\n')
    with open('meta/val_list.txt', 'w', encoding='utf-8') as fp:
        for font in val_font:
            fp.write(font + '\n')

