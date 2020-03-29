import json
import music21
import PySimpleGUI as sg
from constants import *

from scale_collection import ScaleCollection
from scale_converter import ScaleConverter


class ScaleExplorer:

    def __init__(self):
        """ The main program initializer that oversees all interactions with the application. """

        # The app should initialize with the ScaleLibrary JSON file.
        try:
            with open('ScaleLibrary.json', 'r') as infile:
                data = json.load(infile)
                self.scales = ScaleCollection(data)

        # If ScaleLibrary isn't there, throw an error and exit.
        except FileNotFoundError:
            print(ERROR_1)
            return

        # Main Data Members
        self._converter = ScaleConverter()
        self._note_collection = self._converter.get_note_collection()
        self._keys = self._converter.get_keys_by_note()

        # UI Immutable Data Members
        self._keys_for_display = tuple([note.get_longname() for note in self._keys])
        self._default_key = 6

        # UI Mutable Data Members
        self.scales_for_display = self.scales.get_scales()
        self.selected_key = self._keys[self._default_key] # You changed this from long name to note.
        self.note_opts_by_key = self._converter.get_note_order_by_key(
            root=self._keys[self._default_key].get_root(), acc=self._keys[self._default_key].get_accidental()
        )

        # User Selections
        self.user_selections = {
            'notes': []
        }

        # DEMO - to be removed later
        # some_scales = self.scales.get_scales_of_length(7)
        # for scale in some_scales:
        #     if scale.get_name() != 'Unknown':
        #         print(
        #             f"{scale.get_name()} : {self._converter.convert_scale(scale, B, FL)}, leap pattern: {scale.get_leap_pattern()}")
        ###

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
        adjusted_full = full_width + full_size + half_size

        note_nums = ('Any', '5', '6', '7', '8', '9', '10', '11', '12')

        # Row 1 columns
        col_topleft = [
            [sg.Text('Key: ', size=(half_size, 1))],
            [sg.Drop(self._keys_for_display,
                     default_value=self.selected_key.get_longname(),
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

        # TODO: NOTE SELECTION FUNCTIONALITY - Save for later
        # Row 2
        # layout_two = [[
        #     sg.Checkbox(self.note_opts_by_key[1].get_shortname(), size=(cb_size, 1), enable_events=True, key='R2_NOTE1'),
        #     sg.Checkbox(self.note_opts_by_key[2].get_shortname(), size=(cb_size, 1),enable_events=True, key='R2_NOTE2'),
        #     sg.Checkbox(self.note_opts_by_key[3].get_shortname(), size=(cb_size, 1),enable_events=True, key='R2_NOTE3'),
        #     sg.Checkbox(self.note_opts_by_key[4].get_shortname(), size=(cb_size, 1),enable_events=True, key='R2_NOTE4'),
        #     sg.Checkbox(self.note_opts_by_key[5].get_shortname(), size=(cb_size, 1),enable_events=True, key='R2_NOTE5'),
        #     sg.Checkbox(self.note_opts_by_key[6].get_shortname(), size=(cb_size, 1),enable_events=True, key='R2_NOTE6'),
        #     sg.Checkbox(self.note_opts_by_key[7].get_shortname(), size=(cb_size, 1),enable_events=True, key='R2_NOTE7'),
        #     sg.Checkbox(self.note_opts_by_key[8].get_shortname(), size=(cb_size, 1),enable_events=True, key='R2_NOTE8'),
        #     sg.Checkbox(self.note_opts_by_key[9].get_shortname(), size=(cb_size, 1),enable_events=True, key='R2_NOTE9'),
        #     sg.Checkbox(self.note_opts_by_key[10].get_shortname(), size=(cb_size, 1),enable_events=True, key='R2_NOTE10'),
        #     sg.Checkbox(self.note_opts_by_key[11].get_shortname(), size=(cb_size, 1),enable_events=True, key='R2_NOTE11'),
        # ]]

        scale_header_size = 32
        scale_subheader_size = 16
        scale_list_font_size = 24
        scale_list_size = 39
        mini_bar_size = 40
        mini_bar_color = '#dddddd'
        scale_bg_color = '#222222'
        scale_alt_text = 'orange'
        button_pdf_color = '#00e676'
        button_muse_color = '#2fa4e7'

        # The list to hold the scale display tiles.
        scale_layout = []

        # Cycle through scales_for_display and generate scale tiles for display to user.
        # TODO: Auto-Refresh by groups of 10 (Use Generator)
        for i, scale in enumerate(self.scales_for_display.values(), 1):

            # Convert each scale to the selected key.
            converted_scale = [sc for sc in self._converter.convert_scale(
                scale, self.selected_key.get_root(), self.selected_key.get_accidental())]

            # Format the alternate names for scale for display.
            alternate_names = ""
            if scale.get_alternate_names() is None:
                alternate_names = "None."
            else:
                alternate_names = ", ".join([alt for alt in scale.get_alternate_names()])

            # Get a formatted string of the notes of this scale for the given key.
            scale_notes = ", ".join([nt.get_shortname() for nt in converted_scale])

            # Create this scale tile.
            this_scale = [
                [sg.Text('' + str(i) + '. ' + scale.get_name(),
                         background_color=scale_bg_color,
                         font=('Lato', scale_header_size),
                         key=SC_TITLE + str(i))],
                [sg.Text('Alternate Names: ',
                         background_color=scale_bg_color,
                         text_color=scale_alt_text,
                         font=('Lato', scale_subheader_size)),
                 sg.Text(alternate_names,
                         background_color=scale_bg_color,
                         font=('Lato', scale_subheader_size),
                         key=SC_ALTS + str(i))],
                [sg.Text('_' * mini_bar_size,
                         background_color=scale_bg_color,
                         text_color=mini_bar_color)],
                [sg.Text(scale_notes,
                         background_color=scale_bg_color,
                         font=('Lato', scale_list_font_size),
                         size=(scale_list_size, 1),
                         key=SC_NOTES + str(i)),
                 sg.Button('View as PDF',
                           button_color=('white', button_pdf_color),
                           enable_events=True,
                           key=SC_PDF_BTN + str(i)),
                 sg.Button('Load in MuseScore',
                           button_color=('white', button_muse_color),
                           enable_events=True,
                           key=SC_MUSE_BTN + str(i))]
            ]

            scale_layout.append([sg.Column(
                this_scale,
                background_color=scale_bg_color,
                pad=(0, 10),
                key=SC_COLUMN + str(i))
            ])

            if i > 10:
                break

        layout = [
            layout_one,
            [sg.Text('_' * adjusted_full)],
            # TODO: NOTE SELECTION FUNCTIONALITY - Save for later
            # [sg.Frame('Notes to include (Leave unchecked for all): ', layout_two,
            #           pad=(50, 3), element_justification='center')],
            # [sg.Text('_' * adjusted_full)],
            [sg.Column(scale_layout, scrollable=True, vertical_scroll_only=True)]
        ]

        window = sg.Window('Scale Explorer v1.0', layout, default_element_size=(half_size, 1))
        while True:
            event, values = window.read()

            if event in (None, 'Exit'):
                break
            # TODO: NOTE SELECTION FUNCTIONALITY - Save for later
            # if 'R1_KEY' in event:
            #     self.update_note_selections(values[event])
            #     for i in range(1, MAX_SCALE_LENGTH):
            #         text = self.note_opts_by_key[i].get_shortname()
            #         window[R2_NOTE + str(i)].update(text=text)

        window.close()

    def update_note_options_by_key(self, selected_key):
        """ Takes the selected Note object as a parameter and updates the selected key and note selection options
        data members from it. """

        self.selected_key = selected_key
        self.note_opts_by_key = self._converter.get_note_order_by_key(
            root=selected_key.get_root(), acc=selected_key.get_accidental())

    # Can probably get rid of this.
    def update_note_selections(self, selected_key):
        """ Updates the names of the notes the user can select in the note options menu based on the chosen key. """

        self.update_note_options_by_key(selected_key)


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

