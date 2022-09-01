# -*- coding: utf-8 -*-
'''Tile widget (QPushButton)'''

from __future__ import annotations
import proxi.common.strings as strings
from PySide6 import QtCore, QtWidgets, QtGui


STYLESHEET = """
    QPushButton {{
        font-weight: normal;
        height: {height}px;
        max-height: {height}px;
        min-height: {height}px;
        width: {width}px;
        max-width: {width}px;
        min-width: {width}px;
    }}
"""


class QtTile(QtWidgets.QPushButton):

    def __init__(self, label: str, width: int, height: int, properties: dict[str, object]=None, parent=None):
        '''Qt tile widget (QPushButton), primarily for use with `qtFlowLayout`

        Args:
            label (str): Text to display on tile
            width (int): Tile width in pixels
            height (int): Tile height in pixels
            properties (dict[str, object], optional): A collection of key->object pairings to add to the button via QObject.setProperty(). Defaults to None.
            parent (object, optional): [description]. Parent object to associate this widget with. Defaults to None.
        '''

        super().__init__(parent)

        # Set properties
        if isinstance(properties, dict):
            for key, prop in properties.items():
                self.setProperty(key, prop) # type: ignore

        # Set size and other stylesheet properties
        self.setStyleSheet(STYLESHEET.format(width=width, height=height))

        # Button props
        self.setCheckable(True)

        # Insert zero-width whitespace after each underscore and hyphen, to let long text wrap more easily
        label = f'{label}'.replace('_', f'_{strings.Unicode.hairSpace}').replace('-', f'-{strings.Unicode.hairSpace}')

        # Use a child layout and label for button text, to allow wrapping
        labelWidget = QtWidgets.QLabel('{}'.format(label))
        labelWidget.setWordWrap(True)
        labelWidget.setAlignment(QtCore.Qt.AlignCenter)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(labelWidget)
        self.setLayout(layout)