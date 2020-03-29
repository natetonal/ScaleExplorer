from constants import *
from note_collection import NoteCollection


class ScaleConverter:
    """ A class that handles the logic of converting the scale binary strings to notes. """

    def __init__(self):

        self._note_collection = NoteCollection()
        self._notes = self._note_collection.get_collection()

        # The order for a scale if flat key offset is > 5.
        self._double_flat_order = [
            self._notes[C][NT], self._notes[D][FL], self._notes[D][NT], self._notes[E][FL],
            self._notes[F][FL], self._notes[F][NT], self._notes[G][FL], self._notes[G][NT],
            self._notes[A][FL], self._notes[B][DF], self._notes[B][FL], self._notes[C][FL]
        ]

        # The default flat order.
        self._flat_order = [
            self._notes[C][NT], self._notes[D][FL], self._notes[D][NT], self._notes[E][FL],
            self._notes[E][NT], self._notes[F][NT], self._notes[G][FL], self._notes[G][NT],
            self._notes[A][FL], self._notes[A][NT], self._notes[B][FL], self._notes[C][FL]
        ]

        # The default order.
        self._default_order = [
            self._notes[C][NT], self._notes[D][FL], self._notes[D][NT], self._notes[E][FL],
            self._notes[E][NT], self._notes[F][NT], self._notes[G][FL], self._notes[G][NT],
            self._notes[A][FL], self._notes[A][NT], self._notes[B][FL], self._notes[B][NT]
        ]

        # The default sharp order.
        self._sharp_order = [
            self._notes[C][NT], self._notes[C][SH], self._notes[D][NT], self._notes[D][SH],
            self._notes[E][NT], self._notes[E][SH], self._notes[F][SH], self._notes[G][NT],
            self._notes[G][SH], self._notes[A][NT], self._notes[A][SH], self._notes[B][NT]
        ]

        # The order of a scale if sharp key offset > 6
        self._double_sharp_order = [
            self._notes[B][SH], self._notes[C][SH], self._notes[C][DS], self._notes[D][SH],
            self._notes[D][DS], self._notes[E][SH], self._notes[F][SH], self._notes[F][DS],
            self._notes[G][SH], self._notes[G][DS], self._notes[A][SH], self._notes[A][DS]
        ]

        # Key orientations and offsets for given key centers.
        self._keys = {
            self._notes[F][FL].get_note(): {'orientation': DF, 'offset': -8, 'note': self._notes[F][FL]},
            self._notes[C][FL].get_note(): {'orientation': DF, 'offset': -7, 'note': self._notes[C][FL]},
            self._notes[G][FL].get_note(): {'orientation': DF, 'offset': -6, 'note': self._notes[G][FL]},
            self._notes[D][FL].get_note(): {'orientation': FL, 'offset': -5, 'note': self._notes[D][FL]},
            self._notes[A][FL].get_note(): {'orientation': FL, 'offset': -4, 'note': self._notes[A][FL]},
            self._notes[E][FL].get_note(): {'orientation': FL, 'offset': -3, 'note': self._notes[E][FL]},
            self._notes[B][FL].get_note(): {'orientation': FL, 'offset': -2, 'note': self._notes[B][FL]},
            self._notes[F][NT].get_note(): {'orientation': FL, 'offset': -1, 'note': self._notes[F][NT]},
            self._notes[C][NT].get_note(): {'orientation': C,  'offset': 0, 'note': self._notes[C][NT]},
            self._notes[G][NT].get_note(): {'orientation': SH, 'offset': 1, 'note': self._notes[G][NT]},
            self._notes[D][NT].get_note(): {'orientation': SH, 'offset': 2, 'note': self._notes[D][NT]},
            self._notes[A][NT].get_note(): {'orientation': SH, 'offset': 3, 'note': self._notes[A][NT]},
            self._notes[E][NT].get_note(): {'orientation': SH, 'offset': 4, 'note': self._notes[E][NT]},
            self._notes[B][NT].get_note(): {'orientation': SH, 'offset': 5, 'note': self._notes[B][NT]},
            self._notes[F][SH].get_note(): {'orientation': SH, 'offset': 6, 'note': self._notes[F][SH]},
            self._notes[C][SH].get_note(): {'orientation': DS, 'offset': 7, 'note': self._notes[C][SH]},
            self._notes[G][SH].get_note(): {'orientation': DS, 'offset': 8, 'note': self._notes[G][SH]},
            self._notes[D][SH].get_note(): {'orientation': DS, 'offset': 9, 'note': self._notes[D][SH]},
            self._notes[A][SH].get_note(): {'orientation': DS, 'offset': 10, 'note': self._notes[A][SH]},
            self._notes[E][SH].get_note(): {'orientation': DS, 'offset': 11, 'note': self._notes[E][SH]},
            self._notes[B][SH].get_note(): {'orientation': DS, 'offset': 12, 'note': self._notes[B][SH]},
        }

        # Order mapping by key orientation.
        self._order_map = {
            DF: self._double_flat_order,
            FL: self._flat_order,
            C:  self._default_order,
            SH: self._sharp_order,
            DS: self._double_sharp_order
        }

    def get_note_collection(self):
        """ Returns the NoteCollection object. """

        return self._note_collection

    def get_keys_by_note(self):
        """ Returns a list of all the available keys by their Note object. """

        return [value['note'] for value in self._keys.values()]

    def convert_scale(self, scale, root, acc=NT):
        """ Returns a list containing the valid notes of a scale given its key center. """

        scale_order = self.get_note_order_by_key(root, acc)
        if scale_order is None:
            return None

        converted_scale = []

        for i, num in enumerate(scale.get_scale_code()):
            if num == NOTE_ON:
                converted_scale.append(scale_order[i])

        return converted_scale

    def get_note_order_by_key(self, root, acc=NT):
        """ Returns the correct note order map given a root and accidental. """

        # Return the correct order map for this key.
        try:
            order_map = self._order_map[self._keys[root + acc]['orientation']]
        except KeyError:
            print(KEY_ERROR)
            return None

        # Get the index of this key in the order map.
        for i, note in enumerate(order_map):
            if note.get_note() == self._note_collection.get_note(root, acc):
                return order_map[i:] + order_map[:i]

        print(VALUE_ERROR)
        return None



