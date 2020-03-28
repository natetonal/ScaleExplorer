import json
from constants import *

from scale_collection import ScaleCollection
from scale_converter import ScaleConverter


class ScaleExplorer:

    def __init__(self):
        """ The main program initializer that oversees all interactions with the application. """

        self.converter = ScaleConverter()

        # The app should initialize with the ScaleLibrary JSON file.
        try:
            with open('ScaleLibrary.json', 'r') as infile:
                data = json.load(infile)
                self.scales = ScaleCollection(data)

        # If ScaleLibrary isn't there, throw an error and exit.
        except FileNotFoundError:
            print(ERROR_1)
            return

        some_scales = self.scales.get_scales_of_length(7)
        for scale in some_scales:
            if scale.get_name() != 'Unknown':
                print(f"{scale.get_name()} : {self.converter.convert_scale(scale, B, FL)}, leap pattern: {scale.get_leap_pattern()}")



if __name__ == '__main__':
    ScaleExplorer()
