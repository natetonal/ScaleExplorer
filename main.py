import json
from itertools import product
from pprint import pprint

class ScaleExplorer:

    def __init__(self):

        scale_strings = []
        for string in sorted(list(product('10', repeat=12))):
            scale_strings.append(''.join(string))

        with open('scales.json', 'r') as infile:
            scales = json.load(infile)
        print(scales)

        all_scales = {}

        for string in scale_strings:
            if string in scales:
                this_scale = scales[string]
                this_scale['length'] = self.scale_length(string)
                all_scales[string] = this_scale
            else:
                if self.is_a_scale(string):
                    all_scales[string] = {
                        'name': 'Unknown',
                        'alternate_names': [],
                        'length': self.scale_length(string)
                    }

        with open('ScaleLibrary.json', 'w') as scale_json:
            json.dump(all_scales, scale_json, sort_keys=True, indent=4)

    @staticmethod
    def is_a_scale(scale):
        return scale.count('1') >= 2

    @staticmethod
    def scale_length(scale):
        return scale.count('1')


if __name__ == '__main__':
    ScaleExplorer()
