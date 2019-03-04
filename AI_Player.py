import time
import math
from Player import Player
from Card import Card

class AI(Player):
    
    def __init__(self, name, marker, board, maxCardsAllowed):
        Player.__init__(self, name, marker, board, maxCardsAllowed)

    def takeTurn(self):
        self.regular_minimax()

    def regular_minimax(self):
        start_time = time.time()
        state, position, score = self._board.regular_minimax(self._board, 2, True, self._marker)

        print("--- %s seconds ---" % (time.time() - start_time))
        print(self._name, 'played:', state, position, score)

        col, row = position
        card = Card(state, [str(self._board._getColumnLetterFromIndex(col)), str(row)])
        self._cards.append(card)

        return self._board.addCard(card)

    def tourneyAI(self):
        start_time = time.time()
        cache = {}

        for i in range(1, 5):
            state, position, score = self._board.minimax(self._board, i, -math.inf, math.inf, True, self._marker, cache)
            i += 1

        print("--- %s seconds ---" % (time.time() - start_time))
        print(self._name, 'played:', state, position, score)

        col, row = position
        card = Card(state, [str(self._board._getColumnLetterFromIndex(col)), str(row)])
        self._cards.append(card)

        return self._board.addCard(card)
        