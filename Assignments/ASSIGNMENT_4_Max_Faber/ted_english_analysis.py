import nltk

from lxml import etree as et
from utils import find_shortest_talk, find_longest_talk, find_mean_talk_length


def find_wc(talks, length='shortest'):
	"""

	:param talks:
	:param length:
	:return:
	"""
	keyword_shortest = 'shortest'
	keyword_longest = 'longest'
	keyword_mean = 'mean'
	result = ('', '', -1)

	assert(length in [keyword_shortest, keyword_longest, keyword_mean], f"Please specify a valid length requirement, possible options are '{keyword_shortest}', '{keyword_longest}' and '{keyword_mean}!'")
	if length == 'shortest':
		result = find_shortest_talk(talks)
	elif length == 'longest':
		result = find_longest_talk(talks)
	elif length == 'mean':
		result = find_mean_talk_length()
	return result

# Create a python scipt which give you the following information:
#   What is the longest talk (in terms of word count), what is the shortest talk (in terms of word count), what is the average word count? (id and title, numbers) (find_length)
#   Oldest and latest talk (id and title, dates) (find_date)
#   Is there a speaker with multiple talks? (function: find_speaker)
#   How many English talks are there in total? (No function required, you can simply use a built-in function on the list of all English talk elements.)

# find_wc:
#   input: list of all talk elements (positional), length (longest/shortest, keyword argument)
#   output: title(s), id(s), mean word count
# find_date:
#   input: list of all talk elements (positional), time (latest/oldest, keyword argument)
#   output: title(s), id(s)
# find_speaker:
#   input: list of talk elemenets (position)
#   output: dict mapping speakers with more than one talk to their talks (tuple of talk title and id)

# The total number of English talks is: [total number]
#
# Talk length:
# Longest talk: [title] (id: [id])
# Shortest talk: [title] (id: [id])
# Mean word count: [mean word count]
if __name__ == '__main__':
	# Load the english XML file into memory and find all talks
	path_ted_xml_english = '../Data/ted-talks/XML_releases/xml/ted_en-20160408.xml'
	tree = et.parse(path_ted_xml_english)
	root = tree.getroot()
	talks = root.findall('file')
	titles, ids, mean_word_count = find_wc(talks, length='shortest')
