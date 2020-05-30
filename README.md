# DanMacU

写来给自己用的 Bilibili 直播弹幕姬。

几个小时写出来的，我好久没写过 Python 了，代码质量奇差。什么项目架构设计，优雅错误处理啊都不存在，就图一梭子能跑就行，千万不要看实现代码。

## 预览

![preview]

右下角那个就是。

## 依赖

- Python 3.7+
- pipenv

## 使用

```sh
$ pipenv install
$ pipenv shell
$ python -m danmacu.main <房间号>
Danmaku page: http://127.0.0.1:7777/index.html
Press Command+C to stop...
```

然后使用浮动窗口工具（如果不知道是啥请看 Q&A 部分第 6 条，或者直接用浏览器）打开这个程序输出的 URL 即可。

## 工作原理

使用的是 Bilibili Android 客户端的直播 API。

在连接 B 站的弹幕 WebSocket 服务器后，会启动本地 WebSocket 服务器和 HTTP 服务器。

程序会将 B 站返回的弹幕/送礼等信息解析成易处理的格式，发送给连接到本地 WebSocket 服务器的客户端。

而打开终端里的 URL，本地 HTTP 服务输出的页面上的 Javascript 会连接本地 WebSocket 服务器，并把弹幕内容显示在页面上。

配合一些全局浮动窗口工具打开这个本地 HTTP 端口，就可以当一个弹幕姬用了。

见下图：

```text
                          +--------------------------------------------+
                          |                                            |
+-------------------+     |  +------------------+                      |
|                   |     |  |                  |                      |
|  Bilibili Server  +<------>+ WebSocket Client |     Danmacu Core     |
|                   |     |  |                  |                      |
+-------------------+     |  +--------+---------+                      |
                          |           |                                |
                          |  +--------v---------+ +----------------+   |
                          |  |                  | |                |   |
                          |  |     Internal     | |    Internal    |   |
                          |  | Websocket server | |  HTTP Server   |   |
                          |  |                  | |                |   |
                          |  +--------+---------+ +-------+--------+   |
                          |           |                   |            |
                          +--------------------------------------------+
                                      |                   |
                                      |                   |
                                      |        +----------v--------+
                                      |        |  HTML             |
                                      |        |                   |
                                      |        |  +------------+   |
                                      |        |  |     DOM    <-+ |
                                      |        |  +------------+ | |
                                      |        |                 | |
                                      |        |  +------------- | |
                                      +-----------> Javascript +-+ |
                                               |  +------------+   |
                                               |                   |
                                               +-------------------+

                                              Loaded into float window
```

## Q&A

### 1. 为什么要做这个

因为之前在 Mac 上用的[弹幕库][danmuku-homepage]最近获取不了弹幕了，没办法只能自己写个。

### 2. 名字是什么意思

给 **mac**OS 用的弹幕（Danmaku）姬 ==> Dan**Mac**U

没有什么其他意思。

### 3. 为什么不用 blivechat/bilibili-live-chat/BiliChat/或其他类似项目

[bilibili-live-chat][bilibili-live-chat-github]、[BiliChat][BiliChat-github] 这两个我写之前确实不知道。

不用 [blivechat][blivechat-github] 的主要原因是我只知道 [chat.bilisc.com](https://chat.bilisc.com/) 这个网站，然后看这个网站好像是给 OBS 用的，CSS 是额外生成，然后填在 OBS 的浏览器源的参数里。

而我的主要需求是自己放桌面上看，必须有办法用 OBS 以外的方法来改 CSS，所以就以为没法满足需求。

后来快写完才发现原来 blivechat 是开源的，而且可以本地跑，惨 我 惨。

### 4. 只能 Mac 用吗

理论上倒不是。并没有任何操作系统相关的代码，只是 Windows 上可以用的弹幕姬太多了，应该也不会有人需要用这个。

哦哦，Linux 用户倒是有可能来用，不过我没测过，如果有问题你提 Issue 吧。

### 5. 为什么没有 XXX 功能

因为只是我自己用用而已。

平常我也就只在周末给群里朋友们直播写写代码，玩玩小游戏啥的，也没有别人看，主业也不是这个，所以能看到弹幕和礼物就够了。

什么舰长，SC，房管，VIP，彩色弹幕之类的花里胡哨的功能我都用不到。

如果你需要这些功能的话，建议使用 Q&A No.3 的提到的这些功能比较全的项目。

不过你要是实在想自己加，那也可以随意 Fork 加上，如果愿意 PR 回我这里我也欢迎。

### 6. 浮动窗口工具是啥

就是可以 Always on top 的一个窗口，不然你焦点去别的窗口了就看不见弹幕了。

我用的是 [Helium 3][helium3-github]，你也可以用别的，只要能支持打开网页就行。

### 7. 不发布到 PyPI 吗

没这必要，真没必要……

## TODO

- [ ] 页面 CSS 美化（我真的尽力了，可惜我不是前端，这一条强烈欢迎各种 PR）
- [ ] 用户头像（hash 方法未研究）
- [ ] 礼物图片（需要加载一个几百 K 的 JSON，有点大）
- [ ] 礼物合并（因为是自己用，没啥礼物，所以优先级很低）
- [ ] 自定义监听端口（自己用也没啥改的需求）
- [ ] 参数自定义 style（现在如果想改就直接改代码里的了）

## 致谢

除 Pipfile 中的依赖项目以外，还要感谢以下项目的帮助：

- [mitmproxy][mitmproxy-homepage]
- [bilibili-api][bilibili-api-github]
- [blivedm][blivedm-github]

## LICENSE

WTFPL

[preview]: https://rikka.7sdre.am/files/a3412e57-c1f2-4de6-90c5-afc0b75166bb.png
[danmuku-homepage]: https://www.danmaku.live/
[bilibili-live-chat-github]: https://github.com/Tsuk1ko/bilibili-live-chat
[BiliChat-github]: https://github.com/3Shain/BiliChat
[blivechat-github]: https://github.com/xfgryujk/blivechat
[helium3-github]: https://github.com/slashlos/Helium
[mitmproxy-homepage]: https://mitmproxy.org/
[bilibili-api-github]: https://github.com/czp3009/bilibili-api
[blivedm-github]: https://github.com/xfgryujk/blivedm
