import os
import sys
import pytest
from PyQt6.QtWidgets import QMainWindow, QApplication
proj_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(proj_dir)
os.environ["IMG_DIR"] = os.path.join(proj_dir,"img")
from blackJack.Players import Player, Dealer

class TestPlayer:
    app = QApplication(sys.argv)
    window = QMainWindow()

    def test_player_setup(self):
        for num in range(100):
            player = Player(num, self.window)
            assert player is not None
            assert player.pos == num
            assert player.title == "Player " + str(num)
            assert not player.isturn()
            assert player.window == self.window

    def test_dealer_setup(self):
        for num in range(3,50):
            decks = num % 3 if num % 3 > 0 else 1
            args = {"deck_count": decks, "window":self.window, "player_count": 8}
            dealer = Dealer(**args)
            assert dealer is not None
            assert dealer.window == self.window
            assert len(dealer.deck) >= 52
            assert dealer.title == "Dealer"
