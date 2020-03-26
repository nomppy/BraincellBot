from mods import vars_


def get_commands(category: str) -> list:
    return vars_.info_[category].keys()


class Info:
    def __init__(self, name, brief, category='Miscellaneous', description=None, usage=None,
                 settings: {str: str} = None,
                 defaults: {str: str} = None):

        if not description:
            description = brief
        self.name = name
        self.brief = brief
        self.category = category
        self.description = description
        self.usage = usage
        self.settings = settings
        self.default = defaults

    def export(self, _dict: dict):
        if self.category in _dict.keys():
            _dict[self.category][self.name] = self
            return

        _dict[self.category] = {self.name: self}

    def configurable(self):
        return self.settings is not None

    def validate_setting(self, field, value):
        if field not in self.settings.keys():
            return False
        elif self.settings[field] is None or self.settings[field] == 'any':
            return True
        elif self.settings[field] == int:
            try:
                int(value)
                return True
            except ValueError:
                return False
        elif value not in self.settings[field]:
            return False

    def get_defaults(self):
        return self.default

    def get_command(self):
        return self

    def get_settings(self):
        return self.settings.keys()

    def get_options(self, field: str):
        return self.settings[field]

    def get_category(self):
        return self.category
