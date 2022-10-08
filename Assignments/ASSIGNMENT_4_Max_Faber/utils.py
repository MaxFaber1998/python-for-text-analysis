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
	talk_head = talk.find('head')
	talk_id = talk_head.find('talkid')
	talk_id_str = talk_id.text
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


def get_word_count_talk(talk):
	"""

	:param talk: lxml element which contains the information about the talk
	:return:
	"""
	talk_content = talk.find('content')
	talk_text = talk_content.text
	talk_word_tokens = nltk.word_tokenize(talk_text)
	talk_word_token_count = len(talk_word_tokens)
	return talk_word_token_count


def get_talk_speaker(talk):
	"""

	:param talk:
	:return:
	"""
	talk_head = talk.find('head')
	talk_speaker = talk_head.find('speaker')
	talk_speaker_text = talk_speaker.text
	return talk_speaker_text


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


def print_talk_info_list(talk_titles, talk_ids):
	"""

	:param talk_titles:
	:param talk_ids:
	:return:
	"""
	talk_info = zip(talk_titles, talk_ids)
	talk_info = list(talk_info)

	for index, talk_tuple in enumerate(talk_info):
		talk_title, talk_id = talk_tuple

		print(f"\t'{talk_title}' (id: {talk_id})", end='')
		if index < len(talk_info) - 1:
			print(', ')
	print('.')
