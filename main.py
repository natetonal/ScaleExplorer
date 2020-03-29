import json
import music21
import PySimpleGUI as sg
from constants import *

from scale_collection import ScaleCollection
from scale_converter import ScaleConverter


class ScaleExplorer:

    def __init__(self):
        """ The main program initializer that oversees all interactions with the application. """

        # Main Data Members
        self._converter = ScaleConverter()
        self._note_collection = self._converter.get_note_collection()
        self._keys = self._converter.get_keys_by_note()

        # UI Immutable Data Members
        self._keys_for_display = tuple([note.get_longname() for note in self._keys])
        self._default_key = 6

        # UI Mutable Data Members
        self.selected_key = self._keys_for_display[self._default_key]
        self.note_options_by_key = self._converter.get_note_order_by_key(
            root=self._keys[self._default_key].get_root(), acc=self._keys[self._default_key].get_accidental()
        )

        # User Selections
        self.user_selections = {
            'notes': []
        }

        # The app should initialize with the ScaleLibrary JSON file.
        try:
            with open('ScaleLibrary.json', 'r') as infile:
                data = json.load(infile)
                self.scales = ScaleCollection(data)

        # If ScaleLibrary isn't there, throw an error and exit.
        except FileNotFoundError:
            print(ERROR_1)
            return

        self.display_gui()

    def display_gui(self):
        """ The method that displays the GUI to the user. """

        # Set basic theme options.
        sg.theme('Black')
        sg.SetOptions(font=("Lato", 14))

        # Sizing options
        full_width = 80
        full_size = int(full_width / 2)
        half_size = int(full_size / 2)
        quarter_size = int(half_size / 2)
        adjusted_full = full_width + full_size + half_size

        note_options_by_key = self._keys[6]
        note_nums = ('Any', '5', '6', '7', '8', '9', '10', '11', '12')

        # Row 1 columns
        col_topleft = [
            [sg.Text('Key: ', size=(half_size, 1))],
            [sg.Drop(self._keys_for_display,
                     default_value=self.selected_key,
                     enable_events=True,
                     size=(half_size, 1),
                     key='R1_KEY')]
        ]

        col_topmid = [
            [sg.Text('# of Notes: ', size=(half_size, 1))],
            [sg.Drop(note_nums, default_value=note_nums[0], size=(half_size, 1), key='R1_NOTECOUNT')]
        ]

        col_topright = [
            [sg.Text('Search: ', size=(full_size, 1))],
            [sg.In(size=(full_size, 1), key='R1_SEARCH')]
        ]

        # Row 1
        layout_one = [sg.Column(col_topleft), sg.Column(col_topmid), sg.VerticalSeparator(), sg.Column(col_topright)]

        # Row 2
        layout_two = [[
            sg.Checkbox(self.note_options_by_key[1].get_shortname(), enable_events=True, key='R2_NOTE1'),
            sg.Checkbox(self.note_options_by_key[2].get_shortname(), enable_events=True, key='R2_NOTE2'),
            sg.Checkbox(self.note_options_by_key[3].get_shortname(), enable_events=True, key='R2_NOTE3'),
            sg.Checkbox(self.note_options_by_key[4].get_shortname(), enable_events=True, key='R2_NOTE4'),
            sg.Checkbox(self.note_options_by_key[5].get_shortname(), enable_events=True, key='R2_NOTE5'),
            sg.Checkbox(self.note_options_by_key[6].get_shortname(), enable_events=True, key='R2_NOTE6'),
            sg.Checkbox(self.note_options_by_key[7].get_shortname(), enable_events=True, key='R2_NOTE7'),
            sg.Checkbox(self.note_options_by_key[8].get_shortname(), enable_events=True, key='R2_NOTE8'),
            sg.Checkbox(self.note_options_by_key[9].get_shortname(), enable_events=True, key='R2_NOTE9'),
            sg.Checkbox(self.note_options_by_key[10].get_shortname(), enable_events=True, key='R2_NOTE10'),
            sg.Checkbox(self.note_options_by_key[11].get_shortname(), enable_events=True, key='R2_NOTE11'),
        ]]

        layout = [
            layout_one,
            [sg.Text('_' * adjusted_full)],
            [sg.Frame('Notes to include (Leave unchecked for all): ', layout_two, element_justification='center')],
            [sg.Text('_' * adjusted_full)],

        ]

        window = sg.Window('Scale Explorer v1.0', layout, default_element_size=(half_size, 1))
        while True:
            event, values = window.read()

            if event in (None, 'Exit'):
                break
            if 'R1_KEY' in event:
                print('updating notes')
                self.update_note_selections(values[event])
                for i in range(1, MAX_SCALE_LENGTH):
                    text = self.note_options_by_key[i].get_shortname()
                    print(text)
                    window[R2_NOTE + str(i)].update(text=text)



        window.close()

    def update_note_options_by_key(self, selected_note):
        """ Takes the selected Note object as a parameter and updates the selected key and note selection options
        data members from it. """

        self.selected_key = selected_note.get_longname()
        self.note_options_by_key = self._converter.get_note_order_by_key(
            root=selected_note.get_root(), acc=selected_note.get_accidental())

    def update_note_selections(self, selected_note):
        note = self._note_collection.get_note_by_longname(selected_note)
        self.update_note_options_by_key(note)


if __name__ == '__main__':
    ScaleExplorer()

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

