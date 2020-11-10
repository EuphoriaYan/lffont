
import json
import tqdm
import random
import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, required=True)
    parser.add_argument('--output', type=str, required=True)
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()
    with open(args.input, 'r', encoding='utf-8') as fp:
        dataset_json = json.load(fp)
    # print(dataset_json.keys())
    fonts = list(dataset_json.keys())
    for font in fonts:
        if len(dataset_json[font]) == 0:
            dataset_json.pop(font)
    fonts = set(dataset_json.keys())

    with open('meta/train_list.txt') as fp:
        train_list = [s.strip() for s in fp if s.strip() in fonts]
    with open('meta/val_list.txt') as fp:
        val_list = [s.strip() for s in fp if s.strip() in fonts]

    assert 'FZSong' in train_list

    train_json = {k: dataset_json[k] for k in train_list}
    avail_json = dataset_json.copy()
    #  "seen_fonts", "unseen_fonts", "seen_unis", "unseen_unis"
    valid_json = {'seen_fonts': train_list, 'unseen_fonts': val_list}

    train_char_set = set()
    for font in train_list:
        if font == 'FZSong':
            continue
        for char in dataset_json[font]:
            train_char_set.add(char)
    val_char_set = set()
    for font in val_list:
        for char in dataset_json[font]:
            if char not in train_char_set:
                val_char_set.add(char)
    valid_json['seen_unis'] = list(train_char_set)
    valid_json['unseen_unis'] = list(val_char_set)
    total_json = {'train': train_json, 'avail': avail_json, 'valid': valid_json}
    with open(args.output, 'w', encoding='utf-8') as fp:
        json.dump(total_json, fp, ensure_ascii=False)
