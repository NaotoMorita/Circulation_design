import sys
from cx_Freeze import setup, Executable

silent = True
base = None
if sys.platform == "win32":
        base = "Win32GUI"

includes = ["PyQt4.QtCore", "PyQt4.QtGui", "re","numpy","matplotlib.backends.backend_qt4agg","matplotlib.backends.backend_agg","matplotlib.backends.backend_tkagg","binstr"]
includefiles = ["WM_splash.png","WM.ico"]
exe = Executable(script = "Windmize.py",
                 base   = base,
                 icon   = "WM.ico")

setup(
        name = "Windmize",
        version = "1.10",
        description = 'Circulation Desingn',
        options = {"build_exe": {"includes": includes,"include_files":includefiles}},
        executables = [exe],
)