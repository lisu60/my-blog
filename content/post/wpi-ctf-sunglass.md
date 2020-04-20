+++
title = "WPI CTF: 👉😎👉"
date = 2020-04-18T17:02:06+10:00
lastmod = 2020-04-18T17:02:06+10:00
tags = ["WPICTF2020"]
categories = ["Blog", "CTF"]
imgs = []
cover = "/img/sunglass.png"  # image show on top
readingTime = true  # show reading time after article date
toc = true
comments = true
justify = false  # text-align: justify;
single = true  # display as a single page, hide navigation on bottom, like as about page.
license = ""  # CC License
draft = false
+++

![sunglass-2](/img/sunglass-2.png)

> 👈😎👈Zoop👉😎👉Zoop 👈😎👈Zoop👉😎👉Zoop 👈😎👈Zoop👉😎👉Zoop 👈😎👈Zoop👉😎👉Zoop 👈😎👈Zoop👉😎👉Zoop 
>
> ... 
>
>  👈😎👈Zoop👉😎👉Zoop 👈😎👈Zoop👉😎👉Zoop 👈😎👈Zoop👉😎👉Zoop 👈😎👈Zoop
>
> [http://zoop.wpictf.xyz](http://zoop.wpictf.xyz)
>
> made by: ollien

# Exploring

So seems it starts with a web page. Let's take a look first.

![page](/img/sunglass-page.png)

This looks like a IM, and a friend talks about sending a file from a website http://storage.zoop. Let's poke around.

When I click on "Attach" button, a dialog shows up. It allows me to input a URL of the storage.zoop website, and I can even preview the file of the URL I input.

![attach](/img/sunglass-attach.png)

# The *Attach* Dialog

Well, let's try the file mentioned by our friend first.

![quarterly_report](/img/sunglass-quarterly_report.png)

Wow. Such anger. So fierce. ![doge](https://atipsewa.sirv.com/doge.jpg?w=40)


But I just can't resist to try again with file name `flag.txt` in that URL.



And... TADA!

![flag](/img/sunglass-flag.png)