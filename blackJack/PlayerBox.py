#! /usr/bin/python3
# -*- coding: utf-8 -*-

#######################################################################
# BlackJack Card Counting
# Copyright (C) 2021  alexpdev
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses
#########################################################################

import os

from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (QGroupBox,
                            QHBoxLayout,
                            QLabel,
                            QSpacerItem,
                            QVBoxLayout)

IMG_DIR = os.environ.get("IMG_DIR")
# directory containing all png files for cards
CARDCOVER = os.path.join(IMG_DIR, "card_cover.png")
# path to png of a card face down


class PlayerBox(QGroupBox):
    """
    PlayerBox : Subclass of QGroupBox
    Returns:
        GroupBoxWidget: data and cards for each player
    """
    offsheet = """QGroupBox {
        padding: 4px;
        margin: 2px;
        color: black;
        border: 2px solid grey;} """
    onsheet = """QGroupBox {
            color: red;
            padding: 6px;
            margin: 3px;
            border: 3px solid red;
            border-radius: 3px;}"""

    def __init__(self, title, parent=None, player=None):
        """
        __init__ Constructor for PlayerBox
        """
        super().__init__(title, parent=parent)
        self.player = player
        self.setStyleSheet(self.offsheet)
        self.vbox = QVBoxLayout()
        self.setLayout(self.vbox)
        self.hbox = QHBoxLayout()
        self.hbox2 = QHBoxLayout()
        self.label = QLabel("Score: ")
        self.label.setStyleSheet(
            """
            QLabel {
            color: black;
            font-weight: bold;
            font-size: 14pt;
            font-style: italic;}
            """
        )
        self.scorelabel = QLabel("0")
        self.scorelabel.setStyleSheet(
            """
            QLabel {
            border: 1px solid black;
            padding: 3px;
            color: black;
            font-weight: bold;
            font-size: 16pt;
            font-style: italic;}
            """
        )
        self.hbox2.addWidget(self.label)
        self.hbox2.addWidget(self.scorelabel)
        self.hbox2.addSpacerItem(QSpacerItem(80, 0))
        self.vbox.addLayout(self.hbox2)
        self.vbox.addLayout(self.hbox)
        self._turn = False
        for _ in range(2):
            card = CardWidget(parent=self)
            self.hbox.addWidget(card)
            self.addCard(card)
        self.player.box = self

    @property
    def cards(self):
        # shortcut method accessing
        # players cards property
        return self.player.cards

    def addCard(self, card):
        # shortcut for adding card widget
        # to players list of cards
        self.player.cards.append(card)

    def deleteCard(self):
        # removes card from Players list of cards property
        self.player.cards = self.player.cards[1:]

    def reset(self):
        """
        `self.reset()`
        Clears PlayerBox of all widgets. Called when cuttent
        round ends and new deal begins.
        """
        while len(self.cards) > 0:
            card = self.cards[0]
            card.destroy(True, True)
            self.hbox.removeWidget(card)
            self.deleteCard()
            del card

    def isTurn(self):
        # returns True if currently players Turn
        return self._turn

    def turn(self):
        """
        flips `self.turn` property as well as change the

        style of PlayerBox to indicate it is or isn't currently
        players turn
        """
        if self.isTurn():
            self._turn = False
            self.setStyleSheet(self.offsheet)
        else:
            self._turn = True
            self.setStyleSheet(self.onsheet)


class CardWidget(QLabel):
    """
    CardWidget Widget which holds the image of the card it represents.

    Args:
        QLabel (QPixmap): Either a specific card in deck or
        back of card for when it is facedown.
    """
    stylesheet = """QLabel {
        margin: 4px;
        padding: 5px;}"""

    def __init__(self, parent=None, card=None, cover=True, path=CARDCOVER):
        """
        __init__ Constructor for CardWidget class.

        Args:
            parent (QWidget, optional): parent widget for CardWidget. Defaults to None.
            card (Card(), optional): Card object. Defaults to None.
            cover (bool, optional): If True use Cardcoverpath else use give path.
            path (str, optional): path to Pixmap Image. Defaults to CARDCOVER.
        """
        super().__init__(parent=parent)
        self.setStyleSheet(self.stylesheet)
        self.cover = cover
        self.path = path
        self.card = card
        self.setImage()

    def faceDown(self):
        """
        `self.faceDown()` called for dealers face down card.
        """
        pixmap = QPixmap(CARDCOVER)
        self.setPixmap(pixmap)

    def faceUp(self):
        # show value of a facedown card
        self.setImage()

    def setCard(self, card):
        """
        `self.setCard(card)` assign Card objrct to CardWidget
        Args: card (Card object)
        """
        self.cover = False
        self.card = card
        self.path = card.path
        self.setImage()

    def setImage(self):
        # assign image path as pixmap
        pixmap = QPixmap(self.path)
        self.setPixmap(pixmap)
