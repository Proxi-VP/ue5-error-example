# -*- coding: utf-8 -*-
# pyright: reportIncompatibleMethodOverride=false
'''Qt flow (gallery) layout'''

from __future__ import annotations
from PySide6 import QtCore, QtWidgets


class QtFlowLayout(QtWidgets.QLayout):

    def __init__(self, parent: QtWidgets.QWidget|None=None, margin: int=0, spacing: int=3):
        '''Qt flow (gallery) layout

        Args:
            parent (QWidget, optional): Parent object. Usually set automatically by assigning this layout to an object. Defaults to None.
            margin (int, optional): Layout margin (pixels). Defaults to 0.
            spacing (int, optional): Item spacing (pixels). Defaults to 3.
        '''
        super().__init__(parent)

        if parent is not None:
            self.setContentsMargins(margin, margin, margin, margin)

        self.setSpacing(spacing)

        self.itemList: list[QtWidgets.QLayoutItem] = []

    def __del__(self):
        item = self.takeAt(0)
        while item:
            item = self.takeAt(0)

    def addItem(self, item: QtWidgets.QLayoutItem):
        self.itemList.append(item)

    def count(self) -> int:
        return len(self.itemList)

    def itemAt(self, index) -> QtWidgets.QLayoutItem|None:
        if index >= 0 and index < len(self.itemList):
            return self.itemList[index]

        return None

    def takeAt(self, index) -> QtWidgets.QLayoutItem|None:
        if index >= 0 and index < len(self.itemList):
            return self.itemList.pop(index)

        return None

    def expandingDirections(self):
        return QtCore.Qt.Orientations(QtCore.Qt.Orientation(0)) # type: ignore -> Incomplete .pyi definition

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width) -> int:
        height = self._doLayout(QtCore.QRect(0, 0, width, 0), True)
        return height

    def setGeometry(self, rect):
        super().setGeometry(rect)
        self._doLayout(rect, False)

    def sizeHint(self):
        return self.minimumSize()

    def minimumSize(self):
        size = QtCore.QSize()

        for item in self.itemList:
            size = size.expandedTo(item.minimumSize())

        left , top , right, bottom = self.getContentsMargins()
        size += QtCore.QSize(left + right, top + bottom)
        return size

    def _doLayout(self, rect, testOnly):
        x = rect.x()
        y = rect.y()
        lineHeight = 0

        for item in self.itemList:
            # wid = item.widget()
            if not item.widget().isVisible():
                continue
            # spaceX = self.spacing() + wid.style().layoutSpacing(
            #     QtWidgets.QSizePolicy.PushButton,
            #     QtWidgets.QSizePolicy.PushButton,
            #     QtCore.Qt.Horizontal)

            # spaceY = self.spacing() + wid.style().layoutSpacing(
            #     QtWidgets.QSizePolicy.PushButton, 
            #     QtWidgets.QSizePolicy.PushButton, 
            #     QtCore.Qt.Vertical)
            spaceX = self.spacing()
            spaceY = self.spacing()

            nextX = x + item.sizeHint().width() + spaceX
            if nextX - spaceX > rect.right() and lineHeight > 0:
                x = rect.x()
                y = y + lineHeight + spaceY
                nextX = x + item.sizeHint().width() + spaceX
                lineHeight = 0

            if not testOnly:
                item.setGeometry(
                    QtCore.QRect(QtCore.QPoint(x, y), item.sizeHint()))

            x = nextX
            lineHeight = max(lineHeight, item.sizeHint().height())

        return y + lineHeight - rect.y()