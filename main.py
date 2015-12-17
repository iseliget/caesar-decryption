from string import maketrans
import random


# Global variable
epsilon = 0.00000000001


# Load in rdata file and convert to a Python dictionary
rdata = open('lexical_database.csv')
rdata = rdata.readlines()

word_list = rdata[0]
word_list = word_list.split(',')
word_list = [x[1:-1] for x in word_list]
del word_list[0]
word_list[-1] = 'zymurgy'

frequency_list = rdata[1]
frequency_list = frequency_list.split(',')
del frequency_list[0]
frequency_list[-1] = '0.0000000319756700559721'
frequency_list = [float(x) for x in frequency_list]

frequency_table = {}
for i in range(0,len(word_list)):
	frequency_table[word_list[i]] = frequency_list[i]

def caesar_shift(input_string,shift=3):
	'''
	This function encrypt the given string by shifting
	all the letters by given length. Default value is 3.
	'''

	trans_domain = 'abcdefghijklmnopqrstuvwxyz'
	trans_range = ''

	for i in range(0,26):
		trans_range = trans_range + trans_domain[(i+shift)%26]

	trans_domain = trans_domain + trans_domain.upper()
	trans_range = trans_range + trans_range.upper() # Deal with upper case letters
	trans_function = maketrans(trans_domain,trans_range)

	output_string = input_string.translate(trans_function)

	return output_string

def substitution_encrypt(input_string):
	'''
	Generalize the former function.
	This function generates a random bijection between
	sets of all letters. Then it encrypts the input string
	using the bijection.
	'''

	trans_domain = 'abcdefghijklmnopqrstuvwxyz'
	trans_range = 'abcdefghijklmnopqrstuvwxyz'

	while trans_range == trans_domain: # Make sure we don't generate the identity function
		trans_range = random.sample(trans_domain,26)
		trans_range = ''.join(trans_range)

	trans_domain = trans_domain + trans_domain.upper()
	trans_range = trans_range + trans_range.upper() # Deal with upper case letters
	trans_function = maketrans(trans_domain,trans_range)

	output_string = input_string.translate(trans_function)

	return output_string

def score(input_string):
	'''
	Return the probability of a string. Defined as sum of log(Pr).
	If a word is in the frequency_table, then simply return the probability. 
	If not, then return a very small pre-specified number: epsilon.
	'''

	input_string = input_string.lower() 
	list_of_words = input_string.split(' ')
	score = 0

	for word in list_of_words:
		if word in frequency_table:
			score = score + frequency_table[word]
		else:
			score = score + epsilon

	return score

def caesar_decrypt(input_string):
	current_score = score(input_string)
	num_of_shift = 0

	for c in range(0,26):
		print 'Trying shift = ' + str(c) + '\t',
		print caesar_shift(input_string,c)
		if score(caesar_shift(input_string,c))>current_score:
			current_score = score(caesar_shift(input_string,c))
			num_of_shift = c

	return caesar_shift(input_string,num_of_shift)

def greedy_decrypt(input_string):
	pass

def main():
	input_string = raw_input('Enter the string you want to encrypt:')
	shift = input('Enter shift:')
	print ('------Encrypting------')
	print 'Message: ' + input_string
	print 'Encrypted Message: ' + caesar_shift(input_string,shift)
	print ('------Decrypting------')
	print caesar_decrypt(caesar_shift(input_string,shift))

if __name__ == '__main__':
	main()