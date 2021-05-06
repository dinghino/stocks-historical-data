class validation_errors:
    errors = {}

    def reset(self):
        self.errors = {}

    def add(self, key, error, debug_error):
        if key not in self.errors:
            self.errors[key] = {'err': error, 'dbg': debug_error}

    def get(self, key=None, debug=False):
        if not key and not debug:
            return [e['err'] for e in self.errors.values() if not e['dbg']]
        elif debug:
            return [e['err'] for e in self.errors.values()]
        # This doesn't throw
        return self.errors.get(key)

    def remove(self, key):
        self.errors.pop(key, None)
