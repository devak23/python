class Reader:
    def __init__(self, filename):
        self._file = filename
        self._f = open(self._file, "rt")

    def close(self):
        self._f.close()

    def read(self):
        print('reading %s' % self._file)
        return self._f.read()
