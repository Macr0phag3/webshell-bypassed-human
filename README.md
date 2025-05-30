# webshell-bypassed-human
见公众号文章：[传送门](https://mp.weixin.qq.com/s?__biz=MzI3OTE4MTU5Mw==&mid=2247483933&idx=1&sn=94c10672d664ae84e233792c09231a47&chksm=eb4ae26bdc3d6b7d0ffc09f9c64ac081e4e2af2d629927321d531b37a86a6333a5635fdf6a16&scene=0&xtrack=1#rd)
，或者见 fb 文章 https://www.freebuf.com/articles/web/241454.html

过人 webshell 的生成工具

```shell
» python hide_webshell.py
usage: hide_webshell.py [-h] -pf PAYLOAD_FILE [--pro] [-wf WEBSHELL_FILE]
                        [--debug]
                        php
hide_webshell.py: error: the following arguments are required: php, -pf/--payload_file
```

将 payload 放在 `-pf` 所指定的路径

## hide webshell
示例：

`python hide_webshell.py normal.php -pf payload.txt`

## hide webshell pro
示例：

`python hide_webshell.py normal_pro.php -pf payload.txt --pro`

## payload 示例

- `systemecho "hacked by Tr0y :)"`

注：如果是 php <7.2 请见对应文件夹

核心变化是：
1. `create_function` PHP 7.2 版本中被正式废弃的，并在后续版本（如 PHP 8.0）中被移除。现在替换成 `call_user_func`。其实 `call_user_func` 较为麻烦，可以考虑直接用 `system`
2. 由于变化 1，payload 长度，以及 `normal_pro.php` 的变量要足够多，否则会导致无法正常提取参数
3. 注意：在 PHP 中，`eval` 是一个语言结构（language construct）而不是函数，因此不能通过变量函数（variable functions）的方式来调用

## 完整示例
```
# macr0phag3 in ~/Tr0y/webshell-bypassed-human on git:master ✖︎ [14:45:27]
» cat payload.txt
systemecho "hacked by Tr0y :)"%

# macr0phag3 in ~/Tr0y/webshell-bypassed-human on git:master ✖︎ [14:45:28]
» p hide_webshell.py normal.php -pf payload.txt && php webshell_hidden.php
[+] Hide webshell in normal mode
  [-] Get payload from payload.txt
      Payload is systemecho "hacked by Tr0y :)"
  [-] Get php code from normal.php
[!] Saved webshell as webshell_hidden.php
[!] All done

Bye :)
hacked by Tr0y :)

# macr0phag3 in ~/Tr0y/webshell-bypassed-human on git:master ✖︎ [14:45:31]
» p hide_webshell.py normal_pro.php -pf payload.txt --pro && php webshell_hidden.php
[+] Hide webshell in pro mode
  [-] Get payload from payload.txt
      Payload is systemecho "hacked by Tr0y :)"
  [-] Get php code from normal_pro.php
[!] Saved webshell as webshell_hidden.php
[!] All done

Bye :)
hacked by Tr0y :)
```

## 其他
<img src="https://clean-1252075454.cos.ap-nanjing.myqcloud.com/20200528120800990.png" width="500">

[![Stargazers over time](https://starchart.cc/Macr0phag3/webshell-bypassed-human.svg)](https://starchart.cc/Macr0phag3/webshell-bypassed-human)
