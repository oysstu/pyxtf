"""
Utility to read the xtf_ctypes file and generate an pyi file to facilitate type hinting.
Note: Not a general tool for this purpose, it only parses the __fields__ property
"""

import inspect
import ctypes
import os.path


XTF_CField = """
class CField:
    \"\"\"
    This is a redefinition of the _ctype.CField class, which is hidden in the ctypes API.
    This class is not intended to be used at runtime, but is here to allow for static typing of the XTF-classes.
    \"\"\"
    def __init__(self):
        self.offset = 0  # type: int
        self.size = 0  # type: int

"""

XTF_Base = """
class XTFBase(ctypes.LittleEndianStructure):
    \"\"\"
    Base class for all XTF ctypes.Structure children.
    Exposes basic utility like printing of fields and constructing class from a buffer.
    \"\"\"
    def __str__(self) -> str:
        pass

    def __new__(cls, buffer: IOBase = None):
        pass

    def __init__(self, buffer=None, *args, **kwargs):
        pass

"""


def ctype_struct_generator(module):
    module_structs = inspect.getmembers(module, predicate=(
        lambda x: (inspect.isclass(x) and ctypes.Structure in inspect.getmro(x))))

    # Sort by the line number in which the class appears
    module_structs.sort(key=lambda x: inspect.getsourcelines(x[1])[1])
    for name, obj in module_structs:
            if ctypes.Structure in inspect.getmro(obj) and hasattr(obj, '_fields_'):
                yield obj


def get_all_fields(obj):
    cur_obj = obj
    fields = []

    base_fields = []
    if obj.__bases__:
        for base in obj.__bases__:
            base_fields += get_all_fields(base)

    if hasattr(cur_obj, '_fields_'):
        return base_fields + getattr(cur_obj, '_fields_')
    else:
        return base_fields


def generate_pyi(module):
    # Retrieve classes that derive from ctypes.Structure
    c_structs = ctype_struct_generator(module)

    pyi_path = os.path.splitext(module.__file__)[0] + '.pyi'
    with open(pyi_path, 'w') as f:
        # Write imports
        f.writelines([
            'import ctypes\n',
            'import numpy as np\n',
            #'import {}\n'.format(module.__package__),
            'from io import IOBase, BytesIO\n'
            'from typing import List, Tuple, Dict, Callable, Any\n\n\n'
        ])

        # Write CField and XTFBase classes
        f.write(XTF_CField)
        f.write(XTF_Base)

        for struct in c_structs:
            base_names = [type.__name__ for type in struct.__bases__]
            f.write('class {}({}):\n'.format(struct.__name__, ','.join(base_names)))

            # Retrieve _fields_ for this class
            if hasattr(struct, '_fields_'):
                fields = struct._fields_
            else:
                fields = []

            # Write static fields (ctypes.CField)
            for name, type in fields:
                f.write(' ' * 4 + '{} = None  # type: CField\n'.format(name))

            if hasattr(struct, '_typing_static_'):
                for name, type in struct._typing_static_:
                    f.write(' ' * 4 + '{} = None  # type: {}\n'.format(name, type))

            # Write instance (typed) fields
            if fields:
                f.write('\n' + ' '*4 + 'def __init__(self):\n')
            for name, type in fields:
                # Handle arrays correctly by extracting the element type
                if ctypes.Array in type.__bases__:
                    if type._type_ in ctype_struct_generator(module):
                        # Array of structs defined elsewhere in the module
                        typename = 'ctypes.Array[{}]'.format(type._type_.__name__)
                    else:
                        # Array of types not defined in the module (ctype assumed)
                        typename = 'ctypes.Array[{}.{}]'.format(type._type_.__module__, type._type_.__name__)
                else:
                    typename = '{}.{}'.format(type.__module__, type.__name__)

                f.write(' '*8 + 'self.{} = None  # type: {}\n'.format(name, typename))

            if hasattr(struct, '_typing_instance_'):
                for name, type in struct._typing_instance_:
                    f.write(' ' * 8 + 'self.{} = None  # type: {}\n'.format(name, type))

            for name, fun in inspect.getmembers(struct, predicate=inspect.isfunction):
                if not (name.startswith('__') or name.endswith('__')):
                    f.write(' '*4 + 'def {}{}:\n'.format(name, inspect.signature(fun)) + ' '*8 + 'pass\n')

            f.write('\n\n')


if __name__ == '__main__':
    import pyxtf.xtf_ctypes
    generate_pyi(pyxtf.xtf_ctypes)

    import pyxtf.vendors.kongsberg
    generate_pyi(pyxtf.vendors.kongsberg)

