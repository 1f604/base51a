# base51a - a visually unambiguous alphabet for URLs

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
*    m, rn, and nn => ban both m and n
*    d and cl => ban both c and d

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

So, 11 characters are banned and 2 pairings are banned. Out of the 62 characters therefore we only have 51 characters. 

It is important to note the pairings of characters that are banned.

TODOs: 
- add validation function
- add generation function
- Add a "checksum" character at the end, or else specify algorithm to ensure a Hamming distance.

