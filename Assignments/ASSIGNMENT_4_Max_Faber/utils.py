def get_talk_content_text(talk_object):
	"""
	Gets the content text of a Ted's talk
	:param talk_object: lxml element which contains the information about the talk
	:return:
	"""
	talk_content = talk_object.find('content')
	talk_text = talk_content.text
	return talk_text


def find_shortest_talk(talks):
	"""

	:param talks:
	:return:
	"""
	pass


def find_longest_talk(talks):
	"""

	:param talks:
	:return:
	"""
	pass


def find_mean_talk_length(talks):
	"""

	:param talks:
	:return:
	"""
	pass