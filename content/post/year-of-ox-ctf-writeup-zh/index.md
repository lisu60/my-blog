+++
title = "牛年灯谜 CTF Writeup Part 1"
date = 2021-02-13T2:39:00+11:00
lastmod = 2021-02-13T2:39:00+11:00
tags = ["Year of Ox"]
categories = ["CTF"]
imgs = []
cover = ""  # image show on top
readingTime = true  # show reading time after article date
toc = true
comments = true
justify = false  # text-align: justify;
single = true  # display as a single page, hide navigation on bottom, like as about page.
license = ""  # CC License
draft = false
+++


# 引子

[Part 2](/post/year-of-ox-ctf-writeup-part2-zh/)

一年前我在 UTS 开始学习以来，我打算转向网络/信息安全方向，也由此接触到了 CTF (Capture the Flag) 这种有趣的活动。在农历新年的前一周时，我突然想到或许可以自己做一个 CTF 给大家玩玩，分享我的一些乐趣，也让一些可能会感兴趣的朋友接触到 CTF。

于是我就快马加鞭出了几个题，搞定了网站 hosting 服务，匆忙上线了（其实前几天都在忙别的事，最后一天急忙赶出来的哈哈）。具体过程这里就不讲了，有兴趣可以等我稍晚发布的另一篇文章。

下面是我作为出题人自己的解题过程。前两题比较面向新手，我会讲得详细一些。


# 第一个红包

tl;dr

最初的线索是一个 QR Code:

![qr code](start.png)

解码 QR Code 获得如下字符串：

```
dWdnY2Y6Ly9scm5lYnNiay5nbmwxYmUueXYvdmFxcmsudWd6eQo=
```

Base64 解码上述字符串得到：

```
uggcf://lrnebsbk.gnl1be.yv/vaqrk.ugzy
```

将上述字符串所有字母旋转13个位置（如下表所示） 得到：

```
https://yearofox.tay1or.li/index.html
```

|   |   |
| ----- | ----- |
| Input	| `ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz` |
| Output	| `NOPQRSTUVWXYZABCDEFGHIJKLMnopqrstuvwxyzabcdefghijklm` |


在浏览器中打开上述 URL 即可找到红包口令。

下面是详细解释。

## QR Code

最开始的线索是一个 QR Code：

![qr code](start.png)

非专业人士习惯把它称为“二维码”，但 QR Code 只是众多二维码制式中的一种。如今人们跟 QR Code 交互的方式通常是使用手机扫码，随后跳转到一个 app 或者网页。所以不少新手在微信中扫码后看到的结果是一串没有明显意思的字符的时候，第一反应是（引用几位朋友发来的抱怨）：“你这个二维码扫不出来/识别不了啊”。

首先需要了解的一点是：如同大多数二维码和条形码一样，QR Code 编码的通常是是文本。即通过解码 QR Code 可以得到一段文本信息。当你使用手机 app 解码一个 QR Code 的时候（如微信的“识别图中的二维码”），如果解码得到的文本是一个 URL（例如：`https://tay1or.li/post/year-of-ox-ctf-writeup-zh`），手机 app 往往会直接把用户带到浏览器中并且打开该 URL，而不是将这个文本呈现给你。

通过搜索引擎搜寻可以找到不少网站或者 app 可以解码 QR Code，甚至你也可以直接使用微信扫码。解码后我们得到如下文本：

```
dWdnY2Y6Ly9scm5lYnNiay5nbmwxYmUueXYvdmFxcmsudWd6eQo=
```

## Base64

有几位朋友解码出了上述文本，随后来问我：“真的不是乱码吗？？”

首先，并不是看不懂的东西就叫乱码啦 😅

乱码是指解码字符编码时采用了与编码时不同的[字符编码](https://en.wikipedia.org/wiki/Character_encoding)（字符和二进制数值的映射，或者说，如何用二进制数值表示字符的一种约定）导致不能显示正确的字符。下图是一些常见的乱码及原因（twitter: @Linmiv)：

![mojibake](mojibake.png)

本题中的上述文本，不熟悉的人看到之后可能会感到莫名其妙。但若仔细观察，不难发现其中并没有不正常显示的字符，以及如下特征：

```
dWdnY2Y6Ly9scm5lYnNiay5nbmwxYmUueXYvdmFxcmsudWd6eQo=
```

* 包含的字符基本全是大、小写拉丁字母和数字；
* 末尾有一个等号“`=`”。

这里需要你具备一些相关知识，或者使用搜索引擎的技能。一旦你具备这个知识，根据上述特征，你会很容易识别出这是一个 [Base64](https://en.wikipedia.org/wiki/Base64) 编码产生的字符串。因此这里你需要做的，只是 Base64 解码这个字符串。同样地，你也可以很容易地使用搜索引擎找到一个 Base64 解码工具。解码后你会得到：


```
uggcf://lrnebsbk.gnl1be.yv/vaqrk.ugzy
```

---------

这里说些**题外话**，如果没兴趣也可以直接看下一步。

经常看到有人说“Base64 加密”。事实上 Base64 不具备加密的功能，Base64 只是一种**编码**。在特定的语境中，Base64 可能起到**混淆**的作用，让人不能马上识别出被编码的内容，或者避开某些程序针对字符的限制和检查。但如你所见，只要一个唾手可得的解码工具任何人都可以马上看到你想隐藏的内容。

因此，不要用 Base64 来“加密”任何内容。

## ROT13


```
uggcf://lrnebsbk.gnl1be.yv/vaqrk.ugzy
```

我们得到了这样一个字符串。可是，好家伙，这又是个啥？

如果你一路看到了这里，那你很有可能正是本文假设的目标读者：新手，没什么头绪，看到乱糟糟的字符早就想放弃了，但仍然很好奇。

那么你现在需要的，仍然是冷静和仔细观察，以及一些猜测。


* 首先你可能会注意到，这个字符串里出现了`://`序列，很像是平时见到的 URL 里会看到的东西。还有一些点“`.`”和斜杠“`/`”可以印证关于 URL 的猜想，只是其他的字符好像都乱七八糟的。

* 一般的网页 URL 通常是以 `http` 或者 `https` 开头，而我们从前一步中得到的这个开头是 `uggcf`。

* `uggcf` 中的 `gg` 跟 `https` 中的 `tt` 出现在同样的位置上，又都是连续两个重复的字符。这可能意味着 `uggcf` 是由 `https` 通过某种字母替换产生的。

上述过程是我在已经直到答案的情况下写出的。你的具体的观察和猜想的过程可能不尽相同。但是这不要紧，因为你总可以想办法验证你的猜想。不要害怕去验证一些看起来有点傻的猜想，解谜的过程本就是如此，猜错了也不必嘲笑你自己 :)

想到了字母替换，首先要尝试的自然是[恺撒加密](https://en.wikipedia.org/wiki/Caesar_cipher)。恺撒加密很简单，就是将整个字母表按顺序错位，将明文中的字母誊写为错位后的字母。比如当设置错位数为3的时候，明文中的字母 A 在密文中就写成 D，明文中的 B 在密文中写成 E，以此类推。如此，例如明文的句子为：

The quick brown fox jumped over the lazy dog

其对应的密文就是：

Wkh txlfn eurzq ira mxpshg ryhu wkh odcb grj

不难看出，恺撒加密的可能性相当容易穷尽。你只须最多尝试25种可能就能找到明文（或者发现目标密文使用的不是恺撒加密）。而对于已经知道部分密文所对应的明文的情况（例如此题中 `uggcf` -> `https`），只需要一些简单地算数你就可以知道错位的位数。很显然，在我们的例子中这个数字是13。

当你把上一步中得到的文本中的所有字母都错位13位之后，你会得到：

```
https://yearofox.tay1or.li/index.html
```

-------

事实上，错位数为13的恺撒加密有一个特别的性质：因为拉丁字母总共有26个字母，而13正好是它的一半，所以错位数为13的恺撒加密的加密和解谜过程是相同的。意即，对错位13位的密文再次错位13位，即可得到原本的明文。为此，错位数为13的恺撒加密有个特别的名字：ROT13。

|   |   |
| ----- | ----- |
| Input	| `ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz` |
| Output	| `NOPQRSTUVWXYZABCDEFGHIJKLMnopqrstuvwxyzabcdefghijklm` |

------

至此，我们找到了一段真正看起来有点明显意义的文本：一个 URL。在浏览器中打开[这个 URL](https://yearofox.tay1or.li/index.html)，你就找到了第一个红包的口令。恭喜你！

![index](index.png)




