# -*- coding: utf-8 -*-
'''QMainWindow demo from Qt Material module'''

import os
import typing
import proxi.dev as dev
import proxi.config as config
import proxi.ui as ui
import proxi.console as console
import proxi.ui.wrappers.mainWindow as mainWindow
from . import demoMainWindow_ui as window
from qt_material import QtStyleTools

from PySide6 import QtGui



class DemoMainWindow(mainWindow.QtMainWindowWrapper, QtStyleTools):
    def __init__(self, parent=None):
        # scriptPath = os.path.realpath(__file__)

        if typing.TYPE_CHECKING:
            self.ui = window._TypeHint()

        super().__init__(
            uiClass = window.Ui_MainWindow,
            prefsPath = config.getUiPrefsPath('demoMainWindow'),
            opacitySlider = False,
            windowSize = None,
            parent = parent
        )

        # self.set_extra_colors(extra)
        self.add_menu_theme(self, self.ui.menuStyles)
        # self.show_dock_theme(self.main)

        logo = QtGui.QIcon("qt_material:/logo/logo.svg")
        logo_frame = QtGui.QIcon("qt_material:/logo/logo_frame.svg")

        self.setWindowIcon(logo)
        self.ui.actionToolbar.setIcon(logo)



# Keep track of window instance while allowing for module reload without resetting
try:
    WINDOW_INSTANCE # type: ignore
except NameError:
    WINDOW_INSTANCE: DemoMainWindow = None # type: ignore


def showWindow(forceNew=False):
    '''Public access method: Show dialog, instanciate new instance if required'''

    # MUST keep global track of this instance because of the Unreal garbage collection. Or so it seems.
    global WINDOW_INSTANCE

    # We might not be in sync, window could have been deleted even if `WINDOW_INSTANCE` reference claims otherwise.
    # Activate window the brute-force way

    if forceNew or dev.DEBUG_MODE or dev.DEV_MODE:

        # Allow multiple (unbound) window instances in `DEV_MODE`
        if dev.DEV_MODE:
            pass
            # dev.reloadModules([ui])

        # Force window delete for `forceNew` or `DEBUG_MODE`
        elif WINDOW_INSTANCE:
            try:
                console.debug('Deleting existing window instance', timestamp=True)
                del ui.OPEN_WINDOWS[WINDOW_INSTANCE]
                WINDOW_INSTANCE._delete()
            except Exception as e:
                console.error(f'Error destroying old window instance: {e}')

        WINDOW_INSTANCE = None # type: ignore

    try:
        WINDOW_INSTANCE.showAndActivate()
        console.log('Activating existing window')
    except Exception:
        WINDOW_INSTANCE = DemoMainWindow()
        WINDOW_INSTANCE.showAndActivate()
        console.log('Created new window')

    if not WINDOW_INSTANCE in ui.OPEN_WINDOWS:
        ui.OPEN_WINDOWS[WINDOW_INSTANCE] = showWindow
        console.log('Adding window instance to global tracker')