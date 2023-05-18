const scroll = document.getElementById("scroll");
const messages = document.createElement("ul");
scroll.appendChild(messages);

let currentPopularity = 0;

const ws = new WebSocket("ws://127.0.0.1:7778/");

const newDanmakuLine = (danmaku) => {
    const fragment = document.createDocumentFragment();

    if (danmaku.badge !== null) {
        const badge = document.createElement("span");
        badge.classList.add("badge");

        const badge_name = document.createElement("span");
        badge_name.classList.add("badge-name");
        badge_name.textContent = danmaku.badge;
        const color = `#${danmaku.badge_color.toString("16")}`;
        badge_name.style["border-color"] = color;
        badge_name.style["background-color"] = color;
        badge.appendChild(badge_name);

        const badge_level = document.createElement("span");
        badge_level.classList.add("badge-level");
        badge_level.textContent = danmaku.badge_level.toString();
        badge_level.style["border-color"] = color;
        badge.appendChild(badge_level);

        fragment.appendChild(badge);
    }

    const user_level = document.createElement("span");
    user_level.classList.add("user-level");
    user_level.textContent = `UL ${danmaku.level}`;
    const ul_color = `#${danmaku.level_color.toString("16")}`;
    user_level.style["border-color"] = ul_color;
    user_level.style["color"] = ul_color;
    fragment.appendChild(user_level);

    const user = document.createElement("span");
    user.classList.add("user");
    user.textContent = danmaku.user;
    fragment.appendChild(user);

    fragment.appendChild(document.createTextNode("："));

    const message = document.createElement("span");
    message.classList.add("message");
    message.textContent = danmaku.message;
    fragment.appendChild(message)

    return fragment;
};

const newGiftLine = (gift) => {
    const fragment = document.createDocumentFragment();

    const user = document.createElement("span");
    user.classList.add("user");
    user.textContent = gift.user;
    fragment.appendChild(user);

    fragment.appendChild(document.createTextNode(`：赠送 ${gift.name} x${gift.count}`));

    return fragment;
};

const newInteractWord = (interact_word) => {
    const fragment = document.createDocumentFragment();

    const user = document.createElement("span");
    user.classList.add("user");
    user.textContent = interact_word.user;
    fragment.appendChild(user);

    fragment.appendChild(document.createTextNode(`：欢迎进入直播间`));
    return fragment;
}

const newObserver = () => {
    return new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting === false) {
                autoRemoveObserver.unobserve(entry.target);
                messages.removeChild(entry.target);
            }
        });
    }, { threshold: [1] });
}

let autoRemoveObserver = newObserver();

ws.onopen = () => {
    const li = document.createElement("li");
    li.textContent = "连接房间成功！";
    messages.appendChild(li);
};

ws.onmessage = (event) => {

    const message = JSON.parse(event.data)
    const li = document.createElement("li");

    if (message.cmd == "DANMU_MSG") {
        const danmaku = message;
        li.classList.add("danmaku");
        li.appendChild(newDanmakuLine(danmaku));
    } else if (message.cmd == "SEND_GIFT") {
        const gift = message
        li.classList.add("gift");
        li.appendChild(newGiftLine(gift));
    } else if (message.cmd == "INTERACT_WORD") {
        const interact_word = message
        li.classList.add("interact_word");
        li.appendChild(newInteractWord(interact_word));
    } else if (message.type) {
        if (message.type == "popularity") {
            currentPopularity = message.count;
            document.getElementById("popularity").textContent = currentPopularity;
        }
    }

    messages.appendChild(li);

    li.scrollIntoView();
};

ws.onerror = (error) => {
    console.error(error);
};

ws.onclose = (_) => {
    const li = document.createElement("li");
    li.textContent = "连接失败，请检查程序是否已启动并刷新页面";
    messages.appendChild(li);
};

setInterval(() => {
    autoRemoveObserver.disconnect();

    if (messages.childNodes.length > 0) {
        messages.childNodes[messages.childNodes.length - 1].scrollIntoView();
    }

    autoRemoveObserver = newObserver();
    messages.childNodes.forEach((li) => {
        autoRemoveObserver.observe(li);
    });
}, 500);
