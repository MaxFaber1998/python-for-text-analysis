# This module contains a string called 'punctuation'
import string
from utils_3a import preprocess


def count(text):
	"""
	Counts the occurrence of the words in text
	:param text: The text to count the words of
	:return: Dictionary which contains unique words as its keys and the no. occurrences as its values
	"""
	text = preprocess(text)
	words = text.split(' ')
	word_count_dict = dict()

	for word in words:
		if word in word_count_dict:
			word_count_dict[word] += 1
			continue
		word_count_dict[word] = 1
	return word_count_dict

# Testing
if __name__ == '__main__':
	# This string contains 20 words, of which 16 unique words
	text_to_count = "This text (string) contains punctuation, this punctuation should be removed! "\
					"Afterwards, the words in this string need to be counted"
	word_count_dict = count(text_to_count)

	print(f'Text to remove punctuation and check the word frequency of: \'{text_to_count}\'\n')
	print(f'Unique words with its corresponding frequencies without punctuation: {word_count_dict}\n')

	# Test case of the (unique) no. words in the dictionary
	print(f'The dictionary should contain 16 (unique) words and actually contains {len(word_count_dict)} unique words')
	assert(len(word_count_dict) == 16)
	print('Unique word count check finished successfully!\n')

	# Test case of the total no. words in the dictionary
	print(f'The dictionary should contain 20 words in total and actually contains {sum(word_count_dict.values())} words in total')
	assert(sum(word_count_dict.values()) == 20)
	print('Total word count check finished successfully!\n')

	# Test case of the nonexistence of punctuation of the words in the dictionary
	print('Also, the words in the dictionary shouldn\'t contain punctuation characters anymore')
	# For every word in the dictionary we check if it's actually punctuation free
	for word, _ in word_count_dict.items():
		for punc_char in string.punctuation:
			assert(punc_char not in word)
	print('Punctuation check finished successfully!\n')

	# Test case of the frequency of some words in the dictionary
	print(f'The word \'string\' should occur 2 times in the string, and actually occurs {word_count_dict["string"]} times')
	assert(word_count_dict["string"] == 2)
	print(f'The word \'text\' should occur 1 time in the string, and actually occurs {word_count_dict["text"]} times')
	assert(word_count_dict["text"] == 1)
	print('Word frequency check finished successfully!')
