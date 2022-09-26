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
	unique_words = set() # Keep track of all the uniquely identified words so far
	for sent in sentences:
		words = word_tokenize(sent) # Tokenize the current sentence
		# Increment num_tokens with the number of tokens in the current sentence
		statistics['num_tokens'] += len(words)
		unique_words.update(set(words))
	# Use the unique set of words to get the size of the vocabulary
	statistics['vocab_size'] = len(unique_words)

	filename = os.path.basename(txt_path) # Strip the filename of the entire path
	# Then count the no. occurrences of 'CHAPTER', 'Chapter', 'ACT' for 'HuckFinn.txt', 'AnnaKarenina.txt'
	# and 'Macbeth.txt' respectively
	if filename == 'HuckFinn.txt':
		statistics['num_chapters_or_acts'] = file_content.count('CHAPTER')
	elif filename == 'AnnaKarenina.txt':
		statistics['num_chapters_or_acts'] = file_content.count('Chapter')
	elif filename == 'Macbeth.txt':
		statistics['num_chapters_or_acts'] = file_content.count('ACT')
	return statistics
