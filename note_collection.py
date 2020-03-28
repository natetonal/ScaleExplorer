from constants import *

from note import Note


class NoteCollection:
    """ A class that creates string definitions for all lettered notes. """

    def __init__(self):
        """ Creates a collection of all possible notes using their root and accidental. """

        self._collection = {}
        self._roots = [A, B, C, D, E, F, G]
        self._accidentals = [NT, FL, SH, DF, DS]

        for root in self._roots:
            accs = {}
            for acc in self._accidentals:
                accs[acc] = Note(root, acc)
            self._collection[root] = accs

    def get_collection(self):
        """ Returns the entire Note Collection. """

        return self._collection

    def get_note(self, root, acc=NT):
        """ Retrieves a note given a base and modifier. """

        try:
            key = self._collection[root][acc]
        except KeyError:
            return print(KEY_ERROR)

        return key.get_note()

