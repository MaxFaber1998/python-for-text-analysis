import os, nltk
from utils import get_paths, get_basic_stats


if __name__ == '__main__':
	# This resource is required in order to execute this script
	nltk.download('punkt')
	# Exercise 1
	# Get all paths of txt files in the selected directory
	txt_paths = get_paths(input_folder='../Data/books')

	print(f'txt_paths: {txt_paths}')
	# End of exercise 1
	# Exercise 2
	book2stats = {}
	for txt_path in txt_paths:
		# Get the filename without the path of the directory in which it's stored
		txt_filename = os.path.basename(p=txt_path)
		# Get the filename without its extension (which we will use as the key in the dictionary)
		filename, _ = os.path.splitext(p=txt_filename)
		basic_stats = get_basic_stats(txt_path=txt_path)
		book2stats[filename] = basic_stats
		print(f"Basic stats of '{filename}': {basic_stats}")
	print(f'book2stats: {book2stats}')
	# End of exercise 2

	# Exercise 3
	# A dictionary containing the current highest value for each statistic
	highest_stats = {
		'num_sents': float('-inf'), # Negative infinity comes in handy as nothing can be smaller than this value
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
	print(f'stats2book_with_highest_value: {stats2book_with_highest_value}')
	# End of exercise 3

	# Exercise 4
	for book, stats in book2stats.items():
		with open(f'top_30_{book}.txt', mode='w', encoding='utf-8') as outfile:
			for token in stats['top_30_tokens']:
				# Write the top 30 tokens to a file (one token per line)
				outfile.writelines(f'{token}\n')
	# End of exercise 4
