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
        self._max_scale_display = 10

        # UI Mutable Data Members
        self.scales_for_display = self.scales.get_scales_as_list()
        self.selected_key = self._keys[self._default_key]  # You changed this from long name to note.
        self.note_opts_by_key = self._converter.get_note_order_by_key(
            root=self._keys[self._default_key].get_root(), acc=self._keys[self._default_key].get_accidental()
        )

        self.display_gui()

    def display_gui(self):
        """ The method that displays the GUI to the user. """

        # Set basic theme options.
        sg.theme('Black')
        sg.SetOptions(font=("Lato", 14))

        # Global sizing options
        full_width = 80
        full_size = int(full_width / 2)
        half_size = int(full_size / 2)
        adjusted_full = full_width + full_size + half_size

        # Element-specific definitions
        cb_size = 6

        # Scale style definitions
        scale_header_font_size = 32
        scale_header_size = 40
        scale_subheader_size = 16
        scale_list_font_size = 18
        scale_list_size = 52
        mini_bar_font_size = 8
        mini_bar_size = 80
        mini_bar_color = '#dddddd'
        scale_bg_color = '#222222'
        scale_alt_text = 'orange'
        button_pdf_color = '#00e676'
        button_muse_color = '#2fa4e7'

        note_nums = (ANY, '5', '6', '7', '8', '9', '10', '11', '12')

        # Row 1 - Key selection combo box.
        col_topleft = [
            [sg.Text('Key: ', size=(half_size, 1))],
            [sg.Drop(self._keys_for_display,
                     default_value=self.selected_key.get_longname(),
                     enable_events=True,
                     size=(half_size, 1),
                     key='R1_KEY')]
        ]

        # Row 1 - Note count selection combo box.
        col_topmid = [
            [sg.Text('# of Notes: ', size=(half_size, 1))],
            [sg.Drop(
                note_nums,
                default_value=note_nums[0],
                enable_events=True,
                size=(half_size, 1),
                key='R1_NOTECOUNT')]
        ]

        # Row 1 - Search box.
        col_topright = [
            [sg.Text('Search: ', size=(full_size, 1))],
            [sg.In(size=(full_size, 1), enable_events=True, key='R1_SEARCH')]
        ]

        # Row 1 - Combined layout.
        layout_one = [
            sg.Column(col_topleft),
            sg.Column(col_topmid),
            sg.VerticalSeparator(),
            sg.Column(col_topright)
        ]

        # Row 2
        checkboxes = [[]]

        # Cycle through all the note choices by key and create a checkbox for them.
        for i in range(1, MAX_SCALE_LENGTH):
            checkboxes[0].append(
                sg.Checkbox(self.note_opts_by_key[i].get_shortname(),
                            size=(cb_size, 1),
                            enable_events=True,
                            disabled=True,
                            key=R2_NOTE + str(i))
            )

        layout_two = [sg.Frame(
                        'Notes to include (Feature coming soon!): ',
                        checkboxes,
                        pad=(50, 3),
                        element_justification='center'
        )]

        # The list to hold the scale display tiles.
        scale_layout = []

        # Cycle through scales_for_display and generate scale tiles for display to user.
        for i, scale in enumerate(self.scales_for_display, 1):

            # Convert each scale to the selected key.
            converted_scale = self._converter.convert_scale(
                scale, self.selected_key.get_root(), self.selected_key.get_accidental())

            # Get a formatted string of the notes of this scale for the given key.
            scale_notes = ", ".join([nt.get_shortname() for nt in converted_scale])

            # Create this scale tile.
            this_scale = [
                [sg.Text('' + str(i) + '. ' + scale.get_name(),
                         background_color=scale_bg_color,
                         size=(scale_header_size, 1),
                         font=('Lato', scale_header_font_size),
                         key=SC_TITLE + str(i))],
                [sg.Text('Alternate Names: ',
                         background_color=scale_bg_color,
                         pad=(0, 0),
                         text_color=scale_alt_text,
                         font=('Lato', scale_subheader_size)),
                 sg.Text(scale.get_formatted_alt_names(),
                         background_color=scale_bg_color,
                         pad=(0, 0),
                         size=(70, 1),
                         font=('Lato', scale_subheader_size),
                         key=SC_ALTS + str(i))],
                [sg.Text('Number of notes: ',
                         background_color=scale_bg_color,
                         pad=(0, 0),
                         text_color=scale_alt_text,
                         font=('Lato', scale_subheader_size)),
                 sg.Text(str(len(scale)),
                         background_color=scale_bg_color,
                         pad=(0, 0),
                         font=('Lato', scale_subheader_size),
                         key=SC_COUNT + str(i))],
                [sg.Text('_' * mini_bar_size,
                         pad=(0, 0),
                         background_color=scale_bg_color,
                         font=('Lato', mini_bar_font_size),
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

            # Append this scale as a column to the scale_layout.
            scale_layout.append([sg.Column(
                this_scale,
                background_color=scale_bg_color,
                pad=(0, 10),
                key=SC_COLUMN + str(i))
            ])

            # TODO: Auto-Refresh by groups of 10 (Use Generator)
            # For now, break after 10 scales have loaded.
            if i > self._max_scale_display:
                break

        # Display to use when no scales are found (hidden by default)
        no_scales_found = [
            sg.Text(
                '\nNo scales found. Try revising your search.',
                font=('Lato', 24),
                key=SC_EMPTY,
                size=(58, 3),
                justification='center',
                visible=False,
                background_color=scale_bg_color
            )]

        # The scrollable scale output column (hidden if no scales found)
        scales_display = [
            sg.Column(
                scale_layout,
                key=SC_MAIN,
                scrollable=True,
                visible=True,
                vertical_scroll_only=True
            )]

        # Vertical bar display
        vertical_bar1 = [sg.Text('_' * adjusted_full)]
        vertical_bar2 = [sg.Text('_' * adjusted_full)]

        # Build the GUI layout row by row from above defined rows.
        layout = [
            layout_one,
            vertical_bar1,
            layout_two,
            vertical_bar2,
            no_scales_found,
            scales_display
        ]

        # Attach the GUI Layout to the window and add a title.
        window = sg.Window('Scale Explorer v1.0', layout, default_element_size=(half_size, 1))

        # Event Handler loop.
        while True:

            # Read in any event and values from elements that are registered.
            event, values = window.read()

            # If the user exits, quit the program.
            if event in (None, 'Exit'):
                break

            # If user selected a new key, update the checkbox displays to reflect the new key.
            if R1_KEY in event:
                self.update_note_selections(values[event], window)

            # Use current event-enabled element states to update the GUI (selected key will be updated already).
            self.update_gui(window, values)

        window.close()

    def update_gui(self, window, values):
        """ Updates the GUI after a change has been made by the user. """

        for key in values.keys():
            print(key, values[key])

        # Update the display scales state with the selected note count.
        self.update_scales_by_note_count(values[R1_NOTECOUNT])

        # Update the display scales state with the selected search value.
        self.update_scales_by_search(values[R1_SEARCH])

        # If refining the scales left them empty, then make the error display visible.
        if self.scales_for_display is None:
            window[SC_MAIN].update(visible=False)
            window[SC_EMPTY].update(visible=True)
            return

        # Otherwise, make sure the scales are visible and the empty warning isn't.
        window[SC_MAIN].update(visible=True)
        window[SC_EMPTY].update(visible=False)

        # Otherwise, update each element in the scale column GUI to reflect the new state.
        for i, scale in enumerate(self.scales_for_display, 1):
            # Convert scale to the selected key.
            converted_scale = self._converter.convert_scale(
                scale, self.selected_key.get_root(), self.selected_key.get_accidental())

            # Get a formatted string of the notes of this scale for the given key.
            scale_notes = ", ".join([nt.get_shortname() for nt in converted_scale])

            # Get the scale name and alternate names
            scale_name = scale.get_name()
            scale_alt_names = scale.get_formatted_alt_names()

            window[SC_COLUMN + str(i)].update(visible=True)
            window[SC_TITLE + str(i)].update('' + str(i) + '. ' + scale_name)
            window[SC_ALTS + str(i)].update(scale_alt_names)
            window[SC_COUNT + str(i)].update(len(scale))
            window[SC_NOTES + str(i)].update(scale_notes)

            if i > self._max_scale_display:
                break

        # If there were fewer scales than the maximum scale display, then hide the other scales.
        if len(self.scales_for_display) < self._max_scale_display:
            for i in range(len(self.scales_for_display) + 1, self._max_scale_display + 2):
                window[SC_COLUMN + str(i)].update(visible=False)

        window.refresh()

    def update_scales_by_search(self, search):
        """ Updates the scales to be displayed with only those matching (or partial matching) the given search. """

        # Strip any whitespace from left & right side of string.
        search_str = search.strip()

        # If the search box or scales list is empty, no updating needs to be done.
        if not search_str or not self.scales_for_display:
            return

        # Otherwise, search for valid matches.
        self.scales_for_display = self.scales.get_scales_with_substring(search_str, self.scales_for_display)

    def update_scales_by_note_count(self, note_count):
        """ Updates the scales to be displayed given the current user note count selection. """

        # If 'ANY' is selected, then reset scale_list to master list.
        if note_count is ANY:
            self.scales_for_display = self.scales.get_scales_as_list()
            return

        # Otherwise, set scales to only include ones with this note count.
        self.scales_for_display = self.scales.get_scales_of_length(int(note_count))

    def update_note_selections(self, selected_note, window):
        """ Updates the GUI's note selection row with note names given by the selected key. """

        # Get the Note object referenced by the user's selection and set as selected key.
        self.selected_key = self._note_collection.get_note_by_longname(selected_note)

        # Get the sequence of notes corresponding to the selected key.
        self.note_opts_by_key = self._converter.get_note_order_by_key(
            root=self.selected_key.get_root(), acc=self.selected_key.get_accidental())

        # Update the GUI checkbox labels with the short name of each note.
        for i in range(1, MAX_SCALE_LENGTH):
            text = self.note_opts_by_key[i].get_shortname()
            window[R2_NOTE + str(i)].update(text=text)


if __name__ == '__main__':
    ScaleExplorer()

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
