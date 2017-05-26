""" testerino salcino """
import random
from fractions import Fraction as Frac
from scoreholder import ScoreHolder


S = ScoreHolder(112)  # 112 BPM

notes1 = ["Eb2", "Bb3", "Eb3", "G3",  "B4",  "Eb5", "", "", "", "", "", "", ""]
notes2 = ["F#2", "C#3", "G3",  "B3",  "C#4", "F#5", "", "", "", "", "", "", ""]
notes3 = ["G#2", "E3",  "F#3", "C#4", "F#4", "G#5", "", "", "", "", "", "", "", ""]
notes4 = ["G2",  "D3",  "E3",  "A4",  "B4",  "A5",  "", "", "", "", "", "", "", "", ""]
notes5 = ["D2",  "A3",  "F#3", "B4",  "C#4", "F#5", "", "", "", "", "", "", "", "", ""]
notes6 = ["E2",  "B3",  "E3",  "A4",  "D#4", "E5",  "", "", "", "", "", "", "", "", ""]

S.setinstrument("electric guitar (jazz)", 0)
S.setinstrument("acoustic grand piano", 1)
S.setinstrument("soprano sax", 2)
S.setinstrument("vibraphone", 3)
S.setinstrument("shakuhachi", 4)
S.setinstrument("pizzicato strings", 5)
S.setinstrument("pan flute", 6)
S.setinstrument("electric bass (finger)", 7)
S.setinstrument("electric piano 2", 8)
S.setinstrument("acoustic guitar (nylon)", 9)
S.setinstrument("church organ", 10)
S.setinstrument("music box", 11)
S.setinstrument("cello", 12)
S.setinstrument("acoustic bass", 13)
S.setinstrument("orchestral harp", 14)


for i in range(250):
    S.add(random.choice(notes1), random.uniform(0.8, 5.5), random.randint(0, 14), random.randint(52, 127))
    if random.random() < 0.125:
        S.adddrum(random.randint(35, 59), random.uniform(0.1, 1.5), random.randint(52, 126))

for i in range(250):
    S.add(random.choice(notes2), random.uniform(1, 5.5), random.randint(0, 14), random.randint(52, 117))
    if random.random() < 0.125:
        S.adddrum(random.randint(35, 59), random.uniform(0.2, 1.5), random.randint(52, 116))

for i in range(250):
    S.add(random.choice(notes3), random.uniform(1.2, 5.5), random.randint(0, 14), random.randint(52, 107))
    if random.random() < 0.125:
        S.adddrum(random.randint(35, 59), random.uniform(0.3, 1.5), random.randint(52, 106))

for i in range(250):
    S.add(random.choice(notes4), random.uniform(1.4, 5.5), random.randint(0, 14), random.randint(52, 97))
    if random.random() < 0.125:
        S.adddrum(random.randint(35, 59), random.uniform(0.4, 1.5), random.randint(52, 96))

for i in range(250):
    S.add(random.choice(notes5), random.uniform(1.6, 5.5), random.randint(0, 14), random.randint(52, 87))
    if random.random() < 0.125:
        S.adddrum(random.randint(35, 59), random.uniform(0.5, 1.5), random.randint(52, 86))

for i in range(250):
    S.add(random.choice(notes6), random.uniform(1.8, 5.5), random.randint(0, 14), random.randint(52, 77))
    if random.random() < 0.125:
        S.adddrum(random.randint(35, 59), random.uniform(0.6, 1.5), random.randint(52, 76))


S.writefile("test3.mid")
