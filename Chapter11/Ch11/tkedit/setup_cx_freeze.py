from cx_Freeze import setup, Executable

import sys
base = 'Win32GUI' if sys.platform=='win32' else None

import os
import os.path
PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')

options = {
    'build_exe': {
        'include_files':[
            os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tk86t.dll'),
            os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tcl86t.dll'),
         ],
    },
}

executables = [
    Executable('tkedit.py', base=base)
]

setup(name='tkedit',
      version = '1.0',
      description = 'A tkinter text editor',
      options = options,
      executables = executables)
