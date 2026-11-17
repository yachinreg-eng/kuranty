import wave, os, json

SRC = r"C:\Projects\NewYear\_voice"
DST = r"C:\Projects\NewYear\assets\web\greeting.wav"
GAP = 0.45

lines = ["l1", "l2", "l3", "l4", "l5"]
parts = []
for name in lines:
    p = os.path.join(SRC, name + ".wav")
    with wave.open(p, "rb") as w:
        n, ch, sw, sr = w.getnframes(), w.getnchannels(), w.getsampwidth(), w.getframerate()
        data = w.readframes(n)
    parts.append((sr, ch, sw, n / float(sr), data))
    print(name, sr, ch, sw * 8, "bit", round(n / float(sr), 2), "s")

sr, ch, sw = parts[0][0], parts[0][1], parts[0][2]
assert all(p[0] == sr and p[1] == ch and p[2] == sw for p in parts), "format mismatch"

gap_frames = int(round(GAP * sr))
gap = b"\x00" * gap_frames * ch * sw

out = []
cues = []
cursor = 0
for (psr, pch, psw, dur, data) in parts:
    start = cursor / float(sr)
    out.append(data)
    cursor += len(data) // (ch * sw)
    cues.append({"start": round(start, 2), "end": round(cursor / float(sr), 2)})
    out.append(gap)
    cursor += gap_frames

total = sum(len(x) for x in out) // (ch * sw)
with wave.open(DST, "wb") as w:
    w.setnchannels(ch)
    w.setsampwidth(sw)
    w.setframerate(sr)
    w.writeframes(b"".join(out))

print("total", round(total / float(sr), 2), "s ->", DST, os.path.getsize(DST), "bytes")
print(json.dumps(cues))
