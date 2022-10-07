from lxml import etree as et
from datetime import datetime

import nltk


def load_root(path):
	tree = et.parse(path)
	root = tree.getroot()
	return root


def get_talks(root):
	talks = root.findall('file')
	return talks


def get_talk_id(talk):
	"""

	:param talk:
	:return:
	"""
	talk_id_str = talk.get('id')
	talk_id_int = int(talk_id_str)

	return talk_id_int


def get_talk_title(talk):
	"""

	:param talk:
	:return:
	"""
	talk_head = talk.find('head')
	talk_title = talk_head.find('title')
	talk_title_text = talk_title.text

	return talk_title_text


def get_word_token_count_talk(talk):
	"""

	:param talk: lxml element which contains the information about the talk
	:return:
	"""
	talk_content = talk.find('content')
	talk_text = talk_content.text
	talk_word_tokens = nltk.word_tokenize(talk_text)
	talk_word_token_count = len(talk_word_tokens)
	return talk_word_token_count


def get_word_count_overview(talks):
	"""

	:param talks:
	:return:
	"""
	talk_overview_list = []

	for talk in talks:
		talk_id = get_talk_id(talk)
		talk_title = get_talk_title(talk)
		talk_word_count = get_word_token_count_talk(talk)

		talk_overview_list.append({
			'talk_id': talk_id,
			'talk_title': talk_title,
			'talk_word_count': talk_word_count
		})

	return talk_overview_list


def get_mean_talk_length(talk_overview_list):
	"""

	:param talks:
	:return:
	"""
	n_words_talks = []

	for talk_overview in talk_overview_list:
		n_words_talk = talk_overview['talk_word_count']

		n_words_talks.append(n_words_talk)
	return sum(n_words_talks) / len(n_words_talks)


def get_talk_datetime(talk):
	"""

	:param talk:
	:return:
	"""
	talk_head = talk.find('head')
	talk_date = talk_head.find('date')
	talk_date_text = talk_date.text
	talk_date_object = datetime.strptime(talk_date_text, '%Y/%m/%d')
	return talk_date_object


def get_datetime_overview(talks):
	"""

	:param talks:
	:return:
	"""
	talk_datetime_overview = []

	for talk in talks:
		talk_id = get_talk_id(talk)
		talk_title = get_talk_title(talk)
		talk_datetime = get_talk_datetime(talk)

		talk_datetime_overview.append({
			'talk_id': talk_id,
			'talk_title': talk_title,
			'talk_datetime': talk_datetime
		})
	return talk_datetime_overview



# Remove this if not longer necessary, only for testing
# if __name__ == '__main__':
	# path_ted_xml_english = '../Data/ted-talks/XML_releases/xml/ted_en-20160408.xml'
	# root = load_root(path_ted_xml_english)
	# talks = get_talks(root)
	# print(get_datetime(talks[0]))
