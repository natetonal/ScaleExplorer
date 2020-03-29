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

    def get_scales_as_list(self):
        """ Returns the values of the Scale collection. """

        scale_values = list(self._scales.values())
        return scale_values

    def get_scale_by_id(self, scale_id):
        """ Returns a Scale object by its scale_id string. """

        if scale_id in self._scales:
            return self._scales[scale_id]

        return None

    def get_scales_with_substring(self, substring, scales=None):
        """ A method that returns a list of all Scale objects matching a substring, or None if none found. """

        # If scale values were not passed in, use the scale collection values.
        if scales is None:
            scales = self._scales.values()

        # Holder for scales with given substring.
        new_scales = []

        # Make comparisons lower-case for easier searching.
        substring = substring.lower()

        # Add any scales with matching substring to new scales list.
        for scale in scales:
            this_scale = scale.get_name()
            if substring in this_scale.lower():
                new_scales.append(scale)
                continue

            # Try and match the string to any of the alternate names for this scale.
            alt_names = scale.get_alternate_names()
            if alt_names is not None:
                for alt_name in alt_names:
                    if substring in alt_name.lower():
                        new_scales.append(scale)
                        continue

        # If there were scales of that length, return the list. Otherwise, return None.
        if len(new_scales) > 0:
            return new_scales

        return None

    def get_scales_of_length(self, length, scales=None):
        """ A method that returns a list of all Scale objects of a given length, or None if none found. """

        # If scale values were not passed in, use the scale collection values.
        if scales is None:
            scales = self._scales.values()

        # If the number entered is out of bounds, return None.
        if length < MIN_SCALE_LENGTH or length > MAX_SCALE_LENGTH:
            return None

        # Holder for scales of given length.
        new_scales = []

        # Add any scales of given length to new scales list.
        for scale in scales:
            if len(scale) == length:
                new_scales.append(scale)

        # If there were scales of that length, return the list. Otherwise, return None.
        if len(new_scales) > 0:
            return new_scales

        return None
