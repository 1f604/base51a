import unittest
from base51a import b51a_validate, b51a_remap

import string
illegal_characters = set("O91IlWwmncd")
illegal_pairs = set(["VV", "vv"])
legal_characters = set(string.ascii_letters + string.digits) - illegal_characters

class TestBase51aValidationMethod(unittest.TestCase):
	def test_fails_illegal_characters(self):
		for ic in illegal_characters:
			# one character test
			result = b51a_validate(ic)
			self.assertEqual(result, "Error: illegal character: "+ic)

			# two character test
			result = b51a_validate(ic+"a")
			self.assertEqual(result, "Error: illegal character: "+ic)
			result = b51a_validate("a"+ic)
			self.assertEqual(result, "Error: illegal character: "+ic)

			# three character test
			result = b51a_validate(ic+"ab")
			self.assertEqual(result, "Error: illegal character: "+ic)
			result = b51a_validate("a"+ic+"b")
			self.assertEqual(result, "Error: illegal character: "+ic)
			result = b51a_validate("ab"+ic)
			self.assertEqual(result, "Error: illegal character: "+ic)
			
	def test_fails_illegal_pairs(self):
		for ip in illegal_pairs:
			# 0 character test
			result = b51a_validate(ip)
			self.assertEqual(result, "Error: illegal pair: "+ip)
			
			# 1 character test
			result = b51a_validate("a" + ip)
			self.assertEqual(result, "Error: illegal pair: "+ip)
			result = b51a_validate(ip + "a")
			self.assertEqual(result, "Error: illegal pair: "+ip)
			
			# 2 character test
			result = b51a_validate("aa" + ip)
			self.assertEqual(result, "Error: illegal pair: "+ip)
			result = b51a_validate("a" + ip + "a")
			self.assertEqual(result, "Error: illegal pair: "+ip)
			result = b51a_validate(ip + "aa")
			self.assertEqual(result, "Error: illegal pair: "+ip)


class TestBase51aRemapMethod(unittest.TestCase):
	def test_remapping(self):
		result = b51a_remap("aa9a999mOoOO0O909g090Oadsfd")
		self.assertEqual(result,'aagagggm0o0000g0gg0g00adsfd')






			
