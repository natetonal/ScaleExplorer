import json
from itertools import product
from constants import *


class ScaleUtility:
    """ A utility for working directly with the ScalesLibrary JSON file. """

    def __init__(self):
        """ Converts the raw source JSON to a complete and formatted JSON file for use in the program. """

        # The app will use 'scale strings', a binary string that represents all 12 possible tones of a scale.
        # Start by generating a list of every permutation of a binary string of length 12.
        scale_strings = []
        for string in sorted(list(product(SEED, repeat=MAX_SCALE_LENGTH))):
            scale_strings.append(''.join(string))

        # Read in the raw JSON file.
        with open('scales.json', 'r') as infile:
            scales = json.load(infile)

        # Storage space for the new JSON file.
        all_scales = {}

        # Merge the source JSON with the scale string combinations to create the data.
        for string in scale_strings:
            if string in scales:
                scales[string]['length'] = self.scale_length(string)
                scales[string]['scale_code'] = tuple(string)
                scales[string]['leap_pattern'] = self.leap_pattern(string)
                all_scales[string] = scales[string]
            else:
                if self.is_a_scale(string):
                    all_scales[string] = {
                        'name': 'Unknown',
                        'scale_code': tuple(string),
                        'alternate_names': [],
                        'length': self.scale_length(string),
                        'leap_pattern': self.leap_pattern(string)
                    }

        # Write data to the ScaleLibrary JSON file that will be used by program.
        with open('ScaleLibrary.json', 'w') as scale_json:
            json.dump(all_scales, scale_json, sort_keys=True, indent=4)

    @staticmethod
    def is_a_scale(scale):
        """ Checks to make sure this is a valid scale. For the sake of this program, a valid scale
        must have at least 5 notes in it, and the first note must be included. """

        return scale.count('1') >= MIN_SCALE_LENGTH and scale[0] is '1'

    @staticmethod
    def scale_length(scale):
        """ Checks how many notes are in this scale. """

        return scale.count('1')

    @staticmethod
    def leap_pattern(scale):
        """ Returns the numeric leap pattern for this scale, starting with 1. """

        return [i + 1 for i, num in enumerate(scale) if num == '1']


if __name__ == '__main__':
    ScaleUtility()
