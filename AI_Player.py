import time
import math
from Player import Player
from Card import Card

class AI(Player):
    
    def __init__(self, name, marker, board, maxCardsAllowed):
        Player.__init__(self, name, marker, board, maxCardsAllowed)
        self._cache = dict()

    def takeTurn(self):
        if len(self._cards) < self._maxCardsAllowed:
            self._regularMove()
        else:
            self._recycleMove()

    def _regularMove(self):
        start_time = time.time()
        state, position, score = self._regular_minimax()

        col, row = position
        card = Card(state, [str(self._board._getColumnLetterFromIndex(col)), str(row)])
        self._cards.append(card)

        letter = self._board._getColumnLetterFromIndex(col)
        print('{} took {}s to play {} {} {}. Move score was {}'.format(self._name, (time.time() - start_time), state, letter, row, score))

        return self._board.addCard(card)

    def _recycleMove(self):
        pass

    def _regular_minimax(self):
        return self._board.regular_minimax(self._board, 2, True, self._marker)

    def tourneyAI(self):
        state = None
        position = None
        score = None

        for i in range(1, 3):
            state, position, score = self._board.minimax(self._board, i, -math.inf, math.inf, True, self._marker, self._cache)

        return state, position, score
        