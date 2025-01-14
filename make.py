import argparse
import json
import os

languages = ['en', 'fr']
notebook_files = [
    '01-dataframe.ipynb',
]


def make_nodebook(src_path: str, new_path: str, lang: str, remove_tag: str):
    '''Update or rebuild a single notebook from the source notebook

    Arguments:
    src_path -- relative path to the source notebook file
    new_path -- relative path to the new notebook file
    lang -- language code, either "en" or "fr"
    remove_tag -- if this tag is found, remove the cell from the output

    Return value:
    The final number of cells in the saved file.
    '''

    print(f'Building {new_path} ...')

    with open(src_path, 'r') as ipynb:
        src_dict = json.load(ipynb)

    new_cells = []

    for cell in src_dict['cells']:
        cell_metadata = cell['metadata']

        # Skip cells of the other version
        if 'tags' in cell_metadata and remove_tag in cell_metadata['tags']:
            continue

        source_code = cell['source']

        # No language required for empty cells
        if not source_code:
            new_cells.append(cell)
            continue

        assert 'lang' in cell_metadata, \
            f'Cell "{source_code[0]} ..." has no "lang" property'
        assert cell_metadata['lang'], \
            f'Cell "{source_code[0]} ..." has empty "lang" property'

        meta_languages = cell_metadata['lang'].split(',')

        for meta_lang in meta_languages:
            assert meta_lang in languages, \
                f'Cell "{source_code[0]} ..." has invalid lang "{meta_lang}"'

        if lang in meta_languages:
            new_cells.append(cell)

    new_dict = {
        'cells': new_cells,
        'metadata': src_dict['metadata'],
        'nbformat': src_dict['nbformat'],
        'nbformat_minor': src_dict['nbformat_minor'],
    }

    with open(new_path, 'w', newline='\n') as ipynb:
        json.dump(new_dict, ipynb, ensure_ascii=False, indent=1)
        ipynb.write('\n')

    return len(new_cells)


def make_nodebooks(src_file: str, lang: str, force_rebuild: bool = False):
    '''Update or rebuild the student and the teacher notebooks of language lang

    The student version will have the cells with the tag "exer".
    The teacher version will have the cells with the tag "soln".
    When there is no specific tag, both versions will have the cell.

    Arguments:
    src_file -- notebook filename (*.ipynb) expected to be in src/
    lang -- language code, either "en" or "fr"
    force_rebuild -- if True, it overrides the modification time test
    '''

    versions = {
        'student': {'dir_prefix': '', 'remove_tag': 'soln'},
        'teacher': {'dir_prefix': 'solution-', 'remove_tag': 'exer'},
    }
    nb_cells = {version: 0 for version in versions.keys()}

    src_path = os.path.join('src', src_file)
    src_mtime = os.path.getmtime(src_path)

    for version, attrib in versions.items():
        dir_name = f"{attrib['dir_prefix']}{lang}"
        new_path = os.path.join(dir_name, src_file)

        if os.path.isfile(new_path):
            new_mtime = os.path.getmtime(new_path)
        else:
            new_mtime = 0.0

        if (new_mtime < src_mtime) or force_rebuild:
            nb_cells[version] = make_nodebook(
                src_path,
                new_path,
                lang,
                attrib['remove_tag'])

    assert nb_cells['student'] == nb_cells['teacher'], \
        f'student and teacher versions have different number of cells ({lang})'


def make_all_nodebooks():
    '''Update or rebuild all notebooks

    All notebooks:
    - for all source files
        - for all languages in [en, fr]
            - for student and teacher versions
    '''

    arg_parser = argparse.ArgumentParser(
        prog='python make.py',
        description='Generates material and solution per language')

    arg_parser.add_argument(
        '-r', '--rebuild', action='store_true',
        help='Force rebuilding notebooks')

    args = arg_parser.parse_args()

    for src_file in notebook_files:
        for lang in languages:
            make_nodebooks(src_file, lang, args.rebuild)


if __name__ == '__main__':
    make_all_nodebooks()
