class Note:

    def __init__(self, root, acc):
        self._note = root + acc
        self._root = root
        self._accidental = acc

    def get_note(self):
        return self._note

    def get_root(self):
        return self._root

    def get_accidental(self):
        return self._accidental
