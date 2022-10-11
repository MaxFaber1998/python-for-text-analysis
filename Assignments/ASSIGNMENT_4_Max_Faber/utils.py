from lxml import etree as et
from datetime import datetime

import nltk


def load_root(path):
	"""
	Load the root of the XML file
	:param path: Path of the XML file
	:return: Root object of the XML file
	"""
	tree = et.parse(path)
	root = tree.getroot()
	return root


def get_talks(root):
	"""
	Get all talks af the root object of an XML object
	:param root: Root object
	:return: List of file (talk) objects
	"""
	talks = root.findall('file')
	return talks


def get_talk_id(talk):
	"""
	Gets the id of a talk
	:param talk: Talk object
	:return: The talk id (integer)
	"""
	# Get the head of the talk object
	talk_head = talk.find('head')
	# Find the talk id object in the talk head object
	talk_id = talk_head.find('talkid')
	# Extract the id (string) from the talk id object
	talk_id_str = talk_id.text
	# Cast the talk id (string) to an integer
	talk_id_int = int(talk_id_str)
	return talk_id_int


def get_talk_title(talk):
	"""
	Get the title of the given talk
	:param talk: Talk object
	:return: The title of the talk (string)
	"""
	# Get the head object of the talk object
	talk_head = talk.find('head')
	# Find the title of the talk object
	talk_title = talk_head.find('title')
	# Extract the title (string) from the head object of the talk object
	talk_title_text = talk_title.text
	return talk_title_text


def get_talk_word_count(talk):
	"""
	Get the no. words of the given talk
	:param talk: Talk object
	:return: The no. words spoken during the talk (integer)
	"""
	# Find an object containing the content of the talk
	talk_content = talk.find('content')
	# Extract the text from the talk content oject
	talk_text = talk_content.text
	# Tokenize the words of the talk content using the nltk package
	talk_word_tokens = nltk.word_tokenize(talk_text)
	# Get the no. tokens
	talk_word_token_count = len(talk_word_tokens)
	return talk_word_token_count


def get_talk_speaker(talk):
	"""
	Get the speaker of the given talk
	:param talk: Talk object
	:return: The speaker of the talk (string)
	"""
	# Find the head object of the talk object
	talk_head = talk.find('head')
	# Find the speaker object of the head object
	talk_speaker = talk_head.find('speaker')
	# Extract the speaker (string) from the speaker object
	talk_speaker_text = talk_speaker.text
	return talk_speaker_text


def get_talk_datetime(talk):
	"""
	Get a datetime object of which the given talk was given
	:param talk: Talk object
	:return: Datetime of the given talk
	"""
	# Find the head object of the given talk object
	talk_head = talk.find('head')
	# Find the date object of the head object
	talk_date = talk_head.find('date')
	# Extract the date (string) from the date object
	talk_date_text = talk_date.text
	# Convert the date (string) to a datetime object ('%Y/%m/%d' indicates the format, for example: 2005/04/22)
	talk_date_object = datetime.strptime(talk_date_text, '%Y/%m/%d')
	return talk_date_object


def print_info_lists(string_values, integer_values, integer_value_description):
	"""
	Prints an indented overview of the given string and integer values in the following format:
		'<string_value>' (<integer_value_description>: <integer_value>)
	This function has been written as it's utilized multiple times and will therefore clean up redundant code
	:param string_values: A list of string values to be printed
	:param integer_values: A list of integer values to be printed
	:param integer_value_description: String description of the numerical value
	:return: None
	"""
	# Zip the strings and integers together, as they're in the same order
	info_zipped = zip(string_values, integer_values)
	# Convert the zip object to a list of tuples (strings: first element, integers: second element)
	info_zipped = list(info_zipped)

	# Iterate over the list of tuples with strings and integers
	for index, val_tuple in enumerate(info_zipped):
		# Extract the current string and integer from the tuple
		string_value, integer_value = val_tuple

		# Print the string with it's corresponding integer with a tab at the start in order to improve readability
		print(f"\t'{string_value}' ({integer_value_description}: {integer_value})", end='')
		# Check if the current iteration is not the latest one
		if index < len(info_zipped) - 1:
			# If not, print a comma to showcase it's not the latest element in the output
			print(',')
	# Print a period to showcase the end of the overview
	print('.')


def assert_key(key, keys):
	"""
	Does an assertion check whether the given key is in the list of given keys
	:param key: The specified key
	:param keys: List of keys where the given key should be in
	:return: None
	"""
	# Define the base of the assertion message
	assertion_message = 'Please specify a valid key, possible option(s) are'

	# Iterate over the keys list using the enumerate function, so we also get the current index in each iteration
	for index, k in enumerate(keys):
		# Append the key with a space at front to the assertion message
		assertion_message += f" '{k}'"
		# List the possible options using ',' and 'and' between the last two options
		if index < len(keys) - 2:
			assertion_message += ','
		elif index < len(keys) - 1:
			assertion_message += ' and'
	assertion_message += '!'

	# Perform the actual assertion using the generated assertion message
	assert key in keys,\
		assertion_message
