import time
import math
from Player import Player
from Card import Card

class AI(Player):
    
    def __init__(self, name, marker, board, maxCardsAllowed):
        Player.__init__(self, name, marker, board, maxCardsAllowed)

    def takeTurn(self):
        start_time = time.time()
        cache = {}
        card_state, vertical_position, current_score = self._board.minimax(self._board, 4, -math.inf, math.inf, True, self._marker, cache)
        print("--- %s seconds ---" % (time.time() - start_time))
        print(self._name, 'played:', card_state, vertical_position, current_score)

        col, row = vertical_position
        card = Card(card_state, [str(self._board._getColumnLetterFromIndex(col)), str(row)])
        self._cards.append(card)

        return self._board.addCard(card)