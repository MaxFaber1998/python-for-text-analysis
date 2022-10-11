import os

from glob import glob
from utils import load_root, get_talks, get_talk_title, get_talk_id, assert_key
from collections import defaultdict

def map_languages_to_paths():
    """
    Get a dictionary which maps language abbreviations (key) to its corresponding relative XML paths (value)
    The language abbreviations are extracted from the filenames
    :return: Languages to paths dictionary
    """
    # Define the dictionary which is going to store the languages to paths
    languages_to_paths = dict()

    # Use the glob package to get all XML files in the specified directory
    for file_path in glob('../Data/ted-talks/XML_releases/xml/*.xml'):
        # Use the os package to extract the basename (filename without the directory) from the file_path
        basename = os.path.basename(file_path)
        # Use the os package again, now to detach the filename and file extension from each other
        filename, extension = os.path.splitext(basename)
        # Use the split function to get rid of 'ted_' from the filename
        _, language_and_date = filename.split('_')
        # Construct a list of all non-numeric characters in the filename
        char_list_non_numeric = [char for char in language_and_date if not char.isdigit()]
        # Convert the list of characters to a string
        filename_non_numeric = ''.join(char_list_non_numeric)
        # Strip the '-' character from the end of the string, what remains is the language abbreviation
        language = filename_non_numeric.strip('-')

        # Map the language abbreviation to the file path
        languages_to_paths[language] = file_path
    return languages_to_paths


def find_coverage(languages_to_paths, most_least_languages):
    """
    Finds the language(s) with the most or least translations from English
    :param languages_to_paths: The dictionary mapping language abbreviations to paths, generated using map_languages_to_paths()
    :param most_least_languages: A key indicating whether the language(s) with the most or least translation(s) should be looked up
    :return: A dictionary mapping the most or least translated language(s) to the no. translations
    """
    # Check whether the given key is valid
    assert_key(most_least_languages, ['most', 'least'])

    # Define a dictionary, which is going to store all language abbreviations to the no. translation(s)
    languages_to_translation_count = dict()

    # Iterate over the language to path dictionary
    for language, file_path in languages_to_paths.items():
        if language == 'en':
            # It wouldn't be fair to let English join the race, as technically it's always a translation to itself
            continue
        # Load the root using the file_path
        root = load_root(file_path)
        # Load the talks given the root object
        talks = get_talks(root)
        # Get the no. translations (equal to the no. talks)
        n_translations = len(talks)
        # Map the language to the no. translations
        languages_to_translation_count[language] = n_translations
    # Store the dictionary items object in a variable as we're going to use this multiple times
    dict_items = languages_to_translation_count.items()

    if most_least_languages == 'most':
        # Get the key-value pair with the highest value for the no. translations
        language_to_translation_count = max(dict_items, key=lambda dict_obj: dict_obj[1])
    else: # If the given key is not 'most', it must be 'least' as the assertion check before has passed
        # Get the key-value pair with the lowest value for the no. translations
        language_to_translation_count = min(dict_items, key=lambda dict_obj: dict_obj[1])
    # Extract the no. translations from the min/max key-value pair
    n_translations = language_to_translation_count[1]
    # Construct a list of key-value pairs where the no. of translations equals n_translations
    # This is necessary as it's possible that there's multiple and min/max only return one
    min_max_languages_list = [language for language in dict_items if n_translations == language[1]]
    # Convert the list of key-value pairs to a list as this is the required format
    min_max_languages_dict = dict(min_max_languages_list)
    return min_max_languages_dict


def get_id_title_dict(path_english_xml):
    """
    Get a dictionary which maps talk ids to its corresponding titles
    :param path_english_xml: Path to the XML containing the English Ted talks
    :return: Dictionary mapping talk ids to titles
    """
    # Load the root using the given path
    root = load_root(path_english_xml)
    # Get a list of all talks in the XML file
    talks = get_talks(root)
    # Define a dictionary which will store the mappings between talk ids and titles
    ids_to_titles = dict()

    for talk in talks:
        # Get the title and id of the current talk
        talk_title = get_talk_title(talk)
        talk_id = get_talk_id(talk)
        # Map the current id to its corresponding title
        ids_to_titles[talk_id] = talk_title
    return ids_to_titles


def map_talks_to_languages(languages_to_paths):
    """
    Creates a mapping between talks (by id) to the languages the talks have been translated into (list of language abbreviations)
    :param languages_to_paths: The dictionary mapping language abbreviations to paths, generated using map_languages_to_paths()
    :return: Dictionary mapping talk ids to the languages the talks have been translated into
    """
    # Define a dictionary which takes an empty list as its default value
    # This comes in handy in this case as it's no longer necessary to check if a mapping already exists
    # Now it's simply possible to append elements to the list of a given key at all times
    talks_to_languages = defaultdict(list)

    for language, file_path in languages_to_paths.items():
        # Load the root and all talks from the current XML
        root = load_root(file_path)
        talks = get_talks(root)

        if language == 'en':
            continue # We don't count English as a translation as it's the origin language
        for talk in talks:
            # Get the talk id of the current talk
            talk_id = get_talk_id(talk)

            # Append the language abbreviation to the list of translations of the current talk id
            talks_to_languages[talk_id].append(language)
    return talks_to_languages


def map_nlang_to_talks(talks_to_languages):
    """
    Construct a mapping between the no. translations to the talks that are translated that many times
    :param talks_to_languages: Dictionary mapping talk ids to the languages the talks have been translated into (generated by map_talks_to_languages())
    :return: Dictionary mapping the no. translations to the talks that are translated that many times
    """
    # Define a dictionary which takes an empty list as its default value
    # This comes in handy in this case as it's no longer necessary to check if a mapping already exists
    # Now it's simply possible to append elements to the list of a given key at all times
    nlang_to_talks = defaultdict(list)

    for talk_id, languages in talks_to_languages.items():
        # The no. translations equals the length of the languages list
        n_langs = len(languages)
        # Append the current talk id to the list belonging to the current no. translations
        nlang_to_talks[n_langs].append(talk_id)
    return nlang_to_talks


def find_top_coverage(languages_to_paths, most_least_languages):
    """
    Finds the talk(s) (title(s)) with the most or least translations and maps them to the translated language(s)
    :param languages_to_paths: The dictionary mapping language abbreviations to paths, generated using map_languages_to_paths()
    :param most_least_languages: A key indicating whether the talk(s) with the most or least translation(s) should be looked up
    :return: A dictionary mapping the most or least translated talk(s) to the languages it has/they have been translated into
    """
    # Check whether the given key is valid
    assert_key(most_least_languages, ['most', 'least'])

    # Get a dictionary which maps talk ids to the language(s) these talks have been translated into
    talks_to_languages = map_talks_to_languages(languages_to_paths)
    # Using the dictionary above, get another dictionary which maps the no. translations to the talk ids that are translated this many times
    nlang_to_talks = map_nlang_to_talks(talks_to_languages)

    if most_least_languages == 'most':
        # Get the key-value pair with the highest value for the no. translations
        selected_lang_talk_tuple = max(nlang_to_talks.items(), key=lambda lang_talk_tuple: lang_talk_tuple[0])
    else: # If the given key is not 'most', it must be 'least' as the assertion check before has passed
        # Get the key-value pair with the lowest value for the no. translations
        selected_lang_talk_tuple = min(nlang_to_talks.items(), key=lambda lang_talk_tuple: lang_talk_tuple[0])

    # Extract the talk id(s) belonging to the min/max no. translations
    talk_ids = selected_lang_talk_tuple[1]
    # Define the path of the English XML file
    path_ted_xml_english = '../Data/ted-talks/XML_releases/xml/ted_en-20160408.xml'
    # Get a dictionary mapping the talk ids to the talk titles
    ids_to_titles = get_id_title_dict(path_ted_xml_english)

    # Define a dictionary which is going to map talk title(s) to the languages these talk(s) have been translated into
    # To be more specific: the talk titles of the talks with the most or least translations
    talk_titles_to_langs = dict()
    for talk_id in talk_ids:
        # Get the talk title and languages the talk has been translated into using the dictionaries we defined earlier
        talk_title = ids_to_titles[talk_id]
        languages = talks_to_languages[talk_id]

        # Map the title to the language(s)
        talk_titles_to_langs[talk_title] = languages
    return talk_titles_to_langs


if __name__ == '__main__':
    # Get a dictionary which maps the language abbreviations to the paths their XML files are stored
    languages_to_paths = map_languages_to_paths()
    # Print this dictionary
    print('Languages to paths dictionary:')
    print(f'\t{languages_to_paths}')
    print()

    # Find the language(s) which have been translated the most
    most_translated_languages = find_coverage(languages_to_paths, most_least_languages='most')
    # Print the outcome (dictionary mapping the language abbreviation(s) to the no. translations)
    print('Most translated languages:')
    print(f'\t{most_translated_languages}')
    # Find the language(s) which have been translated the least
    least_translated_languages = find_coverage(languages_to_paths, most_least_languages='least')
    # Print the outcome (dictionary mapping the language abbreviation(s) to the no. translations)
    print('Least translated languages:')
    print(f'\t{least_translated_languages}')
    print()

    print('Most translated talks:')
    # Find the talk(s) which have been translated the most
    most_translated_talks = find_top_coverage(languages_to_paths, most_least_languages='most')
    # Print the outcome (dictionary mapping the talk title(s) to the translated language(s))
    print(f'\t{most_translated_talks}')
    print('Least translated talks:')
    # Find the talk(s) which have been translated the least
    least_translated_talks = find_top_coverage(languages_to_paths, most_least_languages='least')
    # Print the outcome (dictionary mapping the talk title(s) to the translated language(s))
    print(f'\t{least_translated_talks}')
