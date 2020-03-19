class Info:
    def __init__(self, name, brief, description=None, usage=None, settings: {str: str} = None):
        if not description:
            description = brief
        self.name = name
        self.brief = brief
        self.description = description
        self.usage = usage
        self.settings = settings

    def export(self, _dict: dict):
        _dict[self.name] = self

    def configurable(self):
        return self.settings.keys() is not None

    def get_options(self, field: str):
        return self.settings[field]



