import time
import math
from Player import Player
from Card import Card

class AI(Player):
    
    def __init__(self, name, marker, board, maxCardsAllowed,isTraceFile, _type='REGULAR'):
        Player.__init__(self, name, marker, board, maxCardsAllowed)
        self._type = _type
        self._cache = dict()
        self._isTraceFile = isTraceFile

    def takeTurn(self):
        if len(self._cards) < self._maxCardsAllowed:
            self._regularMove()
        else:
            self._recycleMove()

    def _regularMove(self):
        start_time = time.time()
        if self._type == 'REGULAR':
            state, position, score,traceArray = self._regular_minimax()
            if self._isTraceFile :
                file =open("minmax.txt","a")
                for x in range(0,len(traceArray)): 
                    if x == 2:
                        file.write("\n")
                    file.write(str(round(traceArray[x],1)))
                    file.write("\n")
                file.write("\n")
                file.close
        elif self._type == 'TOURNEY':
            state, position, score = self.tourneyAI()

        col, row = position
        card = Card(state, [str(self._board._getColumnLetterFromIndex(col)), str(row)])
        self._cards.append(card)

        letter = self._board._getColumnLetterFromIndex(col)
        print('{} took {}s to play {} {} {}. Move score was {}'.format(self._name, (time.time() - start_time), state, letter, row, score))

        return self._board.addCard(card)

    def _recycleMove(self):
        start_time = time.time()
        
        state = None
        position = None
        score = None
        if self._type == 'REGULAR':
            state, position, score = self._board.regular_recycle_minimax(self._board, 2, self._marker)
        elif self._type == 'TOURNEY':
            for i in range(1,2):
                state, position, score = self._board.recycle_minimax(self._board, i, self._marker, self._cache)

        col, row = position
        card = Card(state, [str(self._board._getColumnLetterFromIndex(col)), str(row)])

        letter = self._board._getColumnLetterFromIndex(col)
        print('{} took {}s to recycle and play {} {} {}. Move score was {}'.format(self._name, (time.time() - start_time), state, letter, row, score))

        return self._board.addCard(card, recycled=True)


    def _regular_minimax(self):
        
        return self._board.regular_minimax(self._board, 2, True, self._marker,[0,0])

    def tourneyAI(self):
        traceArray = [0,0]
        state = None
        position = None
        score = None

        state, position, score,traceArray = self._board.minimax(self._board, 2, -math.inf, math.inf, True, self._marker, self._cache,traceArray,None)

        return state, position, score
        