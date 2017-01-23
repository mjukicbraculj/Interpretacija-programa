import types

class AST(types.SimpleNamespace):       #A simple object subclass that provides attribute access to its namespace, as well as a meaningful repr.
    def __repr__(self):
        atributes = vars(self).copy()
        name = atributes.pop('tree', type(self).__name__)
        stavke = ['{}={}'.format(k, v) for k, v in atributes.items()]
        return name + ', '.join(stavke).join('()')
