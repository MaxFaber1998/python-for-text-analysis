from utils import load_root, get_talks, get_word_count_overview, get_mean_talk_length, get_datetime_overview


def find_wc(talks, length='longest'):
	"""

	:param talks:
	:param length:
	:return:
	"""
	keyword_longest = 'longest'
	keyword_shortest = 'shortest'
	assert length in [keyword_longest, keyword_shortest],\
		f"Please specify a valid length requirement, possible options are '{keyword_longest}' and '{keyword_shortest}'!"
	word_count_overview = get_word_count_overview(talks)
	mean_talk_length = get_mean_talk_length(word_count_overview)
	mean_talk_length = int(mean_talk_length)

	if length == 'longest':
		talk_overview = max(word_count_overview, key=lambda talk: talk['talk_word_count'])
	else:
		talk_overview = min(word_count_overview, key=lambda talk: talk['talk_word_count'])
	talk_titles = [talk['talk_title'] for talk in word_count_overview if talk['talk_word_count'] == talk_overview['talk_word_count']]
	talk_ids = [talk['talk_id'] for talk in word_count_overview if talk['talk_word_count'] == talk_overview['talk_word_count']]
	return talk_titles, talk_ids, mean_talk_length


def find_date(talks, time='latest'):
	"""

	:param talks:
	:param time:
	:return:
	"""
	keyword_latest = 'latest'
	keyword_oldest = 'oldest'
	assert time in [keyword_oldest, keyword_latest],\
		f"Please specify a valid time requirement, possible options are '{keyword_latest}' and '{keyword_oldest}'!"
	datetime_overview = get_datetime_overview(talks)
	if time == 'latest':
		talk_overview = max(datetime_overview, key=lambda talk: talk['talk_datetime'])
	else:
		talk_overview = min(datetime_overview, key=lambda talk: talk['talk_datetime'])
	talk_titles = [talk['talk_title'] for talk in datetime_overview if talk['talk_datetime'] == talk_overview['talk_datetime']]
	talk_ids = [talk['talk_id'] for talk in datetime_overview if talk['talk_datetime'] == talk_overview['talk_datetime']]
	return talk_titles, talk_ids


# find_date:
# 	input: list of all talk elements (positional), time (latest/oldest, keyword argument)
# 	output: title(s), id(s)


if __name__ == '__main__':
	# Load the english XML file into memory and find all talks
	path_ted_xml_english = '../Data/ted-talks/XML_releases/xml/ted_en-20160408.xml'
	root = load_root(path_ted_xml_english)
	talks = get_talks(root)

	print(f'The total number of English talks is: {len(talks)}\n')
	print(f'Talk length:')

	titles_longest, ids_longest, mean_word_count = find_wc(talks, length='longest')
	print(f'Longest talk(s): {titles_longest} (id(s): {ids_longest})')

	titles_shortest, ids_shortest, _ = find_wc(talks, length='shortest')
	print(f'Shortest talk(s): {titles_shortest} (id(s): {ids_shortest})')
	print(f'Mean word count: {mean_word_count}\n')

	titles_latest, ids_latest = find_date(talks, time='latest')
	print(f'Latest talk(s): {titles_latest} (id(s): {ids_latest})')

	titles_oldest, ids_oldest = find_date(talks, time='oldest')
	print(f'Oldest talk(s): {titles_oldest} (id(s): {ids_oldest})')
