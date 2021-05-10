import utils


class HandlersMenuItems:
    """Utility class to wrap app handlers from the manager to ease handling
    them in the interactive cli for nicer output."""
    class Item:
        def __init__(self, value, text, description):
            self.v = value
            self.t = text
            self.d = description

        def __repr__(self):
            return f'<v: {self.v} | t: {self.t} | d:{self.d}>'

    def __init__(self, handlers):
        def gt(i): return getattr(i, 'source', getattr(i, 'output_type', None))
        self.menuitems = [
            HandlersMenuItems.Item(
                gt(i),
                i.friendly_name,
                i.description) for i in handlers
            ]

    def get_friendly_names(self, filter=lambda x: True):
        return [i.t for i in self.menuitems if filter(i) is True]

    def get_choice_index(self, choice):
        """
        Return the index of the menu item for the given friendly_name
        """
        try:
            return [i.v for i in self.menuitems].index(choice)
        except Exception:
            return 0

    def get_friendly_name(self, index):
        return self.menuitems[index].t

    def get_value(self, index):
        return self.menuitems[index].v

    def get_description(self, index):
        return self.menuitems[index].d

    def get_value_by_name(self, friendly_name):
        try:
            return [i.v for i in self.menuitems if i.t == friendly_name][0]
        except IndexError:
            return None

    def get_name_by_value(self, value):
        """Takes the choice of the menu and returns the name to print"""
        try:
            return [i.t for i in self.menuitems if i.v == value][0]
        except IndexError:
            return None

    def get_description_by_value(self, value):
        try:
            desc = [i.d for i in self.menuitems if i.t == value]
            return utils.cli.format(desc[0])
        except Exception:
            pass
