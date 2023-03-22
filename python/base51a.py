alphabet = '02345678' + 'abefghijkopqrstuvxyz' + 'ABCDEFGHJKLMNPQRSTUVXYZ'
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

