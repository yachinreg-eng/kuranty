import asyncio, pathlib, edge_tts

OUT = pathlib.Path(r"C:\Projects\NewYear\assets\web")
LINES = [
    ("greet1.mp3", "svetlana", "Здравствуйте, дорогие друзья!"),
    ("greet2.mp3", "dmitry",   "Мы пришли к вам в этот зимний вечер, чтобы пожелать счастья и удачи."),
    ("greet3.mp3", "svetlana", "Пусть Новый год принесёт тепло в ваш дом и радость в каждый день."),
    ("greet4.mp3", "dmitry",   "Пусть куранты пробьют двенадцать, и всё загаданное исполнится!"),
    ("greet5.mp3", "dmitry",   "С Новым годом, дорогие наши!"),
]
BASE = {"dmitry": "ru-RU-DmitryNeural", "svetlana": "ru-RU-SvetlanaNeural"}
VARIANTS = {
    "dmitry":   [dict(rate="-8%", pitch="-12Hz"), dict(pitch="-12Hz"), dict(rate="-10%"), dict()],
    "svetlana": [dict(rate="-2%", pitch="+8Hz"), dict(pitch="+8Hz"), dict(), dict(rate="-4%")],
}

async def synth(text, voice, opts):
    c = edge_tts.Communicate(text, voice=voice, **opts)
    data = b""
    async for ch in c.stream():
        if ch["type"] == "audio":
            data += ch["data"]
    return data

async def main():
    for name, who, text in LINES:
        ok = False
        vs = VARIANTS[who]
        for attempt in range(10):
            opts = vs[attempt % len(vs)]
            try:
                data = await synth(text, BASE[who], opts)
                if len(data) > 5000:
                    (OUT / name).write_bytes(data)
                    print(name, who, opts, len(data), "bytes")
                    ok = True
                    break
            except Exception as e:
                pass
            await asyncio.sleep(1.5)
        if not ok:
            print(name, "FAILED")
        await asyncio.sleep(1.0)

asyncio.run(main())
