import string, random

illegal_characters = set("O91IlWwmncd")
illegal_pairs = set(["VV", "vv"])
legal_chars = set(string.ascii_letters + string.digits) - illegal_characters
alphabet = list(legal_chars)
alphabet_without_v = list(legal_chars - set(['v']))
alphabet_without_V = list(legal_chars - set(['V']))

assert len(alphabet) == len(set(alphabet)), "alphabet contains duplicates"
assert len(alphabet) == 51, "size of alphabet is not 51"
remapping_table = {'O':'0', '9':'g'}

illegal_pairs = set(["VV", "vv"])

def b51a_remap(s:str):
	ls = list(s)
	for i in range(len(ls)):
		if ls[i] in remapping_table:
			ls[i] = remapping_table[ls[i]]
	return ''.join(ls)

def b51a_validate(s:str):
	# check for illegal characters
	for c in s:
		if c not in alphabet:
			return "Error: illegal character: "+c
	# check for illegal pairs
	for ip in illegal_pairs:
		if ip in s:
			return "Error: illegal pair: "+ip
	return True

def b51a_generate_random(n:int):
	# important: verify that different output is returned every time this program is run
	# generate a random string from the alphabet
	# if it contains an illegal pair, try again
	prev_char = ''
	result = []
	for i in range(n):
		if prev_char == 'v':
			choices = alphabet_without_v
		elif prev_char == 'V':
			choices = alphabet_without_V
		else:
			choices = alphabet
		prev_char = random.choice(choices)
		result.append(prev_char)
	return ''.join(result)
		
		
		
