+++
title = "WPI CTF: John Cena 🎺🎺🎺🎺"
date = 2020-04-18T23:16:21+10:00
lastmod = 2020-04-20T22:19:21+10:00
tags = [ "WPICTF2020"]
categories = [ "CTF"]
imgs = []
cover = "/img/john-cena.png"  # image show on top
readingTime = true  # show reading time after article date
toc = true
comments = true
justify = false  # text-align: justify;
single = false  # display as a single page, hide navigation on bottom, like as about page.
license = ""  # CC License
draft = false
+++

# Challenge Description

>You can't see him, but can you see the flag?
>
>[http://us-east-1.linodeobjects.com/wpictf-challenge-files/braille.png](http://us-east-1.linodeobjects.com/wpictf-challenge-files/braille.png)
>
>made by: ollien, with a little help from acurless



# Braille

The first clue for this challenge is a URL to a PNG image. This is how it looks:

![braille](/img/john-cena-braille.png)

Apparently, it's something written in Braille. We need to do an "OCR" of this picture first, and then decode it.

According to [Wikipedia](https://en.wikipedia.org/wiki/Braille), 6-dot Braille patterns are coded in Unicode as this:

|   | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | A | B | C | D | E | F |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| U+280x |⠀ | ⠁ | ⠂ | ⠃ | ⠄ | ⠅ | ⠆ | ⠇ | ⠈ | ⠉ | ⠊ | ⠋ | ⠌ | ⠍ | ⠎ | ⠏ | 
| U+281x |⠐ | ⠑ | ⠒ | ⠓ | ⠔ | ⠕ | ⠖ | ⠗ | ⠘ | ⠙ | ⠚ | ⠛ | ⠜ | ⠝ | ⠞ | ⠟ | 
| U+282x |⠠ | ⠡ | ⠢ | ⠣ | ⠤ | ⠥ | ⠦ | ⠧ | ⠨ | ⠩ | ⠪ | ⠫ | ⠬ | ⠭ | ⠮ | ⠯ | 
| U+283x |⠰ | ⠱ | ⠲ | ⠳ | ⠴ | ⠵ | ⠶ | ⠷ | ⠸ | ⠹ | ⠺ | ⠻ | ⠼ | ⠽ | ⠾ | ⠿ | 

So these characters are like dot-represeted binary numbers, and their Unicode values are their binary values plus 0x2800.

To extract the characters, I wrote some Python code. The way I determine the borders of each character is simply assume every character has the same width and height, and divide the picture evenly. Thus you need to crop off some black margin of the picture if you want to use this code. You can employ a more sophisticated algorithm of course.

```python
import numpy as np
from PIL import Image

def greyscale_to_braille(mat):
	ver1 = round(mat.shape[0] / 3.0)
	ver2 = round(mat.shape[0] * 2 / 3.0)
	hor = round(mat.shape[1] / 2.0)
	dots = [
	mat[:ver1, :hor],
	mat[ver1:ver2, :hor],
	mat[ver2:mat.shape[0] - 1, :hor],
	mat[:ver1, hor:mat.shape[1] - 1],
	mat[ver1:ver2, hor:mat.shape[1] - 1],
	mat[ver2:mat.shape[0] - 1, hor:mat.shape[1] - 1]]

	weight = np.array([1, 2, 4, 8, 16, 32])

	digits = np.array(list(map(lambda x: x.sum() > 2000, dots)))
	offset = digits.dot(weight)

	return chr(0x2800 + offset)

def char_at(bmp, row, col):
	# Uncomment lines below if you want to check the border of each character is correct.
	# It generates a picture file for every cropped character named after the row and col.
	# img.crop((round(col * char_width), 
	# 		round(row * char_height), 
	# 		round((col + 1) * char_width), 
	# 		round((row + 1) * char_height))).save('braille-img/r%dc%d.png' % (row, col))
	mat = bmp[round(row * char_height): round((row + 1) * char_height), 
			round(col * char_width): round((col + 1) * char_width)]
	return greyscale_to_braille(mat)


img = Image.open('braille.png').convert('LA')
bmp = np.array(img)[:,:,0]
char_height = bmp.shape[0] / 57.0
char_width = bmp.shape[1] / 33.0


braille_chars = []

for row in range(57):
	for col in range(33):
		braille_chars.append(char_at(bmp, row, col))
	braille_chars.append('\n')

f = open('braille.txt', 'w')
f.write(''.join(braille_chars))
f.close()
```

After running this code, the `braille.txt` contains:

```
⠼⠛⠋⠼⠙⠼⠑⠼⠙⠉⠼⠙⠼⠋⠼⠚⠼⠃⠼⠚⠼⠁⠼⠚⠼⠁⠼⠚⠼⠚⠼⠚⠼
⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠃
⠼⠚⠼⠚⠼⠉⠑⠼⠚⠼⠚⠼⠚⠼⠁⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠓⠼⠚⠼⠚
⠼⠚⠼⠙⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠙⠼⠚⠼⠚⠼
⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠑⠼⠚⠼⠚⠼⠚⠼
⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚
⠼⠚⠼⠚⠼⠚⠼⠙⠼⠚⠼⠚⠼⠚⠼⠉⠼⠓⠼⠚⠼⠚⠼⠚⠼⠁⠼⠚⠼⠚⠼⠙⠼
⠚⠼⠚⠼⠚⠼⠚⠼⠙⠼⠚⠼⠚⠼⠚⠼⠉⠼⠚⠼⠚⠼⠚⠼⠁⠼⠚⠼⠚⠼⠚⠼⠚
⠼⠚⠼⠚⠼⠚⠼⠛⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠓⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼
⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠓⠼⠚⠼⠚⠼⠚⠼⠙⠼⠚⠼⠚
⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠓⠼⠚⠼⠚⠼⠚⠼⠙⠼⠚⠼⠚⠼
⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠙⠼⠊⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚
⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠙⠼⠊⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼
⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠁⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚
⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼
⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠃⠼⠓⠼⠚⠼⠁⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠃
⠋⠼⠚⠼⠁⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠃⠑⠃⠼⠙⠼⠚⠼⠚⠼⠙⠼⠚⠼⠚⠼
⠚⠼⠉⠼⠁⠉⠼⠊⠼⠋⠼⠛⠼⠓⠃⠼⠁⠼⠙⠼⠚⠑⠼⠓⠼⠉⠉⠼⠃⠼⠉⠼⠁
⠼⠋⠼⠛⠼⠓⠼⠊⠼⠁⠼⠙⠼⠚⠑⠋⠋⠉⠼⠁⠼⠓⠼⠉⠋⠼⠊⠼⠁⠼⠑⠼⠛
⠼⠑⠑⠑⠃⠁⠼⠁⠼⠑⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠋⠼⠚⠼⠑⠃⠼⠓⠼
⠉⠉⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠉⠼⠁⠋⠋⠼⠚⠋⠼⠚⠼⠑⠼⠚⠼⠚⠼⠃
⠼⠋⠼⠁⠋⠼⠁⠼⠓⠼⠙⠁⠼⠉⠃⠼⠚⠼⠉⠼⠙⠼⠃⠼⠚⠼⠚⠼⠙⠼⠛⠼⠚
⠁⠼⠚⠼⠚⠼⠙⠼⠃⠼⠚⠼⠉⠼⠃⠑⠼⠚⠼⠙⠼⠉⠼⠃⠼⠙⠼⠁⠼⠙⠼⠙⠼
⠉⠼⠁⠼⠚⠼⠙⠼⠙⠉⠼⠚⠼⠚⠼⠃⠑⠼⠛⠼⠉⠼⠋⠼⠓⠼⠛⠼⠉⠼⠛⠼⠙
⠼⠛⠼⠃⠼⠛⠼⠙⠼⠋⠼⠁⠼⠋⠼⠃⠼⠚⠼⠚⠼⠃⠑⠼⠛⠼⠙⠼⠋⠼⠑⠼⠛
⠼⠓⠼⠛⠼⠙⠼⠚⠼⠚⠼⠃⠑⠼⠋⠼⠙⠼⠋⠼⠁⠼⠛⠼⠙⠼⠋⠼⠁⠼⠚⠼⠚
⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼
⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚
⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼
⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚
⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼
⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚
⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼
⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠃⠼⠚⠼⠚⠼
⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠁⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠛⠼⠚⠼⠚⠼⠚
⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠓⠼⠚⠼⠚⠼⠚⠼⠙⠼
⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠓⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚
⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠉⠼⠉⠼⠚⠼⠚⠼⠚⠼⠚⠼
⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚
⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠁⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼
⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚
⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠁⠼⠁⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼
⠚⠼⠁⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠉⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚
⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠃⠼⠙⠼⠚⠼⠚⠼⠙⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚
⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠃⠼⠙⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚
⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠁⠼⠑⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼
⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚
⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠙⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼
⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚
⠼⠚⠼⠚⠼⠚⠼⠚⠼⠁⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠉⠼⠚⠼⠚⠼⠚⠼
⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚
⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼
⠚⠼⠚⠉⠼⠊⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼
⠚⠼⠁⠼⠛⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚
⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼
⠚⠼⠁⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚
⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠼⠚⠀⠀⠀
```

# Decode

As I read from Wikipedia, many different Latin alphabets of different languages are encoded into this set of Braille characters, and even non-Latin writing systems. Since this CTF activity is English based, I'll try English first.

Googling 'braille to english' and I found a website: [dcode.fr](https://www.dcode.fr/braille-alphabet) (This website is awesome. It can even decode Sheikah symbols from Legend of Zelda: Breath of the Wild). So I pasted extracted Braille above, but doesn't seem right.

![decode1](/img/john-cena-decode1.png)

I noticed that in this result about half of the lines end with an undecoded ⠼ character. Can it be this character should be decoded with the following character, but saw a line wrap instead? It's worth a try to decode without LF characters.

![decode2](/img/john-cena-decode2.png)

This time it seems to make much better sense. These are hexadecimal numbers. So let's try further decoding this.

First step is always to check if it contains printable characters.

![decode3](/img/john-cena-decode3.png)

It shows 'ELF' at the head of this byte strings. Very good chance it's a executable file on Linux! Definitely I should save this to a file and try running it.

```python

f = open('braille.bin', 'wb')
f.write(a.to_bytes(3840//8, 'big'))
f.close()

```

```bash
chmod +x braille.bin
./braille.bin
```

![flag](/img/john-cena-flag.png)

That's the flag!
