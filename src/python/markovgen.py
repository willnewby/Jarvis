# python markovgen.py -n 1 -c 5 < dump.txt | cut -d ' ' -f 1,2,3,4,5 | sed 's/[.!?]//g'

import random, sys
from optparse import OptionParser

STOP_CHARS = ['.', '!', '?']
P_NEW_PAR = 0.1

def build_database(words, chain_len):
	database = {}
	for chain in [words[i:i+(chain_len)] for i in range(len(words) - (chain_len - 1))]:
		key = tuple(chain[:-1])
		if key not in database:
			database[key] = []
		database[key].append(chain[-1])
	return database

def generate_markov_text(database, num_words, chain_len, seed):
	if seed:
		matches = filter(lambda key: seed.lower() in key or seed.capitalize() in key, database.keys())
		if len(matches) == 0:
			raise Exception("Seed not present in corpus")
		current_phrase = random.choice(matches)
	else:
		current_phrase = random.choice(database.keys())
	gen_words = []
	for i in range(num_words):
		gen_words.append(current_phrase[0])
		if gen_words[-1][-1] in STOP_CHARS:
# randomly begin a new paragraph w/ probability P_NEW_PAR
			if random.random() <= P_NEW_PAR:
				gen_words.append('\n\n')
		current_phrase = tuple(list(current_phrase[1:]) + [random.choice(database[current_phrase])])
	while not any([c in gen_words[-1] for c in STOP_CHARS]):
		gen_words.append(current_phrase[0])
		current_phrase = tuple(list(current_phrase[1:]) + [random.choice(database[current_phrase])])
	return ' '.join(gen_words)

def main():
	parser = OptionParser()
	parser.set_defaults(num_words=None, chain_len=3, seed=None)
	parser.add_option("-n", "--num_words", dest="num_words", type="int")
	parser.add_option("-c", "--chain_len", dest="chain_len", type="int")
	parser.add_option("-s", "--seed", dest="seed")
	(options, args) = parser.parse_args()
	if options.num_words == None:
		options.num_words = random.randint(25,125)

	words = sys.stdin.read().split()
	database = build_database(words, options.chain_len)
	text = generate_markov_text(database, options.num_words, options.chain_len, options.seed)
	print text

if __name__ == '__main__':
	main()
