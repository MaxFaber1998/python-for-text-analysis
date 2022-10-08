from utils import load_root, get_talks, get_talk_id, get_talk_title, get_talk_speaker, get_word_count_talk, get_talk_datetime, print_talk_info_list


def find_wc(talks, length='longest'):
	"""
	Either gets the title(s) and id(s) of the longest or the shortest talk(s), also gets the mean word count of all talks
	:param talks: List of talk objects
	:param length: Keyword which indicates whether the longest or shortest talk(s) should be looked up
	:return: Tuple containing a list of title(s), a list of id(s) and the mean word count (respectively)
	"""
	# Check whether the given length is in the possible options
	keyword_longest = 'longest'
	keyword_shortest = 'shortest'
	assert length in [keyword_longest, keyword_shortest],\
		f"Please specify a valid length requirement, possible options are '{keyword_longest}' and '{keyword_shortest}'!"

	# Define a list in which an overview of the word counts per talk are going to be stored
	word_count_overview = []
	# Define a variable which in which the sum of the word counts is going to be stored, so that the mean can be calculated
	word_count_sum = 0

	for talk in talks:
		# Get the necessary information from the talk object to construct an object
		talk_id = get_talk_id(talk)
		talk_title = get_talk_title(talk)
		talk_word_count = get_word_count_talk(talk)

		# Construct an object containing all necessary information about the current talk and append it to the list
		word_count_overview.append({
			'talk_id': talk_id,
			'talk_title': talk_title,
			'talk_word_count': talk_word_count
		})
		# Increment the word count sum with the current word count
		word_count_sum += talk_word_count

	# Calculate the mean talk length
	mean_talk_length = word_count_sum / len(talks)
	# Cast it to an integer
	mean_talk_length = int(mean_talk_length)

	if length == 'longest':
		# Get the word count overview dictionary with the largest value for the key 'talk_word_count'
		selected_word_count_overview = max(word_count_overview, key=lambda talk: talk['talk_word_count'])
	else: # If the length keyword is not 'longest', it must be 'shortest' as the assertion check above has been passed
		# Get the word count overview dictionary with the smallest value for the key 'talk_word_count'
		selected_word_count_overview = min(word_count_overview, key=lambda talk: talk['talk_word_count'])

	# Define two lists called 'talk_titles' and 'talk_ids', which are going to be the return values after adding the corresponding value(s)
	talk_titles = []
	talk_ids = []
	for word_count_talk in word_count_overview:
		# Find all word count overview dictionaries with the word count stored in 'selected_word_count_overview'
		if word_count_talk['talk_word_count'] == selected_word_count_overview['talk_word_count']:
			# Store the talk title and talk id in a variable
			talk_title = word_count_talk['talk_title']
			talk_id = word_count_talk['talk_id']

			# Append the variables to the lists
			talk_titles.append(talk_title)
			talk_ids.append(talk_id)
	# Return the tuple of talk title(s), talk id(s) and the mean talk length
	return talk_titles, talk_ids, mean_talk_length


def find_date(talks, time='latest'):
	"""
	Either gets the title(s) and id(s) of the latest or the oldest talk(s)
	:param talks: List of talk objects
	:param time: Keyword which indicates whether the latest or oldest talk(s) should be looked up
	:return: Tuple containing a list of title(s) and a list of id(s)
	"""
	# Check whether the given time is in the possible options
	keyword_latest = 'latest'
	keyword_oldest = 'oldest'
	assert time in [keyword_oldest, keyword_latest],\
		f"Please specify a valid time requirement, possible options are '{keyword_latest}' and '{keyword_oldest}'!"

	# Define a list in which an overview of the datetime objects per talk are going to be stored
	datetime_overview = []

	for talk in talks:
		# Get the necessary information from the talk object to construct an object
		talk_id = get_talk_id(talk)
		talk_title = get_talk_title(talk)
		talk_datetime = get_talk_datetime(talk)

		# Construct an object containing all necessary information about the current talk and append it to the list
		datetime_overview.append({
			'talk_id': talk_id,
			'talk_title': talk_title,
			'talk_datetime': talk_datetime
		})

	if time == 'latest':
		# Get the datetime overview dictionary with the largest value for the key 'talk_datetime'
		selected_datetime_overview = max(datetime_overview, key=lambda talk: talk['talk_datetime'])
	else: # If the time keyword is not 'latest', it must be 'oldest' as the assertion check above has been passed
		# Get the datetime overview dictionary with the smallest value for the key 'talk_datetime'
		selected_datetime_overview = min(datetime_overview, key=lambda talk: talk['talk_datetime'])

	# Define two lists called 'talk_titles' and 'talk_ids', which are going to be the return values after adding the corresponding value(s)
	talk_titles = []
	talk_ids = []
	for datetime_talk in datetime_overview:
		# Find all datetime overview dictionaries with the word count stored in 'selected_datetime_overview'
		if datetime_talk['talk_datetime'] == selected_datetime_overview['talk_datetime']:
			# Store the talk title and talk id in a variable
			talk_title = datetime_talk['talk_title']
			talk_id = datetime_talk['talk_id']

			# Append the variables to the lists
			talk_titles.append(talk_title)
			talk_ids.append(talk_id)
	# Return the tuple of talk title(s) and the talk id(s)
	return talk_titles, talk_ids


def find_speaker(talks):
	"""
	Gets the speakers which gave multiple talks, with its corresponding talk ids and titles
	:param talks: List of talk objects
	:return: A dictionary which has the names of the speakers as its keys and a list of tuples containing the talk ids and titles respectively
	"""
	# Define an intermediate dictionary which is going to store the id(s) and title(s) of each speaker
	talk_speakers = dict()

	for talk in talks:
		# Get the necessary information from the talk object
		talk_id = get_talk_id(talk)
		talk_title = get_talk_title(talk)
		talk_speaker = get_talk_speaker(talk)

		# Create an entry with an empty list in the dictionary for the current talk speaker if there's no one yet
		if talk_speaker not in talk_speakers.keys():
			talk_speakers[talk_speaker] = []
		# Construct the tuple which is going to be stored in the value of the dictionary for the current talk speaker
		talk_info_tuple = (talk_id, talk_title)
		# Append the tuple to the list for the current speaker
		talk_speakers[talk_speaker].append(talk_info_tuple)

	# Define a dictionary which is going to store the ids and titles of the speakers who gave multiple talks
	multiple_talk_speakers = dict()

	for talk_speaker, talk_info_tuple_list in talk_speakers.items():
		# Check whether the list contains more than one tuple
		if len(talk_info_tuple_list) > 1:
			# Create an entry in the new dictionary with the list of tuples for the given talk speaker
			multiple_talk_speakers[talk_speaker] = talk_info_tuple_list
	return multiple_talk_speakers



if __name__ == '__main__':
	# Load the english XML file into memory and find all talks
	path_ted_xml_english = '../Data/ted-talks/XML_releases/xml/ted_en-20160408.xml'
	root = load_root(path_ted_xml_english)
	talks = get_talks(root)

	# Print the number of English talks (length of the talks list)
	print(f'The total number of English talks is: {len(talks)}\n')

	# Get and print longest title(s) and id(s) of the longest talk
	print('Talk length:')
	print('Longest talk(s):')
	titles_longest, ids_longest, mean_word_count = find_wc(talks, length='longest')
	print_talk_info_list(titles_longest, ids_longest)

	# Get and print longest title(s) and id(s) of the shortest talk
	print('Shortest talk(s):')
	titles_shortest, ids_shortest, _ = find_wc(talks, length='shortest')
	print_talk_info_list(titles_shortest, ids_shortest)

	print(f'Mean word count: {mean_word_count}\n')

	print('Latest talk(s):')
	titles_latest, ids_latest = find_date(talks, time='latest')
	print_talk_info_list(titles_latest, ids_latest)

	print('Oldest talk(s)')
	titles_oldest, ids_oldest = find_date(talks, time='oldest')

	print()

	print('Speaker(s) with multiple talks:')
	multiple_talk_speakers = find_speaker(talks)
	for speaker, talk_info_tuple_list in multiple_talk_speakers.items():
		talk_ids = [talk_info_tuple[0] for talk_info_tuple in talk_info_tuple_list]
		talk_titles = [talk_info_tuple[1] for talk_info_tuple in talk_info_tuple_list]

		print(f'Speaker {speaker} had the following talks:')
		print_talk_info_list(talk_titles, talk_ids)