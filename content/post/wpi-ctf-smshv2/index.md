+++
title = "WPI CTF: Suckmore Shell 2.0"
date = 2020-04-18T23:27:46+10:00
lastmod = 2020-04-18T23:27:46+10:00
tags = ["WPICTF2020"]
categories = [ "CTF"]
imgs = []
cover = "smsh.png"  # image show on top
readingTime = true  # show reading time after article date
toc = true
comments = true
justify = false  # text-align: justify;
single = false  # display as a single page, hide navigation on bottom, like as about page.
license = ""  # CC License
draft = false
+++

# Challenge Description

> After its abysmal performance at WPICTF 2019, suckmore shell v1 has been replaced with a more secure, innovative and performant version, aptly named suckmore shell V2.
>
> ssh smsh@smsh.wpictf.xyz pass: suckmore>suckless
>
> made by: acurless

# Poking Around

First off, SSH login. 

```bash
ssh smsh@smsh.wpictf.xyz
```

Give the password when asked.

![login](smsh-login.png)

A prompt, hmmmm. Doesn't look a normal shell, but it's a shell. Okay, let's see what we have now.

```bash
ls -la
```

![ls](smsh-ls.png)

Whaaaaaaaat? We have found the `flag` already!? Easy 200 points!

```bash
cat flag
```

![cat](smsh-cat.png)

Strange. The shell was hanging after I entered the command.

That's fine. Let's try other ways to read the file.

![other commands](smsh-other-cmd.png)

Not even `string` or `grep`. When I tried `less flag` it even messed the console up, and I had to fire up a new terminal tab. I was wrong. It's not easy 200 points.

I finally got lucky with `base64` command.

```bash
base64 flag
```

![base64](smsh-base64.png)

Seems it managed to read and encode that file. Let's copy the encoded text and decode it on our own machine.

```bash
echo -n "ZWNobyAiV1BJe1NVY2ttb3JlU29mdHdhcmVOMzNkejJHM1RpdFRvZ2VUSEVSfSIK" | base64 -d
```


![decode](smsh-decode.png)

Curious. It's a shell command in that file. Anyway, we've retrieved the flag.
