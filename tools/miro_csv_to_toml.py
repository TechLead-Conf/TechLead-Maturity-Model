#!/usr/bin/env python3

import os
import sys
from collections import OrderedDict
import unicodedata
import re
import csv
import os.path as path


CSV_LEVELS_COL = 1
CSV_SKILLS_COLS_FROM = 2
MAX_FILE_NAME_LEN = 32


def slugify(value):
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    """
    value = str(value)
    value = unicodedata.normalize('NFKC', value)
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '_', value).strip('-_')


def write_skill(skill, skills_dir):
    skill = skill.strip()
    skill_parts = skill.split(',')

    slug = slugify(skill_parts[0][:MAX_FILE_NAME_LEN])
    file_name = slug + '.toml'
    if 'http' in skill_parts[-1]:
        display_name = ', '.join(skill_parts[:-1])
        link = skill_parts[-1].strip()
    else:
        display_name = skill
        link = None

    with open(path.join(skills_dir, file_name), 'w') as f:
        f.write('[display_name]\n')
        f.write(f'ru = "{display_name}"\n')

        if link:
            f.write('\n[links]\n')
            f.write(f'ru = "{link}"\n')

    return slug


def write_category(category, levels, categories_dir):
    slug = slugify(category[:MAX_FILE_NAME_LEN]) + '.toml'

    with open(path.join(categories_dir, slug), 'w') as f:
        f.write('[display_name]\n')
        f.write(f'ru = "{category}"\n')

        for level, skills in levels.items():
            level_name = slugify(level[:MAX_FILE_NAME_LEN])
            f.write(f'\n[levels.{level_name}]\n')
            f.write('skills = [\n')

            for skill in skills:
                f.write(f'    "{skill}",\n')

            f.write(']\n')

    return slug


def write_level(level, levels_dir):
    slug = slugify(level[:MAX_FILE_NAME_LEN]) + '.toml'

    with open(path.join(levels_dir, slug), 'w') as f:
        f.write('[display_name]\n')
        f.write(f'ru = "{level}"\n')


def write_matrix(categories, matrix_dir):
    with open(path.join(matrix_dir,'matrix.toml'), 'w') as f:
        f.write('[display_name]\n')
        f.write('ru = "Матрица зрелости"\n')

        f.write('\ncategories = [\n')
        for category in categories.keys():
            category_name = slugify(category[:MAX_FILE_NAME_LEN])
            f.write(f'    "{category_name}",\n')

        f.write(']\n')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Please specify directory to write output')
        sys.exit(1)

    output_dir = sys.argv[1]

    if not path.isdir(output_dir):
        print('Path specified is not a directory')
        sys.exit(1)

    if len(os.listdir(output_dir)) != 0:
        print('Directory specified is not empty')
        sys.exit(1)

    skills_dir = path.join(output_dir, 'skills')
    levels_dir = path.join(output_dir, 'levels')
    categories_dir = path.join(output_dir, 'categories')
    for d in [skills_dir, levels_dir, categories_dir]:
        os.makedirs(d)

    # {category1: {level1: [skill1, skill2]}}
    categories = OrderedDict()

    sys.stdin.readline() # ignore board name
    reader = csv.DictReader(sys.stdin, delimiter=',', strict=True)

    for row_n, row in enumerate(reader):
        if row_n == 0:
            for category_col in list(row.keys())[CSV_SKILLS_COLS_FROM:]:
                categories[category_col] = OrderedDict() # dict of levels

        level = row[list(row.keys())[CSV_LEVELS_COL]]

        for category in list(categories.keys()):
            if not row[category]:
                continue

            for skill in row[category].splitlines():
                file_name = write_skill(skill, skills_dir)

                if level not in categories[category]:
                    categories[category][level] = []

                categories[category][level].append(file_name)

    for category, levels in categories.items():
        write_category(category, levels, categories_dir)

    unique_levels = set()
    for levels in categories.values():
        for level in levels.keys():
            unique_levels.add(level)

    for level in unique_levels:
        write_level(level, levels_dir)

    write_matrix(categories, output_dir) 