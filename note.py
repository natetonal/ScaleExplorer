from constants import (
    NT, NT_SHORT, NT_LONG,
    SH, SH_SHORT, SH_LONG,
    FL, FL_SHORT, FL_LONG,
    DF, DF_SHORT, DF_LONG,
    DS, DS_SHORT, DS_LONG
)


class Note:

    def __init__(self, root, acc):
        self._note = root + acc
        self._root = root
        self._accidental = acc
        self._shortname = self._create_shortname(root, acc)
        self._longname = self._create_longname(root, acc)

        # A mapping for generating short & long names for notes from the root & acc.
        self._namemap = {
            NT: (NT_SHORT, NT_LONG),
            SH: (SH_SHORT, SH_LONG),
            FL: (FL_SHORT, FL_LONG),
            DF: (DF_SHORT, DF_LONG),
            DS: (DS_SHORT, DS_LONG)
        }

    def get_note(self):
        return self._note

    def get_root(self):
        return self._root

    def get_accidental(self):
        return self._accidental

    def get_shortname(self):
        return self._shortname

    def get_longname(self):
        return self._longname

    def _create_shortname(self, root, acc):
        """ Creates a displayable abbreviated name for this note. """

        return root + self._namemap[acc][0]

    def _create_longname(self, root, acc):
        """ Creates a displayable full name for this note. """

        return root + " " + self._namemap[acc][1]
