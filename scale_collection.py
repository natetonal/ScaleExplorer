from scale import Scale
from constants import MIN_SCALE_LENGTH, MAX_SCALE_LENGTH


class ScaleCollection:
    """ A ScaleCollection holds a collection of Scale objects and has some useful methods to retrieve data from
    the collection. """

    def __init__(self, scales):
        """ Initializes the ScaleCollection from a dictionary of raw scale data and creates/stores a Scale object
        for each one. """

        # A dictionary of Scale objects keyed by their scale_id.
        self._scales = {}

        for key in scales.keys():
            self._scales[key] = Scale(key, scales[key])

    def get_scales(self):
        """ Return the entire Scale collection. """

        return self._scales

    def get_scale_by_id(self, scale_id):
        """ Returns a Scale object by its scale_id string. """

        if scale_id in self._scales:
            return self._scales[scale_id]

        return None

    def get_scale_by_name(self, name):
        """ Returns a Scale object by name (also searching alternate names), or None if none found. """

        for scale in self._scales.values():
            if scale.get_name() == name:
                return scale

            alt_names = scale.get_alternate_names()
            if alt_names is not None and name in alt_names:
                return scale

        return None

    def get_scales_of_length(self, length):
        """ A method that returns a list of all Scale objects of a given length, or None if none found. """

        # If the number entered is out of bounds, return None.
        if length < MIN_SCALE_LENGTH or length > MAX_SCALE_LENGTH:
            return None

        # Holder for scales of given length.
        scales = []

        # Add any scales of given length to scales list.
        for scale in self._scales.values():
            if len(scale) == length:
                scales.append(scale)

        # If there were scales of that length, return the list. Otherwise, return None.
        if len(scales) > 0:
            return scales

        return None
