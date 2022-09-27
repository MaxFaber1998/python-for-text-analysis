import os, glob
from nltk.tokenize import sent_tokenize, word_tokenize


def get_paths(input_folder):
	"""
	Gets all the paths of files that end with the .txt file-extension
	:param input_folder: The path of the folder to search in
	:return: List of the found filenames
	"""
	# glob.glob() returns a list already so there's no need to iterate over it again
	txt_filenames = glob.glob(f'{input_folder}/*.txt')

	return txt_filenames


def get_basic_stats(txt_path):
	"""
	Collects basic statistics of the contents of the given file
	:param txt_path: Path to the file to gather the statistics of
	:return: A dictionary which contains the statistics ('num_sents', 'num_tokens', 'vocab_size' and 'num_chapters_or_aacts')
	"""
	statistics = dict()

	with open(txt_path, mode='r', encoding='utf-8') as input_file:
		file_content = input_file.read()
	sentences = sent_tokenize(file_content) # Store all sentences in a list
	statistics['num_sents'] = len(sentences) # The length of this list equals the no. sentences

	# Initialize the no. tokens to zero, we will count them by iterating over the sentences
	statistics['num_tokens'] = 0
	word_frequencies = dict() # Keep track of all unique words with its corresponding occurrences
	for sent in sentences:
		words = word_tokenize(sent) # Tokenize the current sentence
		# Increment num_tokens with the number of tokens in the current sentence
		statistics['num_tokens'] += len(words)
		# Update the dictionary based on the current word
		for word in words:
			if word in word_frequencies:
				word_frequencies[word] += 1
				continue
			word_frequencies[word] = 1

	# The dictionary keeps track of the unique words
	# So the length of this dictionary can be utilized to get the vocabulary size
	statistics['vocab_size'] = len(word_frequencies)

	# Sort the dictionary with its value (frequency) as the sorting key in reverse (from high to low)
	dict_sorted = sorted(word_frequencies.items(), key=lambda x: x[1], reverse=True)
	# Now extract the words from the tuples in the list
	list_sorted = [word for word, freq in dict_sorted]
	# Put the first 30 (30 highest) values of the list in the statistics dictionary
	statistics['top_30_tokens'] = list_sorted[:30]

	filename = os.path.basename(txt_path) # Strip the filename of the entire path
	# Count the no. occurrences of 'CHAPTER', 'Chapter', 'ACT' for 'HuckFinn.txt', 'AnnaKarenina.txt'
	# and 'Macbeth.txt' respectively
	if filename == 'HuckFinn.txt':
		statistics['num_chapters_or_acts'] = file_content.count('CHAPTER')
	elif filename == 'AnnaKarenina.txt':
		statistics['num_chapters_or_acts'] = file_content.count('Chapter')
	elif filename == 'Macbeth.txt':
		statistics['num_chapters_or_acts'] = file_content.count('ACT')
	return statistics
