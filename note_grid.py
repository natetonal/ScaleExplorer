from constants import *


class NoteGrid:
    """ A class that defines a base note and its possible accidentals. """

    def __init__(self, base):
        self._grid = {
            NATURAL: base,
            FLAT: base + FL,
            SHARP: base + SH,
            DOUBLE_FLAT: base + DF,
            DOUBLE_SHARP: base + DS
        }

    def get_note(self, base, mod=None):
        """ Gets the correctly spelled note given """
        if mod is None:
            mod = NATURAL





