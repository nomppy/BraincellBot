def get_all(which: str = None):
    if not which:
        return Info.info
    elif which == 'help':
        return Info.help
    elif which == 'settings':
        return Info.settings


def get(command: str):
    if command in Info.help:
        return Info.help[command]
    elif command in Info.settings:
        return Info.settings[command]
    elif command in Info.info:
        return Info.info[command]
    return 'Command not found.'


def get_settings(command: str):
    if command in Info.settings:
        return Info.settings[command]
    return 'Command has no settings.'


class Info:

    info = {}
    help = {}
    settings = {}

    def __init__(self, name, description=None):
        self.name = name
        self.description = description

    def __dict__(self):
        return {
            'name': self.name,
            'description': self.description
        }

    def export(self):
        Info.info[self.name] = self


class Help(Info):

    def __init__(self, name, description=None, usage=None):
        super().__init__(name, description)
        self.usage = usage

    def __dict__(self):
        return {
            'name': self.name,
            'description': self.description,
            'usage': self.usage
        }

    def export(self):
        super().export()
        super().help[self.name] = self

    def get_help(self):
        return self.__dict__()


class Settings(Info):

    def __init__(self, name, data: {str: []}):
        super().__init__(name)
        self.fields = data.keys()
        self.dict = data

    def __dict__(self):
        return {
            'name': self.name,
            'fields': self.fields,
            'dict': self.dict
        }

    def export(self):
        super().export()
        super().settings[self.name] = self

    def get_fields(self):
        return self.fields

    def get_field_options(self, field):
        return self.dict[field]
