class Scale:

    def __init__(self, scale_id, scale):
        self._scale_id = scale_id
        self._scale_code = tuple(scale['scale_code'])
        self._length = scale['length']
        self._name = scale['name']
        self._alternate_names = scale['alternate_names']
        self._formatted_alt_names = self.format_alt_names()
        self._leap_pattern = scale['leap_pattern']

    def __len__(self):
        return self._length

    def get_scale_id(self):
        return self._scale_id

    def get_scale_code(self):
        return self._scale_code

    def get_name(self):
        return self._name

    def get_leap_pattern(self):
        return self._leap_pattern

    def get_alternate_names(self):
        if len(self._alternate_names) > 0:
            return self._alternate_names

        return None

    def get_formatted_alt_names(self):
        return self._formatted_alt_names

    def format_alt_names(self):
        if len(self._alternate_names) is 0:
            return "None."
        else:
            return ", ".join([alt for alt in self._alternate_names])


