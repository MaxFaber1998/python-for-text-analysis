# This module contains a string called 'punctuation'
# All the characters in this string are removed from the text which is passed into the function text()
import string


def preprocess(text):
	"""
	Preprocesses text by removing its punctuation
	:param text: The text to remove the punctuation of
	:return: Text without punctuation
	"""
	# Iterate over all punctuation characters
	for punc_char in string.punctuation:
		# If the current character is not in 'text', there's no need to call str.replace()
		if punc_char not in text:
			continue
		text = text.replace(punc_char, '')
	# The punctuation characters are now removed so the modified text can be returned
	return text