import copy
from enum import Enum
from Card import Card

class Player:
    Marker = Enum('Marker', 'DOTS COLOR')

    def __init__(self, name, marker, board, maxCardsAllowed):
        self._name = name
        self._marker = marker
        self._board = board
        self._cards = []
        self._won = False
        self._maxCardsAllowed = maxCardsAllowed
    
    def getName(self):
        return self._name

    def getMarker(self):
        return self._marker

    def getCards(self):
        return self._cards

    def takeTurn(self):
        tries = 0

        while tries < 2: 
            # get move string from player
            move = input('\n{}! Enter your move: '.format(self._name)).strip()
            while len(move) != 7 and len(move) != 13:
                print('Please enter a valid move string (e.g. 0 5 A 1, F 2 F 3 3 A 2, etc.')
                move = input('\n{}! Enter your move: '.format(self._name)).strip()

            moveArr = move.split()
            moveType = moveArr[0]

            success = False
            failure_message = ''
            if moveType == '0':
                if len(self._cards) < self._maxCardsAllowed:
                    state = moveArr[1]
                    location = moveArr[2:]
                    success = self._regularMove(state, location)
                else:
                    failure_message = 'You have no more cards left. Please recycle a card'
            else:
                if len(self._board.getCards()) == self._maxCardsAllowed * 2:
                    fromLocationArr = moveArr[:4]
                    state = moveArr[4]
                    toLocationArr = moveArr[5:]
                    success = self._recycleMove(fromLocationArr, state, toLocationArr)
                else:
                    failure_message = 'You cannot recycle until you have run out of cards'

            if not success:
                print('Illegal move! {}\n'.format(failure_message))
                tries = tries + 1
            else:
                break

        return

    def _regularMove(self, state, location):
        card = Card(int(state), location)
        self._cards.append(card)

        return self._board.addCard(card)

    def _recycleMove(self, fromLocationArr, state, toLocationArr):
        card_to_recycle = self._board.getCardToRecycle(fromLocationArr)

        if card_to_recycle is not None:
            print('will recycle the following card:\n{}'.format(str(card_to_recycle)))

            tmp = copy.copy(card_to_recycle)
            new_segments = card_to_recycle._createCardSegments(int(state), toLocationArr)
            card_to_recycle._segments = new_segments

            return self._board.recycleCard(tmp, card_to_recycle)
        
        return False
