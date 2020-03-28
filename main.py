import json
import music21
import PySimpleGUI as sg
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

        self.update_gui()

    def update_gui(self):
        """ The method that displays the GUI to the user. """

        # Set basic theme options.
        sg.theme('Black')
        sg.SetOptions(font=("Lato", 14))

        # Sizing options
        full_size = 40
        half_size = int(full_size / 2)
        quarter_size = int(half_size / 2)

        keys = tuple(self.converter.get_keys())

        col_topleft = [
            [sg.Text('Key: ', size=(half_size, 1))],
            [sg.Drop(keys, size=(half_size, 1))]
        ]

        col_topmid = [
            [sg.Text('# of Notes: ', size=(half_size, 1))],
            [sg.Drop(('Any', '5', '6', '7', '8', '9', '10', '11', '12'), size=(half_size, 1))]
        ]

        col_topright = [
            [sg.Text('Search: ', size=(full_size, 1))],
            [sg.In('Search by name (eg. \'Phrygian\')', size=(full_size, 1))]
        ]

        layout_top = [sg.Column(col_topleft), sg.Column(col_topmid), sg.VerticalSeparator(), sg.Column(col_topright)]

        layout = [
            [sg.Text('Scale Explorer v1.0', font=('Lato', 26), size=(full_size, 1), justification='center')],
            layout_top
        ]

        window = sg.Window('Scale Explorer v1.0', layout, default_element_size=(half_size, 1), finalize=True)
        event, values = window.read()
        window.close()

        # layout = [[sg.Text('Some text on Row 1', font=("Lato", 20))],
        #           [sg.Text('Enter something on Row 2', font=("Lato", 20)), sg.InputText(font=("Lato", 20))],
        #           [sg.Button('Ok', tooltip='Hi friend', font=("Lato", 20)), sg.Button('Cancel', font=("Lato", 20))]]
        #
        # # Create the Window
        # window = sg.Window('ScaleExplorer v1.0', layout)
        # # Event Loop to process "events" and get the "values" of the inputs
        # while True:
        #     event, values = window.read()
        #     if event in (None, 'Cancel'):  # if user closes window or clicks cancel
        #         break
        #     print('You entered ', values[0])
        #
        # window.close()

        # Short program that uses music21's tools to output a scale to the user through MuseScore.

        # phryg = self.scales.get_scale_by_name("Phrygian")
        # phryg_fsharp = self.converter.convert_scale(phryg, F, SH)
        # phryg_notes = [x.get_note() for x in phryg_fsharp]
        # phryg_name = phryg.get_name()
        #
        # scale_stream = music21.stream.Stream()
        # for note in phryg_notes:
        #     scale_stream.append(music21.note.Note(note))
        # scale_stream.metadata = music21.metadata.Metadata()
        # scale_stream.metadata.title = phryg_name
        # scale_stream.metadata.composer = 'ScaleExplorer v1.0'
        # scale_stream.show()


if __name__ == '__main__':
    ScaleExplorer()
