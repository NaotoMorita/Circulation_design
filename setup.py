import sys
from cx_Freeze import setup, Executable

silent = True
base = None
if sys.platform == "win32":
        base = "Win32GUI"

includes = ["PyQt4.QtCore", "PyQt4.QtGui", "re","numpy","matplotlib.backends.backend_qt4agg","matplotlib.backends.backend_agg","matplotlib.backends.backend_tkagg"]
#setup
setup(
        name = "Circulation_Design",
        version = "0.10",
        options = {"build_exe": {"includes": includes}},
        executables = [Executable("opt_circulation.py", base=base)],
)