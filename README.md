# Danmacu

Bilibili 直播弹幕姬。

因为之前在 Mac 上用的弹幕库最近几天获取不了弹幕了，所以准备自己写一个。

## 使用

```bash
pipenv install
pipenv shell
env DANMACU_APPKEY="" DANMACU_SECRET="" python -m danmaku.main <房间号>
```

然后会显示一个 URL，使用浮动窗口工具打开这个网页即可。

**注意：还没写完，现在还没法用。**

## 工作原理

使用 Bilibili Android 客户端的直播 API，成功启动进入房间后会监听一个本地 HTTP 端口和一个 WebSocket 端口。

HTTP 端口会返回一个 HTML 网页，这个网页上的 JS 会通过 WebSocket 连接后台，并把弹幕内容显示在页面上。

配合一些全局浮动窗口工具（如 Helium）打开这个本地 HTTP 端口，就可以当一个弹幕姬用了。

**目前只完成了协议部分， HTML，JS，和内部 WebSocket 协议都还没写。**

## LICENSE

WTFPL
