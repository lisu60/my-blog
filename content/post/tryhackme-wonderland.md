+++
title = "Wonderland - TryHackMe Box Walkthrough"
date = 2020-06-13T01:29:18+10:00
lastmod = 2020-06-13T01:29:18+10:00
tags = ["TryHackMe", "Escalation"]
categories = ["CTF"]
imgs = []
cover = "/img/wonderland/wonderland0.png"  # image show on top
readingTime = true  # show reading time after article date
toc = true
comments = true
justify = false  # text-align: justify;
single = true  # display as a single page, hide navigation on bottom, like as about page.
license = ""  # CC License
+++

Room URL: [https://tryhackme.com/room/wonderland](https://tryhackme.com/room/wonderland)

# Before you read

If you haven't tried this box yet, I'd highly recommend try it yourself first. This box is quite fun :)

Well, let's:

> Fall down the rabbit hole and enter wonderland.

# nmap

First thing, no doubt, we gotta know which ports are open on this box. This is how we do it:

```bash
nmap -sC -sV <your box ip>
```

![nmap](/img/wonderland/wonderland-nmap.png)


An ssh and a HTTP server.

First thing I would do is always to poke around the HTTP server if there is one. Not to say that we don't have any credentials for ssh at the moment.

Besides opening the website in a browser, what we can also do now is to have a look at what directories the website has. This is how I do this:

```bash
gobuster dir -u http://<your box ip> -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
```

You can of course choose another wordlist to run.

Now you can leave gobuster running in the background while you work on your browser.


# Meet White Rabbit

Put your box IP address into your browser, this is what we see:

![wonderland1](/img/wonderland/wonderland1.png)

Not quite informative looked this way. We shall check the page source.

![wonderland2](/img/wonderland/wonderland2.png)

So Mr. Rabbit here is a .jpg image. When seeing .jpg I'd always give it a try with `steghide`:

![steghide](/img/wonderland/wonderland-steghide.png)

In case you wonder the passphrase I entered: Nothing. Empty passphrase. Under this empty passphrase hides a file *hint.txt*, which says

> `follow the r a b b i t`

It seems simply repeating the title on the frontpage. But what does it mean?

Meanwhile, gobuster has found something interesting. We left it running in background, still remember?

![gobuster](/img/wonderland/wonderland-gobuster.png)

The "/img" directory we've already seen. The "/r" directory is especially curious. Let's try type it into URL and see where we go.

![r](/img/wonderland/wonderland-r.png)

It asks me to "keep going". I think I have got a theory about the previous hint... 

Follow the `r a b b i t`, huh?

# Rabbit hole


Here's what I got:

> "Would you tell me, please, which way I ought to go from here?"
>
> "That depends a good deal on where you want to get to," said the Cat.
>
> "I don't much care where--" said Alice.
>
> "Then it doesn't matter which way you go," said the Cat.

![r](/img/wonderland/wonderland-r.png)

![ra](/img/wonderland/wonderland-ra.png)

![rab](/img/wonderland/wonderland-rab.png)

![rabb](/img/wonderland/wonderland-rabb.png)

![rabbi](/img/wonderland/wonderland-rabbi.png)

![rabbit](/img/wonderland/wonderland-rabbit.png)



Now we've exhausted clues we got. What now?

Well, page sources are always worth a shot. Let's check the source of `/r/a/b/b/i/t` now.

![rabbit source](/img/wonderland/wonderland-rabbit-src.png)

It's a hidden paragraph! Such colon separated format could be a username-password pair, i.e. a login credential. 

Would it be a credential we can use to login to SSH? (Yes. Turns out it is.)

![ssh](/img/wonderland/wonderland-ssh.png)

Woowee! We are in the Wonderland now!

# Knock at White Ribbit's home

> Curiouser and curiouser!

Let's first look at the home directory.

![alice home](/img/wonderland/wonderland-alice-home.png)

![home](/img/wonderland/wonderland-home.png)

Hmm? `root.txt` is here. Well, since we can't do anything to it, let's leave it alone for now. 

And, other users' home directories are only accessible by themselves. Not cool, not cool.

Second thing caught my eyes is `walrus_and_the_carpenter.py`. We better check what in it.

P.S.: The code below is shortened for readability. You can read the complete poem [here](https://www.poetryfoundation.org/poems/43914/the-walrus-and-the-carpenter-56d222cbc80a9)

```python
import random
poem = """The sun was shining on the sea,
Shining with all his might:
He did his very best to make
The billows smooth and bright —
And this was odd, because it was
The middle of the night.

The moon was shining sulkily,
Because she thought the sun
Had got no business to be there
After the day was done —
"It’s very rude of him," she said,
"To come and spoil the fun!"

......

"I weep for you," the Walrus said.
"I deeply sympathize."
With sobs and tears he sorted out
Those of the largest size.
Holding his pocket handkerchief
Before his streaming eyes.

"O Oysters," said the Carpenter.
"You’ve had a pleasant run!
Shall we be trotting home again?"
But answer came there none —
And that was scarcely odd, because
They’d eaten every one."""

for i in range(10):
    line = random.choice(poem.split("\n"))
    print("The line was:\t", line)
```

Although it is very long, the things it does are quite simple. The core is the last few lines: If you run this script, it simply print 10 random lines from this poem to stdout.

![random lines](/img/wonderland/wonderland-random-lines.png)

One thing I would always try in priviledge escalation is `sudo`. We shall first check what command we can run with sudo:

`sudo -l`

![alice sudo](/img/wonderland/wonderland-alice-sudo.png)

Interesting! The Python script here in our home directory, we can run it as another user.

That is to say, if we can edit the script, we can run arbitary command as this user. In this case, as `rabbit`.

However, `walrus_and_the_carpenter.py` is only writable by root. Now what?

I was stuck here for a night. And something came to my mind the next morning. It was an interesting thought and thus very satisfying.

I don't wanna spoil the fun. If you are fairly farmiliar with Python you should be able to figure it out by yourself. So in case you wanna try it, I'll put some paddings below :)

.

.

.

.

.

.

.

.

.

```python
import random
```

Funny that the syntex for importing a system package and importing another .py file from project are the same. What if we create a `random.py` in the home directory (surely we have priviledge to do this)? Will the interpreter import the system one, or this one we just made?

To confirm that, I did a bit research and found [this article](https://rastating.github.io/privilege-escalation-via-python-library-hijacking/) talking about Python library hijacking. The important part is the directories and their priority that Python searches for the package to import:

> * **Directory of the script being executed**
> * /usr/lib/python2.7
> * /usr/lib/python2.7/plat-x86_64-linux-gnu
>* /usr/lib/python2.7/lib-tk
>
> ...

Which means if we create our own version of `random.py` in the home directory, it will be imported instead of the genuine `random` module.

So this is the `random.py` I created:

```python
import pty
pty.spawn('/bin/bash')
```

And let's run the Python script once more (as `rabbit`):

![visit-rabbit](/img/wonderland/wonderland-visit-rabbit.png)

Voila! We now have a rabbit shell!

# The tea party

Now we can see what's in rabbit's home directory.

![rabbit's home](/img/wonderland/wonderland-rabbit-home.png)

Ah! Sticky bits. I like it.

In case you don't know what it is, a sticky bit is basically some permission on a executable file in Linux that allows whoever runs this file to do something as another user (SUID) or another group (SGID).

Combined with PATH variable exploitation, sticky bits can be used to execute arbitary command as another user. So let's see if there's anything we can take advantage of within this tea party.

Here, we use `strings` command to extract printable strings from a binary file. 

```bash
strings teaParty
```

![tea party](/img/wonderland/wonderland-teaparty.png)

So we can easily infer that this part in the red brackets generated the messages shown in the previous image. 

Most interesing thing among them is the line in the red rectangle. This shows that somewhere inside this program, it runs a command in shell. And it used the `date` command without specifying an absolute path.

We can create a executable file called `date` inside `/tmp` directory, and add `/tmp` to the beginning of `PATH` variable. Then we can execute whatever we want as another user by running `./teaParty`.

So first thing let's check which user's priviledge we can get by doing this.

![tea party whoami](/img/wonderland/wonderland-teaparty-whoami.png)

Now we've got Mr. Hatter's priviledge, let's see what's under hatter's home directory.

Modify `/tmp/date` as following:

```bash
#!/bin/sh
echo 
ls -la /home/hatter
echo 
```

And do the trick again:

![ls hatter](/img/wonderland/wonderland-ls-hatter2.png)

Inside the password.txt file is the password of hatter. Now we have a full shell as hatter by SSH into the box.

![hatter shell](/img/wonderland/wonderland-hatter-shell.png)


# Root

As we found nothing doable inside hatter's home directory, now it's time to do some local enumeration. The enumeration script I used is [LinEnum.sh](https://github.com/rebootuser/LinEnum/blob/master/LinEnum.sh).

By reading the report carefully, I found this interesting:

![hatter enum](/img/wonderland/wonderland-hatter-enum.png)

![hatter perl](/img/wonderland/wonderland-hatter-perl.png)

The `perl` interpreter executable has the `setuid` capability. And we now, as hatter, has the permission to run it. This means we can get anyone's priviledge in this box as hatter.

I'm not quite familiar with perl, but I found [this amazing guide](https://gtfobins.github.io/gtfobins/perl/).

![root](/img/wonderland/wonderland-root.png)

Hooray! Now loot the flags!

