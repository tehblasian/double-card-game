from enum import Enum

class Card:
    CardColor = Enum('CARD_COLOR', 'WHITE RED')
    CardSymbol = Enum('CARD SYMBOL', 'WHITE_DOT BLACK_DOT')
    
    _card_id = 1

    def __init__(self, state, locationArr):
        self._state = state
        self._location = ''.join(locationArr)
        self._segments = self._createCardSegments(state, locationArr)

        Card._card_id += 1

    def getLocation(self):
        return self._location

    def getState(self):
        return self._state

    def getSegments(self):
        return self._segments

    def setLocation(self, location):
        self._location = location
    
    def setState(self, state):
        self._state = state

    def _getXLocationIndexFromLetter(self, rowLetter):
        indices = {
            'A': 1,
            'B': 2,
            'C': 3,
            'D': 4,
            'E': 5,
            'F': 6,
            'G': 7,
            'H': 8,
        }

        return indices[rowLetter]

    def _getAdjacentXLocation(self, rowIndex):
        return int(rowIndex) + 1
    
    def _getYLocationIndexBelow(self, colIndex):
        return int(colIndex) - 1

    def _getYLocationIndexAbove(self, colIndex):
        return int(colIndex) + 1

    def _createCardSegments(self, state, locationArr):
        col = locationArr[0].upper()
        row = locationArr[1]

        first_segment = None
        second_segment = None

        firstSegmentXLocation = self._getXLocationIndexFromLetter(col)
        if state == 1:
            first_segment = self.CardSegment(Card._card_id, Card.CardColor.RED, Card.CardSymbol.BLACK_DOT, firstSegmentXLocation, row)
            secondSegmentXLocation = self._getAdjacentXLocation(self._getXLocationIndexFromLetter(col))
            second_segment = self.CardSegment(Card._card_id, Card.CardColor.WHITE, Card.CardSymbol.WHITE_DOT, secondSegmentXLocation, row)

        if state == 2:
            first_segment = self.CardSegment(Card._card_id, Card.CardColor.WHITE, Card.CardSymbol.WHITE_DOT, firstSegmentXLocation, row)
            secondSegmentYLocation = self._getYLocationIndexAbove(row)
            second_segment = self.CardSegment(Card._card_id, Card.CardColor.RED, Card.CardSymbol.BLACK_DOT, firstSegmentXLocation, secondSegmentYLocation)

        if state == 3:
            first_segment = self.CardSegment(Card._card_id, Card.CardColor.WHITE, Card.CardSymbol.WHITE_DOT, firstSegmentXLocation, row)
            secondSegmentXLocation = self._getAdjacentXLocation(self._getXLocationIndexFromLetter(col))
            second_segment = self.CardSegment(Card._card_id, Card.CardColor.RED, Card.CardSymbol.BLACK_DOT, secondSegmentXLocation, row)

        if state == 4:
            first_segment = self.CardSegment(Card._card_id, Card.CardColor.RED, Card.CardSymbol.BLACK_DOT, firstSegmentXLocation, row)
            secondSegmentYLocation = self._getYLocationIndexAbove(row)
            second_segment = self.CardSegment(Card._card_id, Card.CardColor.WHITE, Card.CardSymbol.WHITE_DOT, firstSegmentXLocation, secondSegmentYLocation)

        if state == 5:
            first_segment = self.CardSegment(Card._card_id, Card.CardColor.RED, Card.CardSymbol.WHITE_DOT, firstSegmentXLocation, row)
            secondSegmentXLocation = self._getAdjacentXLocation(self._getXLocationIndexFromLetter(col))
            second_segment = self.CardSegment(Card._card_id, Card.CardColor.WHITE, Card.CardSymbol.BLACK_DOT, secondSegmentXLocation, row)

        if state == 6:
            first_segment = self.CardSegment(Card._card_id, Card.CardColor.WHITE, Card.CardSymbol.BLACK_DOT, firstSegmentXLocation, row)
            secondSegmentYLocation = self._getYLocationIndexAbove(row)
            second_segment = self.CardSegment(Card._card_id, Card.CardColor.RED, Card.CardSymbol.WHITE_DOT, firstSegmentXLocation, secondSegmentYLocation)

        if state == 7:
            first_segment = self.CardSegment(Card._card_id, Card.CardColor.WHITE, Card.CardSymbol.BLACK_DOT, firstSegmentXLocation, row)
            secondSegmentXLocation = self._getAdjacentXLocation(self._getXLocationIndexFromLetter(col))
            second_segment = self.CardSegment(Card._card_id, Card.CardColor.RED, Card.CardSymbol.WHITE_DOT, secondSegmentXLocation, row)

        if state == 8:
            first_segment = self.CardSegment(Card._card_id, Card.CardColor.RED, Card.CardSymbol.WHITE_DOT, firstSegmentXLocation, row)
            secondSegmentYLocation = self._getYLocationIndexAbove(row)
            second_segment = self.CardSegment(Card._card_id, Card.CardColor.WHITE, Card.CardSymbol.BLACK_DOT, firstSegmentXLocation, secondSegmentYLocation)

        return [first_segment, second_segment]
    
    def __str__(self):
        return '''
        State: {}
        Location: {}
        ID: {}
        Segments: \n{}\n{}
        '''.format(self._state, self._location, self._card_id, str(self._segments[0]), str(self._segments[1]))

    def __eq__(self, otherCard):
        if otherCard is None:
            return False

        return (self._card_id == otherCard._card_id
                and self._location == otherCard._location
                and self._state == otherCard._state
                and self._segments[0] == otherCard._segments[0]
                and self._segments[1] == otherCard._segments[1])

    def __hash__(self):
        return hash((self._segments[0], self._segments[1]))

    # def _getAdjacentLocation(self, state, col, row):

    #     right = {
    #         'A': 'B',
    #         'B': 'C',
    #         'C': 'D',
    #         'D': 'E',
    #         'E': 'F',
    #         'F': 'G',
    #         'H': None,
    #     }

    #     if state in [1, 3, 5, 7]:
    #         return '{}{}'.format(right[col.upper()], row)
    #     elif state in [2, 4, 6, 8]:
    #         return '{}{}'.format(row, row - 1)
    #     else:
    #         raise ValueError()
        
    class CardSegment:
        def __init__(self, parent, color, symbol, locationX, locationY):
            self._parent = parent
            self._color = color
            self._symbol = symbol
            self._locationX = locationX
            self._locationY = 12 - int(locationY)

        def getParent(self):
            return self._parent

        def getColor(self):
            if self._color == Card.CardColor.RED:
                return 'RED'
                
            return 'WHITE'

        def getSymbol(self):
            if self._symbol == Card.CardSymbol.WHITE_DOT:
                return 'WDOT'
            
            return 'BDOT'

        def getLocationX(self):
            return self._locationX

        def getLocationY(self):
            return self._locationY

        def setLocation(self, location):
            self._location = location

        def __str__(self):
            return '''
            Parent ID: {}
            Color: {}
            Symbol: {}
            X Location: {}
            Y Location: {}
            '''.format(self._parent, self._color, self._symbol, self._locationX, self._locationY)

        def __eq__(self, otherSegment):
            if otherSegment is None:
                return False

            return (self._parent == otherSegment._parent
                    and self._color == otherSegment._color
                    and self._symbol == otherSegment._symbol
                    and self._locationX == otherSegment._locationX
                    and self._locationY == otherSegment._locationY)
        
        def __hash__(self):
            return hash((self._color, self._symbol, self._locationX, self._locationY))