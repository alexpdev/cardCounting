#! /usr/bin/python3
# -*- coding: utf-8 -*-

from card_counter.Deck import Deck
from card_counter.Window import CardWidget

class Player:

    def __init__(self,pos=None,window=None,**kwargs):
        self.pos = pos
        self.hand = []
        self.window = window
        self._turn = False
        self.cards = None
        self.box = None
        self.title = "Player " + str(pos)


    @property
    def score(self): return sum(card.value for card in self.hand)

    def __str__(self): return self.title

    def __repr__(self): return self.title

    def isturn(self): return self._turn

    def turn(self): self._turn = not self._turn


    def set_widgets(self,cards=None,box=None):
        self.cards = cards
        self.box = box

    def add_card(self,card):
        card_img = card.getPath()
        self.hand.append(card)
        cover = False
        for c in self.cards:
            if c.cover == True:
                c.reset(card_img)
                cover = True; break
        if not cover:
            cWidget = CardWidget(cover=False,path=card_img)
            self.box.layout().addWidget(cWidget)
            self.cards.append(cWidget)

    def show_hand(self):
        output = str(self) + " "  + str(self.hand) + " " + str(self.score) + "\n"
        print(self,self.hand,self.score)
        self.window.textBrowser.append(output)


class Dealer(Player):
    """
        Dealer Object. Controls game.
    """

    def __init__(self,limit=26,deck_count=1,players=[],**kwargs):
        super().__init__(**kwargs)
        self.title = "Dealer"
        self.deck_count = deck_count
        self.limit = limit
        self.players = players
        self.deck = Deck.times(deck_count)

    def start_deal(self):
        for _ in range(2):
            for player in self.players:
                self.deal_card(player)
            self.deal_card(self)

    def deal_card(self,player):
        card = self.deck.pop()
        player.add_card(card)
        self.window.update()

    def round(self):
        for player in self.players:
            player.turn()

    def new_game(self):
        self.deck.shuffle()
        self.start_deal()
        self.round()


class Stats:

    counts = {
        2: 4, 3: 4,
        4: 4, 5: 4,
        6: 4, 7: 4,
        8: 4, 9: 4,
        10: 16, 11: 4}

    refresh = lambda: [counts.__setitem__(k,4) for k in counts]

    @classmethod
    def probability(cls,val):
        total = sum(cls.counts.values())
        p = cls.counts[val]
        return p/total