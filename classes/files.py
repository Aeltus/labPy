class Files():

    def fopen(path):
        file = open(path, 'r')
        content = file.read()
        file.close()
        return content
    fopen = staticmethod(fopen)