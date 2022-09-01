# -*- coding: utf-8 -*-
'''Qt custom table widget item (sortable)'''

from __future__ import annotations
from PySide6 import QtWidgets


class QtListWidgetItemCustom(QtWidgets.QListWidgetItem):
    '''Custom sorted QListWidgetItem
    
    Args:
        text (str): Cell text value
        sortKey (int|float|mixed): Custom sort value you want to use for comparison with other cell types of this same class (this.sortKey *less than* other.sortKey)
    '''

    def __init__(self, text, sortKey=None):
        if sortKey is None:
            sortKey = text

        if not isinstance(text, str):
            text = f'{text}'

        super().__init__(text, type=QtWidgets.QListWidgetItem.UserType)
        self.sortKey = sortKey

    def __lt__(self, other):
        try:
            if isinstance(other, QtListWidgetItemCustom):
                # print(f'Custom sort {self.text()}: {self.sortKey} < {other.sortKey}')
                return self.sortKey < other.sortKey
            else:
                # print(f'Text sort {self.text()} < {other.text()}')
                return self.text() < other.text()
        except Exception as e:
            # print(f'Failed sorting for {self.text()}: {e}')
            return True