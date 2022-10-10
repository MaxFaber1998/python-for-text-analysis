from utils import load_root, get_talks, get_talk_id, get_talk_title, get_talk_speaker, get_talk_word_count, get_talk_datetime, print_talk_info_list


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

	# As the word count per talk is an expensive function because of nltk.word_tokenize()
	# and is either required for determining the mean word count as the longest/shortest talk,
	# We construct a list of tuples which has the talk object as its first element
	# and its corresponding word count as its second element
	# This list can then be utilized for both aforementioned tasks
	talk_word_counts = [(talk, get_talk_word_count(talk)) for talk in talks]

	# Define a list in which the word counts of all talks are being stored
	word_counts = [talk_word_count[1] for talk_word_count in talk_word_counts]
	# Calculate the mean talk length based on this list
	mean_talk_length = sum(word_counts) / len(word_counts)
	# Cast it to an integer
	mean_talk_length = int(mean_talk_length)

	if length == 'longest':
		# Get the talk/word_count tuple with the largest value for the word count (second element of the tuple)
		selected_talk = max(talk_word_counts, key=lambda talk: talk[1])
	else: # If the length keyword is not 'longest', it must be 'shortest' as the assertion check above has been passed
		# Get the talk/word_count tuple with the smallest value for the word count (second element of the tuple)
		selected_talk = min(talk_word_counts, key=lambda talk: talk[1])

	# Construct a list of all talk/word_count tuples with the word count equal to the word count in 'selected_talk' (second element of both tuples)
	# This is necessary as it's possible that there's multiple talks with this word count
	# The min() and max() functions only return one talk, even if there's multiple talks that satisfy this same requirement
	selected_talks = [talk for talk in talk_word_counts if talk[1] == selected_talk[1]]
	# Construct a list of all title(s) and a list of all id(s)
	talk_titles = [get_talk_title(talk[0]) for talk in selected_talks]
	talk_ids = [get_talk_id(talk[0]) for talk in selected_talks]

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

	if time == 'latest':
		# Get the talk with the latest datetime
		selected_talk = max(talks, key=lambda talk: get_talk_datetime(talk))
	else: # If the time keyword is not 'latest', it must be 'oldest' as the assertion check above has been passed
		# Get the talk with the oldest datetime
		selected_talk = min(talks, key=lambda talk: get_talk_datetime(talk))

	# Construct a list of all title(s) and a list of all id(s)
	# It's necessary to search for all talk objects with the datetime stored in 'selected_talk', as it's possible that
	# there's multiple talks with this datetime
	# The min() and max() functions only return one talk, even if there's multiple talks that satisfy this same requirement
	talk_titles = [get_talk_title(talk) for talk in talks if get_talk_datetime(talk) == get_talk_datetime(selected_talk)]
	talk_ids = [get_talk_id(talk) for talk in talks if get_talk_datetime(talk) == get_talk_datetime(selected_talk)]

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
	titles_longest, ids_longest, mean_word_count = find_wc(talks, length='longest')
	print('Longest talk(s):')
	print_talk_info_list(titles_longest, ids_longest)

	# Get and print longest title(s) and id(s) of the shortest talk
	titles_shortest, ids_shortest, _ = find_wc(talks, length='shortest')
	print('Shortest talk(s):')
	print_talk_info_list(titles_shortest, ids_shortest)

	# Print the mean word count
	print(f'Mean word count: {mean_word_count}\n')

	# Get and print the title(s) and id(s) of the latest talk(s)
	titles_latest, ids_latest = find_date(talks, time='latest')
	print('Latest talk(s):')
	print_talk_info_list(titles_latest, ids_latest)

	# Get and print the title(s) and id(s) of the oldest talk(s)
	titles_oldest, ids_oldest = find_date(talks, time='oldest')
	print('Oldest talk(s)')
	print_talk_info_list(titles_oldest, ids_oldest)

	print()

	# Get and print the title(s) and id(s) of the speakers which gave multiple talks
	multiple_talk_speakers = find_speaker(talks)
	print('Speaker(s) with multiple talks:')
	for speaker, talk_info_tuple_list in multiple_talk_speakers.items():
		# Construct lists of the id(s) (first element) and title(s) (second element) separately using the list of tuples
		# We need this data format in order to utilize the utility function 'print_talk_info_list()'
		talk_ids = [talk_info_tuple[0] for talk_info_tuple in talk_info_tuple_list]
		talk_titles = [talk_info_tuple[1] for talk_info_tuple in talk_info_tuple_list]

		print(f'Speaker {speaker} had the following talks:')
		print_talk_info_list(talk_titles, talk_ids)