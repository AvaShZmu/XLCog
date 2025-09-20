
# XLCog

A feature-rich personal Discord Bot made using discord.py for fun, also with some pretty interesting functions.  
This project began back in September 2024, but with a slightly less appropriate alias. This repo is a refactor of the project, with much neater and more appropriate code.




## Features

- Various simple commands (shooting, ping commands, and a bunch of miscancellous functions)
- A "Chatbot" which essentially uses a Python API wrapper around c.ai (https://github.com/Xtr4F/PyCharacterAI).
- A musicplayer built using wavelink (https://github.com/PythonistaGuild/Wavelink). Functions include: play, pause, search youtube videos, load playlists, queues, etc. - in the forms of discord's beautiful GUI.

> [!IMPORTANT]
> In order to use the music player function of this client, you need to have a Lavalink server to host the bot on.  
> Instructions on creating a Lavalink server can be found here: [https://lavalink.dev/getting-started](https://lavalink.dev/getting-started). Add the server's URI, port and password in Bot_Class.     Alternatively, you can use a public node, but this is not advisable.  
> You may want to bypass Youtube's OAuth2. Instructions can be found in [here](https://github.com/lavalink-devs/youtube-source?tab=readme-ov-file#plugin)

## Installation

- Clone the project.

```bash
git clone https://github.com/AvaShZmu/XLCog.git
cd XLCog
pip install -r requirements.txt
```
- Create a Discord Application on the [Discord Developer Portal](https://discord.com/developers/applications).
- Insert the token in Bot.py (an environment variable is recommended but I'm too lazy for that).
- Run Bot.py

```bash
python Bot.py
```

- If you don't want wavelink support, then delete the following in Bot_Class:
```python
async def setup_hook(self) -> None:
    nodes = [wavelink.Node(uri="...", password="...", inactive_player_timeout=...)]
    await wavelink.Pool.connect(nodes=nodes, client=self, cache_capacity=100)

async def on_wavelink_node_ready(self, payload: wavelink.NodeReadyEventPayload) -> None:
    logging.info("Wavelink Node connected: %r | Resumed: %s", payload.node, payload.resumed)
```

## 📸 Screenshots  

<details>
<summary><b>📝 All Commands</b></summary>

<img src="https://media.discordapp.net/attachments/868390457623859220/1418950196968161380/image.png?ex=68cffbd9&is=68ceaa59&hm=187b74a4dcfe522e46941d7cbf0fb3ffbd4be6899d1d7a1811fc33b8c9023762&=&format=webp&quality=lossless&width=1458&height=1360" width="80%" />

</details>

---

<details>
<summary><b>🎮 Miscellaneous Games / Entertainment</b></summary>

**Shoot**  

<p float="left">
  <img src="https://media.discordapp.net/attachments/868390457623859220/1418948914702188604/image.png?ex=68cffaa8&is=68cea928&hm=f39b7fa3c4b104bac9e2cc6ddd92d65c9b386653ec11b20d184589bc8c831790&=&format=webp&quality=lossless&width=2046&height=784" width="45%" />
  <img src="https://media.discordapp.net/attachments/868390457623859220/1418948915121885204/image.png?ex=68cffaa8&is=68cea928&hm=99f2a377e46a15f0d2c12d08c5cbe8255884ee135c3030fa1aa4b4dade445ad9&=&format=webp&quality=lossless&width=1846&height=736" width="45%" />
</p>

**Duel**  

<p float="left">
  <img src="https://cdn.discordapp.com/attachments/868390457623859220/1418950905553752125/image.png?ex=68cffc82&is=68ceab02&hm=5d0ecb9f338919209e3bb2c348a7d6c9674ce1f9d61f9fe0d966abd0cdfa1df1&" width="30%" />
  <img src="https://media.discordapp.net/attachments/868390457623859220/1418951578286559373/image.png?ex=68cffd23&is=68ceaba3&hm=c8f5ab83345f34f07e18f7bbc1e296de296ea4842b49f7e9ab422d91d2b506fe&=&format=webp&quality=lossless&width=1584&height=950" width="30%" />
  <img src="https://media.discordapp.net/attachments/868390457623859220/1418951578794201179/image.png?ex=68cffd23&is=68ceaba3&hm=63f5d88db694e79a4ccc6b06bd836e8e82f4d0ccdff0d68021bbfd348d499c8d&=&format=webp&quality=lossless&width=1114&height=1044" width="30%" />
</p>

</details>

---

<details>
<summary><b>🎵 Music Player</b></summary>

**Searching (based on keywords):**  

<img src="https://media.discordapp.net/attachments/868390457623859220/1418949699251212358/image.png?ex=68cffb63&is=68cea9e3&hm=4b40c5819aa30571692a4cce3c605dfb75c5bd2da588925e293e113cef020ce9&=&format=webp&quality=lossless&width=2256&height=1094" width="80%" />

**Adding query to queue:**  

<img src="https://media.discordapp.net/attachments/868390457623859220/1418949699641278515/image.png?ex=68cffb63&is=68cea9e3&hm=d686601d21e269521152f40bda27d484f54ca077f549c29b3297f378b1ac93f9&=&format=webp&quality=lossless&width=1138&height=1152" width="80%" />

**Queue:**  

<p float="left">
  <img src="https://media.discordapp.net/attachments/868390457623859220/1418949700106850436/image.png?ex=68cffb63&is=68cea9e3&hm=13d493f88709fd8a5afeb7ecce11f8928614e6e6f8a6227afde6de290ee3d0c7&=&format=webp&quality=lossless&width=2092&height=1152" width="45%" />
  <img src="https://media.discordapp.net/attachments/868390457623859220/1418949700484333680/image.png?ex=68cffb63&is=68cea9e3&hm=6bb19620fb51748a801399c98fe6d52fbfdbecf0cd9b59b8217f64e08a999638&=&format=webp&quality=lossless&width=1524&height=1152" width="45%" />
</p>

</details>

---

<details>
<summary><b>🤖 Chatbot</b></summary>

<img src="https://media.discordapp.net/attachments/868390457623859220/1418948383137206383/image.png?ex=68cffa29&is=68cea8a9&hm=76f099e23f9b7084f2e14a65fc6dd17b54580ec11ba225df25ad6b71f2024a53&=&format=webp&quality=lossless&width=1420&height=1360" width="80%" />

</details>

---

And much more!

## Acknowledgements

 - [wavelink](https://github.com/PythonistaGuild/Wavelink)
 - [discord.py](https://github.com/Rapptz/discord.py)
 - [Lavalink](https://github.com/lavalink-devs/Lavalink)
 - [PyCharacterAI](https://github.com/Xtr4F/PyCharacterAI)

