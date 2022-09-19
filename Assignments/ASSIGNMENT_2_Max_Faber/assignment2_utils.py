def clean_text_general(text, chars_to_remove={'\n', ',', '.', '"'}):
    """
    Cleans a given text by removing a set of characters from it (default characters are: '\n', ',', '.', '"')

    :param text: The text to clean
    :param chars_to_remove: A set of characters to be removed from the text
    :return: The cleaned text
    """
    # Put text in cleaned_text beforehand
    cleaned_text = text
    for char_to_remove in chars_to_remove:
        # Every character in the set is removed from cleaned_text one-by-one
        cleaned_text = cleaned_text.replace(char_to_remove, '')
    return cleaned_text
