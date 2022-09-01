# -*- coding: utf-8 -*-
'''Qt spinner widget'''

from __future__ import annotations

import math
from PySide6 import QtGui, QtCore, QtWidgets


class QtSpinner(QtWidgets.QWidget):

    def __init__(self, parent, centerOnParent=True, disableParentWhenSpinning=False, modality=QtCore.Qt.NonModal):
        '''Spinner widget to indicate that UI is busy. Optionally disables underlying parent window/dialog while active

        Args:
            parent (QDialog|QMainWindow): Parent window to attach the spinner to
            centerOnParent (bool, optional): Center spinner on parent (vertical and horizontal)? Defaults to True.
            disableParentWhenSpinning (bool, optional): Disable parent while spinner is active? Defaults to False.
            modality ([type], optional): Window modality. Untested...? Defaults to QtCore.Qt.NonModal.
        '''
        super().__init__(parent)

        self._centerOnParent = centerOnParent
        self._disableParentWhenSpinning = disableParentWhenSpinning

        self._color = QtGui.QColor(QtCore.Qt.white)
        self._roundness: float = 100.0
        self._minimumTrailOpacity: float = 3.14159265358979323846
        self._trailFadePercentage: float = 80.0
        self._revolutionsPerSecond: float = 1.57079632679489661923
        self._numberOfLines: int = 20
        self._lineLength: int = 10
        self._lineWidth: int = 2
        self._innerRadius: int = 10
        self._currentCounter: int = 0
        self._isSpinning: bool = False

        self._timer = QtCore.QTimer(self)
        self._timer.timeout.connect(self.rotate) # type: ignore
        self.updateSize()
        self.updateTimer()
        self.hide()

        self.setWindowModality(modality)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

    def paintEvent(self, event):
        self.updatePosition()
        # self.updateSize()
        painter = QtGui.QPainter(self)
        painter.fillRect(self.rect(), QtCore.Qt.transparent)
        # painter.fillRect(self.rect(), QtCore.Qt.lightGray)
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)

        if self._currentCounter >= self._numberOfLines:
            self._currentCounter = 0

        painter.setPen(QtCore.Qt.NoPen)
        for i in range(0, self._numberOfLines):
            painter.save()
            painter.translate(self._innerRadius + self._lineLength, self._innerRadius + self._lineLength)
            rotateAngle = float(360 * i) / float(self._numberOfLines)
            painter.rotate(rotateAngle)
            painter.translate(self._innerRadius, 0)
            distance = self.lineCountDistanceFromPrimary(i, self._currentCounter, self._numberOfLines)
            color = self.currentLineColor(distance, self._numberOfLines, self._trailFadePercentage,
                                          self._minimumTrailOpacity, self._color)
            painter.setBrush(color)
            painter.drawRoundedRect(QtCore.QRect(0, -self._lineWidth // 2, self._lineLength, self._lineWidth), self._roundness,
                                    self._roundness, QtCore.Qt.RelativeSize)
            painter.restore()

    def start(self):
        self.updatePosition()
        self._isSpinning = True
        self.show()

        if self.parentWidget and self._disableParentWhenSpinning:
            self.parentWidget().setEnabled(False)

        if not self._timer.isActive():
            self._timer.start()
            self._currentCounter = 0

    def stop(self):
        self._isSpinning = False
        self.hide()

        if self.parentWidget() and self._disableParentWhenSpinning:
            self.parentWidget().setEnabled(True)

        if self._timer.isActive():
            self._timer.stop()
            self._currentCounter = 0

    def setNumberOfLines(self, lines: int):
        self._numberOfLines = lines
        self._currentCounter = 0
        self.updateTimer()

    def setLineLength(self, length: int):
        self._lineLength = length
        self.updateSize()

    def setLineWidth(self, width: int):
        self._lineWidth = width
        self.updateSize()

    def setInnerRadius(self, radius: int):
        self._innerRadius = radius
        self.updateSize()

    def color(self):
        return self._color

    def roundness(self):
        return self._roundness

    def minimumTrailOpacity(self):
        return self._minimumTrailOpacity

    def trailFadePercentage(self):
        return self._trailFadePercentage

    def revolutionsPersSecond(self):
        return self._revolutionsPerSecond

    def numberOfLines(self):
        return self._numberOfLines

    def lineLength(self):
        return self._lineLength

    def lineWidth(self):
        return self._lineWidth

    def innerRadius(self):
        return self._innerRadius

    def isSpinning(self):
        return self._isSpinning

    def setRoundness(self, roundness):
        self._roundness = max(0.0, min(100.0, roundness))

    def setColor(self, color=QtCore.Qt.black):
        self._color = QtGui.QColor(color)

    def setRevolutionsPerSecond(self, revolutionsPerSecond):
        self._revolutionsPerSecond = revolutionsPerSecond
        self.updateTimer()

    def setTrailFadePercentage(self, trail):
        self._trailFadePercentage = trail

    def setMinimumTrailOpacity(self, minimumTrailOpacity):
        self._minimumTrailOpacity = minimumTrailOpacity

    def rotate(self):
        self._currentCounter += 1
        if self._currentCounter >= self._numberOfLines:
            self._currentCounter = 0
        self.update()

    def updateSize(self):
        size = (self._innerRadius + self._lineLength) * 2
        self.setFixedSize(size, size)
        # self.setFixedSize(self.parentWidget().width(), self.parentWidget().height())

    def updateTimer(self):
        self._timer.setInterval(int(1000 / (self._numberOfLines * self._revolutionsPerSecond)))

    def updatePosition(self):
        if self.parentWidget() and self._centerOnParent:
            self.move(self.parentWidget().width() // 2 - self.width() // 2,
                      self.parentWidget().height() // 2 - self.height() // 2)

    def lineCountDistanceFromPrimary(self, current, primary, totalNrOfLines):
        distance = primary - current
        if distance < 0:
            distance += totalNrOfLines
        return distance

    def currentLineColor(self, countDistance, totalNrOfLines, trailFadePerc, minOpacity, colorinput):
        color = QtGui.QColor(colorinput)
        if countDistance == 0:
            return color
        minAlphaF = minOpacity / 100.0
        distanceThreshold = int(math.ceil((totalNrOfLines - 1) * trailFadePerc / 100.0))
        if countDistance > distanceThreshold:
            color.setAlphaF(minAlphaF)
        else:
            alphaDiff = color.alphaF() - minAlphaF
            gradient = alphaDiff / float(distanceThreshold + 1)
            resultAlpha = color.alphaF() - gradient * countDistance
            # If alpha is out of bounds, clip it.
            resultAlpha = min(1.0, max(0.0, resultAlpha))
            color.setAlphaF(resultAlpha)
        return color