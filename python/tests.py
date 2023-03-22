import unittest
from base53a import b53a_validate, b53a_remap, b53a_generate_random

import string
from collections import defaultdict
illegal_characters = set("O91IlWwmd")
illegal_pairs = set(["VV", "vv", "rn", "nn"])
legal_characters = set(string.ascii_letters + string.digits) - illegal_characters

class Testbase53aValidationMethod(unittest.TestCase):
	def test_fails_illegal_characters(self):
		for ic in illegal_characters:
			# one character test
			result = b53a_validate(ic)
			self.assertEqual(result, "Error: illegal character: "+ic)

			# two character test
			result = b53a_validate(ic+"a")
			self.assertEqual(result, "Error: illegal character: "+ic)
			result = b53a_validate("a"+ic)
			self.assertEqual(result, "Error: illegal character: "+ic)

			# three character test
			result = b53a_validate(ic+"ab")
			self.assertEqual(result, "Error: illegal character: "+ic)
			result = b53a_validate("a"+ic+"b")
			self.assertEqual(result, "Error: illegal character: "+ic)
			result = b53a_validate("ab"+ic)
			self.assertEqual(result, "Error: illegal character: "+ic)
			
	def test_fails_illegal_pairs(self):
		for ip in illegal_pairs:
			# 0 character test
			result = b53a_validate(ip)
			self.assertEqual(result, "Error: illegal pair: "+ip)
			
			# 1 character test
			result = b53a_validate("a" + ip)
			self.assertEqual(result, "Error: illegal pair: "+ip)
			result = b53a_validate(ip + "a")
			self.assertEqual(result, "Error: illegal pair: "+ip)
			
			# 2 character test
			result = b53a_validate("aa" + ip)
			self.assertEqual(result, "Error: illegal pair: "+ip)
			result = b53a_validate("a" + ip + "a")
			self.assertEqual(result, "Error: illegal pair: "+ip)
			result = b53a_validate(ip + "aa")
			self.assertEqual(result, "Error: illegal pair: "+ip)

class Testbase53aRemapMethod(unittest.TestCase):
	def test_remapping(self):
		result = b53a_remap("aa9a999mOoOO0O909g090Oadsfd")
		self.assertEqual(result,'aagagggm0o0000g0gg0g00adsfd')

class Testbase53aGenerateMethod(unittest.TestCase):
	def test_generates_no_illegals(self):
		for n in range(5): # check zero length strings too!
			for _ in range(20000):
				rs = b53a_generate_random(n)
				self.assertEqual(b53a_validate(rs), True)
	
	def test_generates_all_legal_chars(self):
		for n in range(1,5):
			seen = defaultdict(bool)
			for _ in range(2000):
				rs = b53a_generate_random(n)
				for c in rs:
					seen[c] = True
			for c in legal_characters:
				self.assertTrue(seen[c], (c, seen))
			
	def test_generates_all_legal_strings(self):
		# check it generates all legal 2-character strings
		n = 2
		results = set()
		for i in range(50000): # should have less than 0.001% chance of failing
			rs = b53a_generate_random(n)
			results.add(rs)
		self.assertEqual(len(results), 53 * 53 - 4) # only 'VV' 'vv' 'rn' and 'nn' are disallowed
			
	def test_generates_different_strings(self):
		results = set()
		for _ in range(100):
			rs = b53a_generate_random(8)
			results.add(rs)
		self.assertEqual(len(results), 100) # should never get repeats.
