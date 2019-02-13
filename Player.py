from enum import Enum
from Card import Card

class Player:
    Marker = Enum('Marker', 'DOTS COLOR')

    def __init__(self, name, marker, board):
        self._name = name
        self._marker = marker
        self._board = board
        self._cards = []
    
    def getName(self):
        return self._name

    def getMarker(self):
        return self._marker

    def takeTurn(self):
        tries = 0

        while tries < 2: 
            # get move string from player
            move = input('\n{}! Enter your move: '.format(self._name))
            moveArr = move.split()

            # create card based on input
            card = Card(int(moveArr[1]), moveArr[2:])
            self._cards.append(card)

            # add card to board
            added = self._board.addCard(card)

            if not added:
                print('Illegal move!\n')
                tries = tries + 1
            else:
                break

        return