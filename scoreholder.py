"""
Holds an easier-to-use internal representation of some music, which can then
be outputted as actual MIDI.
"""
import re
from midiutil import MIDIFile


PITCH_RE = re.compile(r'([A-Ga-g])(bb|b|#|x)(-1|[0-9])')
PITCH_NAME_OFFSETS = {
    "C": 0,
    "D": 2,
    "E": 4,
    "F": 5,
    "G": 7,
    "A": 9,
    "B": 11
}
PITCH_ACCIDENTAL_OFFSETS = {
    "bb": -2,
    "b": -1,
    "#": 1,
    "x": 2
}
INSTRUMENT_NAMES = {
    "acoustic grand piano": 0,
    "bright acoustic piano": 1,
    "electric grand piano": 2,
    "honky-tonk piano": 3,
    "electric piano 1": 4,
    "electric piano 2": 5,
    "harpsichord": 6,
    "clavi": 7,
    "celesta": 8,
    "glockenspiel": 9,
    "music box": 10,
    "vibraphone": 11,
    "marimba": 12,
    "xylophone": 13,
    "tubular bells": 14,
    "dulcimer": 15,
    "drawbar organ": 16,
    "percussive organ": 17,
    "rock organ": 18,
    "church organ": 19,
    "reed organ": 20,
    "accordion": 21,
    "harmonica": 22,
    "tango accordion": 23,
    "acoustic guitar (nylon)": 24,
    "acoustic guitar (steel)": 25,
    "electric guitar (jazz)": 26,
    "electric guitar (clean)": 27,
    "electric guitar (muted)": 28,
    "overdriven guitar": 29,
    "distortion guitar": 30,
    "guitar harmonics": 31,
    "acoustic bass": 32,
    "electric bass (finger)": 33,
    "electric bass (pick)": 34,
    "fretless bass": 35,
    "slap bass 1": 36,
    "slap bass 2": 37,
    "synth bass 1": 38,
    "synth bass 2": 39,
    "violin": 40,
    "viola": 41,
    "cello": 42,
    "contrabass": 43,
    "tremolo strings": 44,
    "pizzicato strings": 45,
    "orchestral harp": 46,
    "timpani": 47,
    "string ensemble 1": 48,
    "string ensemble 2": 49,
    "synthstrings 1": 50,
    "synthstrings 2": 51,
    "choir aahs": 52,
    "voice oohs": 53,
    "synth voice": 54,
    "orchestra hit": 55,
    "trumpet": 56,
    "trombone": 57,
    "tuba": 58,
    "muted trumpet": 59,
    "french horn": 60,
    "brass section": 61,
    "synthbrass 1": 62,
    "synthbrass 2": 63,
    "soprano sax": 64,
    "alto sax": 65,
    "tenor sax": 66,
    "baritone sax": 67,
    "oboe": 68,
    "english horn": 69,
    "bassoon": 70,
    "clarinet": 71,
    "piccolo": 72,
    "flute": 73,
    "recorder": 74,
    "pan flute": 75,
    "blown bottle": 76,
    "shakuhachi": 77,
    "whistle": 78,
    "ocarina": 79,
    "lead 1 (square)": 80,
    "lead 2 (sawtooth)": 81,
    "lead 3 (calliope)": 82,
    "lead 4 (chiff)": 83,
    "lead 5 (charang)": 84,
    "lead 6 (voice)": 85,
    "lead 7 (fifths)": 86,
    "lead 8 (bass + lead)": 87,
    "pad 1 (new age)": 88,
    "pad 2 (warm)": 89,
    "pad 3 (polysynth)": 90,
    "pad 4 (choir)": 91,
    "pad 5 (bowed)": 92,
    "pad 6 (metallic)": 93,
    "pad 7 (halo)": 94,
    "pad 8 (sweep)": 95,
    "fx 1 (rain)": 96,
    "fx 2 (soundtrack)": 97,
    "fx 3 (crystal)": 98,
    "fx 4 (atmosphere)": 99,
    "fx 5 (brightness)": 100,
    "fx 6 (goblins)": 101,
    "fx 7 (echoes)": 102,
    "fx 8 (sci-fi)": 103,
    "sitar": 104,
    "banjo": 105,
    "shamisen": 106,
    "koto": 107,
    "kalimba": 108,
    "bag pipe": 109,
    "fiddle": 110,
    "shanai": 111,
    "tinkle bell": 112,
    "agogo": 113,
    "steel drums": 114,
    "woodblock": 115,
    "taiko drum": 116,
    "melodic tom": 117,
    "synth drum": 118,
    "reverse cymbal": 119,
    "guitar fret noise": 120,
    "breath noise": 121,
    "seashore": 122,
    "bird tweet": 123,
    "telephone ring": 124,
    "helicopter": 125,
    "applause": 126,
    "gunshot": 127
}


class Note:
    """ Struct holding pitch, duration, and volume. """

    def __init__(self, pitch, duration, volume):
        if isinstance(pitch, str):
            pitchmatch = PITCH_RE.fullmatch(pitch)
            if pitchmatch:
                pitchletter = pitchmatch.group(1).upper()
                pitchaccidental = pitchmatch.group(2)
                pitchoctave = int(pitchmatch.group(3))

                notenum = 12 * (pitchoctave + 1)
                notenum += PITCH_NAME_OFFSETS[pitchletter]

                pitch = notenum + PITCH_ACCIDENTAL_OFFSETS[pitchaccidental]
            elif pitch == "" or pitch.lower() == "r":
                pitch = -1
            else:
                raise ValueError("Bad pitch name: " + pitch)
        else:
            pitch = int(pitch)
            if pitch > 127:
                raise ValueError("Bad pitch value: " + str(pitch))
        self.pitch = pitch
        self.duration = float(duration)
        if volume > 127:
            raise ValueError("volume must be in the interval [0, 127]")
        self.volume = int(volume)


class ScoreHolder:
    """
    Holds an easier-to-use internal representation of the music, which can then
    be outputted as actual MIDI.
    """

    def __init__(self, tempo=120):
        self.tempo = tempo
        self.voices = [None] * 16
        self.instruments = [1] * 16

    def hasvoice(self, voice=0):
        """
        Takes an integer ``voice`` and returns a bool indicating whether or not
        a voice of that number has been initialized.
        """
        if voice < 0 or voice > 15:
            return False
        return self.voices[voice] is not None

    def add(self, pitch, duration=1, voice=0, volume=96):
        """
        Adds a note to the end of one of the voices.

        ``pitch``: string or integer indicating the pitch of the note.
        Integers are in the range [0, 127] for pitches and -1 for rests, and
        pitch strings are denoted either as ``""`` or ``"r"`` for a rest, and
        using scientific notation for actual pitches, e.g. ``"Gb3"``, ``"Cx1"``.

        ``duration``: float or Fraction indicating the duration of the note,
        in beats.

        ``voice``: integer indicating which voice this note is to be added to.

        ``volume``: integer in the range [0, 127] denoting volume of the note.
        """

        if not self.hasvoice(voice):
            self.addat(0, pitch, duration, voice, volume)
        else:
            self.addat(len(self.voices[voice]), pitch, duration, voice, volume)

    def addat(self, index, pitch, duration=1, voice=0, volume=96):
        """
        Adds a note to one of the voices at the specified index.

        ``pitch``: string or integer indicating the pitch of the note.
        Integers are in the range [0, 127] for pitches and -1 for rests, and
        pitch strings are denoted either as ``""`` or ``"r"`` for a rest, and
        using scientific notation for actual pitches, e.g. ``"Gb3"``, ``"Cx1"``.

        ``duration``: float or Fraction indicating the duration of the note,
        in beats.

        ``voice``: integer indicating which voice this note is to be added to.

        ``volume``: integer in the range [0, 127] denoting volume of the note.
        """
        voice = int(voice)
        if voice < 0 or voice > 15:
            raise ValueError(
                "voice must be an integer in the range [0, 15]. Instead got: " +
                str(voice)
            )

        if not self.hasvoice(voice):
            self.voices[voice] = []

        self.voices[voice].insert(index, Note(pitch, duration, volume))

    def remove(self, voice=0):
        """ Removes the last note in a given voice and returns it. """
        return self.removeat(-1, voice)

    def removeat(self, index, voice=0):
        """
        Removes the note in a voice that is at a given index and returns it.
        """
        if not self.hasvoice(voice):
            raise IndexError("No such voice " + str(voice))

        try:
            return self.voices[voice].pop(index)
        except IndexError:
            raise IndexError(
                "Invalid index " + str(index) +
                " in voice " + str(voice)
            )

    def setinstrument(self, instrument, voice=0):
        """
        Sets the General MIDI instrument of a given voice.

        ``instrument`` is either an integer specifying the instrument,
        or a (case insensitive) string with that instrument's name.
        """
        voice = int(voice)
        if voice < 0 or voice > 15:
            raise ValueError(
                "voice must be an integer in the range [0, 15]. Instead got: " +
                str(voice)
            )

        if isinstance(instrument, int):
            self.instruments[voice] = instrument
        else:
            instrument = str(instrument).lower()
            if instrument in INSTRUMENT_NAMES:
                self.instruments[voice] = INSTRUMENT_NAMES[instrument]
            else:
                raise ValueError("No such instrument named " + instrument)

    def writefile(self, filepath):
        """
        Writes the current internal musical representation to the file
        specified by ``filepath``.
        """
        midi = MIDIFile(sum(1 for v in self.voices if v), True, True, True, 1)

        i = -1
        for vindex in range(len(self.voices)):
            voice = self.voices[vindex]
            if not voice:
                continue
            i += 1
            time = 0.0
            midi.addTempo(i, 0, self.tempo)
            midi.addProgramChange(i, i, 0, self.instruments[vindex])
            for note in voice:
                if note.pitch >= 0:
                    midi.addNote(
                        i, i, note.pitch, time, note.duration, note.volume
                    )
                time += note.duration

        with open(filepath, "wb") as outputfile:
            midi.writeFile(outputfile)
