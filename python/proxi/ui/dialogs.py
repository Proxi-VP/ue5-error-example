# -*- coding: utf-8 -*-
'''UI dialogs'''

from __future__ import annotations

import proxi.console as console
from typing import Callable
from PySide6.QtWidgets import (
    QWidget,
    QMessageBox
)


# Dialog styles
class DialogStyle:
    '''Dialog styles (eg icon)'''

    information = QMessageBox.information
    warning = QMessageBox.warning
    error = QMessageBox.critical
    question = QMessageBox.question


# Standard buttons (inheriting for future, and shorter name)
class StandardButton(QMessageBox.StandardButton):
    '''Standard buttons for dialogs'''


def messagebox(title: str, message: str, parent: QWidget=None, buttons=StandardButton.Ok, default=StandardButton.Ok, consolePrint: bool=False) -> StandardButton:
    '''Display a modal information-style pop up for the user
 
    Args:
        title (string): Heading
        message (string): Body text
        parent (QtWidget): Parent object, if any
        buttons (QtWidgets.QMessageBox.StandardButton|...): Collection of buttons to display, separated by a bitwise OR operator (|)
        default (QtWidgets.QMessageBox.StandardButton): Default button for various non-mouse interactions like pressing Enter key, etc. Must be present in the `buttons` collection

    Returns:
        QtWidgets.QMessageBox.StandardButton: Result of interaction
    '''

    if consolePrint:
        console.log(message)

    return QMessageBox.information(parent, title, message, buttons, default) # type: ignore


def notify(title: str, message: str, parent: QWidget=None, consolePrint: bool=True):
    '''Alias for `messagebox` with a single OK button

    Args:
        title (string): Heading
        message (string): Body text
        parent (QtWidget): Parent object, if any
        consolePrint (bool, optional): Print message to console. Defaults to True
    
    Returns:
        QtWidgets.QMessageBox.StandardButton: Result of interaction
    '''

    return messagebox(title, message, parent=parent, buttons=StandardButton.Ok, default=StandardButton.Ok, consolePrint=consolePrint)


def warn(title: str, message: str, parent: QWidget=None, buttons=StandardButton.Ok, default=StandardButton.Ok) -> StandardButton:
    '''Display a modal warning pop up for the user and log a warning

    Args:
        title (string): Heading
        message (string): Body text
        parent (QtWidget): Parent object, if any
        buttons (QtWidgets.QMessageBox.StandardButton|...): Collection of buttons to display, separated by a bitwise OR operator (|)
        default (QtWidgets.QMessageBox.StandardButton): Default button for various non-mouse interactions like pressing Enter key, etc. Must be present in the `buttons` collection

    Returns:
        QtWidgets.QMessageBox.StandardButton: Result of interaction
    '''

    console.warning(message)
    return QMessageBox.warning(parent, title, message, buttons, default) # type: ignore


def error(title: str, message: str, parent: QWidget=None, buttons: StandardButton=StandardButton.Ok, default: StandardButton=StandardButton.Ok, throw: bool=True) -> StandardButton:
    '''Display a pop up message box for the user with a 'critical' style icon

    Args:
        title (string): Heading
        message (string): Body text
        parent (QtWidget): Parent object, if any
        buttons (QtWidgets.QMessageBox.StandardButton|...): Collection of buttons to display, separated by a bitwise OR operator (|)
        default (QtWidgets.QMessageBox.StandardButton): Default button for various non-mouse interactions like pressing Enter key, etc. Must be present in the `buttons` collection

    Raises:
        RuntimeError

    Returns:
        QtWidgets.QMessageBox.StandardButton: Result of interaction
    '''

    console.error(message)
    result = QMessageBox.critical(parent, title, message, buttons, default) # type: ignore

    if throw:
        raise RuntimeError(message)

    return result


def questionYesNo(title: str, message: str, parent: QWidget=None, dialogStyle: object|None=None) -> bool:
    '''Display a pop up question box for the user with two buttons -> Yes and No

    Args:
        title (string): Heading
        message (string): Body text
        parent (QtWidget): Parent object, if any
        dialogStyle (DialogStyle): Desired dialog style. Defaults to `question`

    Returns:
        bool: True on Yes, False on No (or cancel/dismiss)
    '''

    console.log(f'{title}: {message}')

    _dialogStyle: Callable = dialogStyle or DialogStyle.question # type: ignore
    reply = _dialogStyle(parent, title, message, StandardButton.Yes|StandardButton.No, StandardButton.No)
    if reply == StandardButton.Yes:
        return True
    else:
        return False


def questionOkCancel(title: str, message: str, parent: QWidget=None, dialogStyle: object=None):
    '''Display a pop up question box for the user with two buttons -> OK and Cancel

    Args:
        title (string): Heading
        message (string): Body text
        parent (QtWidget): Parent object, if any
        dialogStyle (DialogStyle): Desired dialog style. Defaults to `question`

    Returns:
        bool: True on Yes, False on No (or cancel/dismiss)
    '''

    console.log(f'{title}: {message}')

    _dialogStyle: Callable = dialogStyle or DialogStyle.question # type: ignore
    reply = _dialogStyle(parent, title, message, StandardButton.Ok|StandardButton.Cancel, StandardButton.Cancel)
    if reply == StandardButton.Ok:
        return True
    else:
        return False