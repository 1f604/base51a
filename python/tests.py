import unittest, itertools
from base53a import _b53a_remap, b53_generate_random_Base53ID, Base53ID, ValidationResult, char_to_num, num_to_char, _b53a_internal_get_checksum, b53_generate_next_Base53ID

import string
from collections import defaultdict
illegal_characters = set("O91IlWwmd")
illegal_pairs = set(["VV", "vv", "rn", "nn"])
legal_characters = set(string.ascii_letters + string.digits) - illegal_characters

assert char_to_num == {'0': 0, '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7, 'A': 8, 'B': 9, 'C': 10, 'D': 11, 'E': 12, 'F': 13, 'G': 14, 'H': 15, 'J': 16, 'K': 17, 'L': 18, 'M': 19, 'N': 20, 'P': 21, 'Q': 22, 'R': 23, 'S': 24, 'T': 25, 'U': 26, 'V': 27, 'X': 28, 'Y': 29, 'Z': 30, 'a': 31, 'b': 32, 'c': 33, 'e': 34, 'f': 35, 'g': 36, 'h': 37, 'i': 38, 'j': 39, 'k': 40, 'n': 41, 'o': 42, 'p': 43, 'q': 44, 'r': 45, 's': 46, 't': 47, 'u': 48, 'v': 49, 'x': 50, 'y': 51, 'z': 52}
assert num_to_char == {0: '0', 1: '2', 2: '3', 3: '4', 4: '5', 5: '6', 6: '7', 7: '8', 8: 'A', 9: 'B', 10: 'C', 11: 'D', 12: 'E', 13: 'F', 14: 'G', 15: 'H', 16: 'J', 17: 'K', 18: 'L', 19: 'M', 20: 'N', 21: 'P', 22: 'Q', 23: 'R', 24: 'S', 25: 'T', 26: 'U', 27: 'V', 28: 'X', 29: 'Y', 30: 'Z', 31: 'a', 32: 'b', 33: 'c', 34: 'e', 35: 'f', 36: 'g', 37: 'h', 38: 'i', 39: 'j', 40: 'k', 41: 'n', 42: 'o', 43: 'p', 44: 'q', 45: 'r', 46: 's', 47: 't', 48: 'u', 49: 'v', 50: 'x', 51: 'y', 52: 'z'}


class TestBase53IDValidation(unittest.TestCase):
	def expect(self, input_string, input_checksum, expected_result): # helper method
		# one character test
		with self.assertRaises(AssertionError) as cm:
			Base53ID(string_without_checksum=input_string, checksum_char=input_checksum)
		self.assertEqual(cm.exception.args[0], expected_result)

	def test_remapping_impl(self):
		result = _b53a_remap("aa9a999mOoOO0O909g090Oadsfd")
		self.assertEqual(result,'aagagggm0o0000g0gg0g00adsfd')

	def test_remapping_flag(self):
		self.assertRaises(AssertionError, Base53ID, string_without_checksum='avO', checksum_char='4')
		try:
			Base53ID(string_without_checksum='avO', checksum_char='4', remap=True)
		except Exception as e:
			self.fail("Unexpected exception", e)

	def test_length_check(self):
		self.expect('', '4', ValidationResult(False, 'String too short'))
		self.expect('a'*52, '4', ValidationResult(False, 'String too long'))
		Base53ID(string_without_checksum='a'*51, checksum_char='a')

	def test_fails_illegal_characters(self):
		for ic in illegal_characters:
			# one character test
			self.expect(ic, '4', ValidationResult(False, f'Error: illegal character: {ic}'))
			self.expect('4', ic, ValidationResult(False, f'Error: illegal character: {ic}'))
			self.expect('af4876', ic, ValidationResult(False, f'Error: illegal character: {ic}'))

			# two character test
			self.expect(ic + "a", '4', ValidationResult(False, f'Error: illegal character: {ic}'))
			self.expect("a" + ic, '4', ValidationResult(False, f'Error: illegal character: {ic}'))

			# three character test
			self.expect(ic + "ab", '4', ValidationResult(False, f'Error: illegal character: {ic}'))
			self.expect("a" + ic + "b", '4', ValidationResult(False, f'Error: illegal character: {ic}'))
			self.expect("ab" + ic, '4', ValidationResult(False, f'Error: illegal character: {ic}'))

	def test_fails_illegal_pairs(self):
		for ip in illegal_pairs:
			# 0 character test
			self.expect(ip, '4', ValidationResult(False, f'Error: illegal pair: {ip}'))
			self.expect(ip[0], ip[1], ValidationResult(False, f'Error: illegal pair: {ip}'))

			# 1 character test
			self.expect(ip+"a", '4', ValidationResult(False, f'Error: illegal pair: {ip}'))
			self.expect("a"+ip, '4', ValidationResult(False, f'Error: illegal pair: {ip}'))
			self.expect("a"+ip[0], ip[1], ValidationResult(False, f'Error: illegal pair: {ip}'))

			# 2 character test
			self.expect(ip+"ab", '4', ValidationResult(False, f'Error: illegal pair: {ip}'))
			self.expect("a"+ip+"b", '4', ValidationResult(False, f'Error: illegal pair: {ip}'))
			self.expect("ab"+ip, '4', ValidationResult(False, f'Error: illegal pair: {ip}'))
			self.expect("ab"+ip[0], ip[1], ValidationResult(False, f'Error: illegal pair: {ip}'))

	def test_checksum_validation(self):
		# check no error on correct checksum
		for n in range(2,4): # check all strings up to length 2
			for seq in itertools.product(legal_characters, repeat=n):
				seq = ''.join(seq)
				if any(ip in seq for ip in illegal_pairs):
					continue
				# check if it errors or not
				checksum = _b53a_internal_get_checksum(seq[:-1])
				try:
					Base53ID(string_without_checksum=seq[:-1], checksum_char=seq[-1])
				except Exception as e:
					self.assertNotEqual(checksum, seq[-1], (e, seq))
				else:
					self.assertEqual(checksum, seq[-1])


class TestBase53GenerateRandom(unittest.TestCase):
	def test_generates_all_legal_chars(self):
		for n in range(1,5):
			seen = defaultdict(bool)
			for _ in range(2000):
				rs = b53_generate_random_Base53ID(n)
				for c in str(rs):
					seen[c] = True
			for c in legal_characters:
				self.assertTrue(seen[c], (c, seen))
			
	def test_generates_all_legal_strings(self):
		# check it generates all legal 2-character strings
		n = 2
		results = set()
		for i in range(50000): # should have less than 0.001% chance of failing
			rs = b53_generate_random_Base53ID(n)
			results.add(rs)
		self.assertEqual(len(results), 53 * 53 - 4*2) # only 'VV' 'vv' 'rn' and 'nn' are disallowed, but these pairs can occur in two places
			
	def test_generates_different_strings(self):
		results = set()
		for _ in range(100):
			rs = b53_generate_random_Base53ID(8)
			results.add(rs)
		self.assertEqual(len(results), 100) # should never get repeats.


class TestBase53GenerateNext(unittest.TestCase):
	def test_check_number_of_strings(self):
		count = {
			1: 53,
			2: 2805 - 4, # this is the number of valid strings after removing those with illegal pairs
			3: 148457 - 208,
		}
		for i in range(1,4): # all sequences up to length 3
			id = Base53ID(string_without_checksum='0'*i, checksum_char='0')
			results = set([str(id)])
			num_strings = count[i] # subtract the number of illegal pairs
			for x in range(1, num_strings):
				id = b53_generate_next_Base53ID(id)
				sid = str(id)
				self.assertEqual(len(sid), i+1, (id, sid, x))
				results.add(sid)
			self.assertEqual(len(results), num_strings) # should never get repeats.

