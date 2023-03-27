# base53a - a visually unambiguous alphabet for URLs

## How to use

### Python

#### How to actually use it

```
$ cd base53a/
$ ls
LICENSE  python  README.md
$ cd python
$ python
>>> from base53a import Base53ID, b53_generate_random_Base53ID, b53_generate_next_Base53ID
>>> b53_generate_random_Base53ID(5)
Base53ID(string_without_checksum='4gG6g', checksum_char='F')
>>> b53_generate_next_Base53ID(Base53ID(string_without_checksum='4gG6g', checksum_char='F'))
Base53ID(string_without_checksum='4gG6h', checksum_char='8')
```

#### How to run the tests
```
$ cd base53a/
$ ls
LICENSE  python  README.md
$ cd python
$ python -m unittest 
..........
----------------------------------------------------------------------
Ran 10 tests in 3.757s

OK
```

#### How to type check

```
$ cd base53a
$ python3 -m venv venv
$ . venv/bin/activate
(venv) $ pip install mypy
(venv) $ mypy .
```

## Background

I was creating a URL shortener and of course, short URLs are meant to be read and typed by humans. This creates a problem when characters are visually similar, such as O and 0.

Although this alphabet was designed for URLs, it can be used for other purposes.

For more background details see: https://1f604.blogspot.com/2023/03/introducing-base52a-visually.html

## Scheme

Dealing with visually ambiguous character groups:

*    0 and O => choose 0 as canonical
*    9 and g => choose g as canonical
*    1, I, and l => ban 1, I, and l
*    W and VV => ban both W and VV
*    w and vv => ban both w and vv
*    m, rn, and nn => ban m, rn, and nn
*    d and cl => ban d (l is already banned)

So the following characters are banned from the alphabet:

*    O => automatically remapped to 0
*    9 => automatically remapped to g
*    1 => Error: Invalid ID
*    I => Error: Invalid ID
*    l => Error: Invalid ID
*    W => Error: Invalid ID
*    w => Error: Invalid ID
*    m => Error: Invalid ID
*    n => Error: Invalid ID
*    c => Error: Invalid ID
*    d => Error: Invalid ID
*    VV => Error: Invalid ID
*    vv => Error: Invalid ID
*    rn => Error: Invalid ID
*    nn => Error: Invalid ID

So, 9 characters are banned and 4 pairings are banned. Out of the 62 characters therefore we only have 53 characters. 

It is important to note the pairings of characters that are banned.

# How the checksum works

The checksum is a generalization of the ISBN-10 checksum (one could perhaps call it the ISBN-n checksum). The scheme is as follows:

Choose any prime p. Our alphabet will consist of p symbols which map to the set of integers from 0 to p-1. For example, if we choose p to be 17, then our alphabet will be {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, a, b, c, d, e, f, g} where 0 maps to 0 and g maps to 16.

The maximum valid length of a string (not including the checksum character) in this scheme shall be p-2.

Given a string of length n where n is less than or equal to p-2 consisting of symbols from the alphabet, we want to compute a single-character error-detection checksum for the string. Denote characters in the string as x_i such that x_1 is the first character of the string, x_2 is the second character and x_n is the last character (n is the length of the string). Denote the checksum character as c.

The checksum character c shall be computed as the sum of products of multipliers with the characters of the string mod p, as follows:

c = sum mod p

Where sum = (p-2) * x_1 + (p-3) * x_2 + ... (p-1-n) * x_n

Where:

    n is the length of the string
    n is less than or equal to p-2
    the multipliers are (p-2), (p-3), ...

As c is a number modulo p, its minimum value is 0 and maximum value is p-1, which means it can be represented using the alphabet.

For example, for p=17 the checksum will be computed as:

c = 15 * x_1 + 14 * x_2 + ... + (p-1-n) * x_n mod 17

Where n is less than or equal to 15.

The verification of a string will simply consist of recomputing the checksum of the string without the checksum character (the checksum character will be the last character in the string because we append the checksum character to the end of the string) and seeing if it matches the checksum character.

We want to be able to detect 2 types of errors:

    Single character typo, where a single character is changed
    Adjacent transposition, where two adjacent characters are swapped resulting in a different string.

The checksum character will be appended to the end of the string, therefore an adjacent transposition could swap the checksum character with the character next to it. We want to be able to detect this.

Here is my proof:

Lemma: A change in the string will go undetected iff the original and new strings have the same checksum, which means that the sums are equal mod p.

Therefore: A change will only go undetected iff the sum changes by a multiple of p.

## Property 1. This checksum detects all single-character changes 

Proof:

Since none of the multipliers are a multiple of p (they are all smaller than p) this means that in order for a single character change to produce a change by a multiple of p, it has to be a character that changes by a multiple of p. But as the characters are in the range 0 to p-1, it is impossible for them to change by a multiple of p (except for 0 * p, which isn't a change).

Therefore, it is impossible for a single-character change to go undetected.

## Property 2. This checksum detects all adjacent transpositions in the string excluding the checksum character 

Proof:

Transposition of two adjacent characters will go undetected iff the resulting sum is equal to the original sum plus a multiple of p.

Let r be the multiplier of x, x and y be the adjacent characters (where x precedes y in the string), and k be any integer.

The other characters in the string remain in their positions unchanged, therefore their contribution to the sum remains unchanged therefore the sum only changes if the sum of the products involving the two transposed characters changes.

In order for the change to go undetected the sum of the products involving the two transposed characters must remain unchanged mod p:

r * x + (r-1) * y = r * y + (r-1) * x + p * k where k is any integer

rx + ry - y = ry + rx - x + pk

rx - rx - y = ry - ry - x + pk

-y = -x + pk

x = y + pk

Thus, the only time when a transposition results in an unchanged checksum is when x is equal to y plus a multiple of p. This is impossible if k is nonzero because the characters are in the range 0 to p-1. But if k is 0 then x equals y and there is no change in the string.

Therefore the code detects all adjacent transpositions excluding the checksum character.

## Property 3. This checksum detects the transposition between the checksum character and the last character 

Denote the checksum character as c.

Denote the length of the string as n where n is less than or equal to p-2.

Denote the last character (not the checksum) as x_n.

Denote the sum not including the last character (p-2) * x_1 + (p-3) * x_2 + ... + x_{n-1} as s.

Denote the last multiplier (the multiplier for x_n) as r.

Then the following equation holds:

s + r * x_n = c + p * k where k is some integer

When the last character x_n is transposed with c, the string will be valid iff:

s + r * c = x_n + p * k where k is some integer. Otherwise the string would be detected as invalid.

Therefore in order for the transposition to go undetected, the following simultaneous equations must hold:

s + r * x_n = c + p * u where u is some integer

s + r * c = x_n + p * v where v is some integer.

Now we can subtract them like this:

s - s + r * x_n - r * c = c - x_n + p(u-v)

r * x_n - r * c - c + x_n = p(u-v)

(r + 1) * x_n - (r + 1) * c = p(u-v)

(r + 1) * (x_n - c) = p(u-v)

Now, p(u-v) is a multiple of p which means (r + 1) * (x_n - c) must be a multiple of p. This means that either r+1 is a multiple of p or (x_n - c) is a multiple of p or both.

r cannot be zero because we specified that the length of the string is less than or equal to p-2 which means r cannot be less than 1. The maximum possible value of r is p-2, which means r+1 cannot be a multiple of p.

Since r+1 cannot be a multiple of p, that means x_n - c must be a multiple of p. But the characters go from 0 to p-1, so the difference between two characters must be less than p, which means that if x_n - c is a multiple of p then x_n - c = 0, which means they're the same and therefore the string is unchanged.

Therefore the last transposition cannot go undetected.