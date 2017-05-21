""" testerino salcino """
from fractions import Fraction as Frac
from scoreholder import ScoreHolder


S = ScoreHolder(132)  # 132 BPM

S.setinstrument("electric guitar (jazz)", 0)
S.setinstrument("soprano sax", 2)

S.add("Bx4", Frac(1, 2), 0, 127)  # 73
S.add("r",   Frac(1, 2), 2, 0)
S.add("r",   Frac(1, 2), 0, 0)
S.add("Bx4", Frac(1, 2), 2, 111)
S.add("r",   Frac(3, 4), 0, 0)
S.add("r",   Frac(3, 4), 2, 0)
S.add("Db4", Frac(1, 2), 0, 127)  # 61
S.add("r",   Frac(1, 2), 2, 0)
S.add("r",   Frac(1, 2), 0, 0)
S.add("Db4", Frac(1, 2), 2, 111)

S.writefile("test.mid")
