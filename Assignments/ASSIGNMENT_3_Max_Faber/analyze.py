import os, nltk
from utils import get_paths, get_basic_stats


if __name__ == '__main__':
	# Exercise 2
	# This resource is required in order to execute this script
	nltk.download('punkt')
	# Get all paths of txt files in the selected directory
	txt_paths = get_paths(input_folder='../Data/books')
	book2stats = {}

	print(f'txt_paths: {txt_paths}')
	for txt_path in txt_paths:
		# Get the filename without the path of the directory in which it's stored
		txt_filename = os.path.basename(p=txt_path)
		# Get the filename without its extension (which we will use as the key in the dictionary)
		filename, _ = os.path.splitext(p=txt_filename)
		basic_stats = get_basic_stats(txt_path=txt_path)
		book2stats[filename] = basic_stats
		print(f"Basic stats of '{filename}': {basic_stats}")
	print(f'book2stats: {book2stats}')

	# Exercise 3
	# A dictionary containing the current highest value for each statistic
	highest_stats = {
		'num_sents': float('-inf'),
		'num_tokens': float('-inf'),
		'vocab_size': float('-inf'),
		'num_chapters_or_acts': float('-inf')
	}
	stats2book_with_highest_value = {}
	# Iterate over each statistic
	for stat in highest_stats.keys():
		# Then we iterate over the books with its corresponding statistics
		for book, stats in book2stats.items():
			# Check if the stat of the current book is higher than the highest thus far
			if stats[stat] > highest_stats[stat]:
				# Update current highest value for the selected statistic
				highest_stats[stat] = stats[stat]
				# Set the current book to statistic with the highest value thus far
				stats2book_with_highest_value[stat] = book
	print(stats2book_with_highest_value)