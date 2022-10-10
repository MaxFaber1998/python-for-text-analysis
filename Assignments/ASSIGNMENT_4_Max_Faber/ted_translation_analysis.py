import os

from glob import glob
from utils import load_root, get_talks, get_talk_title, get_talk_id
from collections import defaultdict

def map_languages_to_paths():
    """

    :return:
    """
    languages_to_paths = dict()

    for file_path in glob('../Data/ted-talks/XML_releases/xml/*.xml'):
        basename = os.path.basename(file_path)
        filename, extension = os.path.splitext(basename)
        _, language_and_date = filename.split('_')
        char_list_non_numeric = [char for char in language_and_date if not char.isdigit()]
        filename_non_numeric = ''.join(char_list_non_numeric)
        language = filename_non_numeric.strip('-')

        languages_to_paths[language] = file_path
    return languages_to_paths


def find_coverage(languages_to_paths, most_least_languages):
    """

    :param languages_to_paths:
    :param most_least_languages:
    :return:
    """
    languages_to_translation_count = dict()

    for language, file_path in languages_to_paths.items():
        if language == 'en':
            # It wouldn't be fair to let English join the race, as technically it's always a translation to itself
            continue
        root = load_root(file_path)
        talks = get_talks(root)
        n_translations = len(talks)
        languages_to_translation_count[language] = n_translations
    dict_items = languages_to_translation_count.items()

    if most_least_languages == 'most':
        language_to_translation_count = max(dict_items, key=lambda dict_obj: dict_obj[1])
    else:
        language_to_translation_count = min(dict_items, key=lambda dict_obj: dict_obj[1])
    n_translations = language_to_translation_count[1]
    min_max_languages_list = [language for language in dict_items if n_translations == language[1]]
    min_max_languages_dict = dict(min_max_languages_list)
    return min_max_languages_dict


def get_id_title_dict(path_english_xml):
    """

    :param path_english_xml:
    :return:
    """
    root = load_root(path_english_xml)
    talks = get_talks(root)
    ids_to_titles = dict()

    for talk in talks:
        talk_title = get_talk_title(talk)
        talk_id = get_talk_id(talk)
        ids_to_titles[talk_id] = talk_title
    return ids_to_titles


def map_talks_to_languages(languages_to_paths):
    """

    :param languages_to_paths:
    :return:
    """
    talks_to_languages = defaultdict(list)

    for language, file_path in languages_to_paths.items():
        root = load_root(file_path)
        talks = get_talks(root)

        if language == 'en':
            continue # We don't count English as a translation as it's the origin language
        for talk in talks:
            talk_id = get_talk_id(talk)

            talks_to_languages[talk_id].append(language)
    return talks_to_languages


def map_nlang_to_talks(talks_to_languages):
    """

    :param talks_to_languages:
    :return:
    """
    nlang_to_talks = defaultdict(list)

    for talk_id, languages in talks_to_languages.items():
        n_langs = len(languages)
        nlang_to_talks[n_langs].append(talk_id)
    return nlang_to_talks


def find_top_coverage(languages_to_paths, most_least_languages):
    """

    :param languages_to_paths:
    :param most_least_languages:
    :return:
    """
    talks_to_languages = map_talks_to_languages(languages_to_paths)
    nlang_to_talks = map_nlang_to_talks(talks_to_languages)

    if most_least_languages == 'most':
        selected_lang_talk_tuple = max(nlang_to_talks.items(), key=lambda lang_talk_tuple: lang_talk_tuple[0])
    else:
        selected_lang_talk_tuple = min(nlang_to_talks.items(), key=lambda lang_talk_tuple: lang_talk_tuple[0])

    talk_ids = selected_lang_talk_tuple[1]
    path_ted_xml_english = '../Data/ted-talks/XML_releases/xml/ted_en-20160408.xml'
    ids_to_titles = get_id_title_dict(path_ted_xml_english)
    talk_titles_to_langs = dict()
    for talk_id in talk_ids:
        talk_title = ids_to_titles[talk_id]
        languages = talks_to_languages[talk_id]
        talk_titles_to_langs[talk_title] = languages
    return talk_titles_to_langs


if __name__ == '__main__':
    languages_to_paths = map_languages_to_paths()
    print('Languages to paths dictionary:')
    print(f'\t{languages_to_paths}')
    print()

    most_translated_languages = find_coverage(languages_to_paths, most_least_languages='most')
    print('Most translated languages:')
    print(f'\t{most_translated_languages}')
    least_translated_languages = find_coverage(languages_to_paths, most_least_languages='least')
    print('Least translated languages:')
    print(f'\t{least_translated_languages}')
    print()

    print('Most translated talks:')
    most_translated_talks = find_top_coverage(languages_to_paths, most_least_languages='most')
    print(f'\t{most_translated_talks}')
    print('Least translated talks:')
    least_translated_talks = find_top_coverage(languages_to_paths, most_least_languages='least')
    print(f'\t{least_translated_talks}')
