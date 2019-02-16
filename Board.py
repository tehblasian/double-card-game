from Card import Card
from Player import Player

class Board:
    #initializing the board 8x12
    #ititializing first column with NUMBERS and first row with LETTERS
    def __init__(self, maxCardsAllowed):
        self._board = [[None for column in range(13)] for row in range(9)]
        self._cards = []
        self._lastCardPlayed = None
        self._MAX_CARDS_ALLOWED = maxCardsAllowed

        for row in range(0,12):
            self._board[0][row] = 12-row

        self._board[1][12] = " A  "
        self._board[2][12] = " B  "
        self._board[3][12] = " C  "
        self._board[4][12] = " D  "
        self._board[5][12] = " E  "
        self._board[6][12] = " F  "
        self._board[7][12] = " G  "
        self._board[8][12] = " H  "
        
        self._board[0][12] = 0
    
    def printBoard(self):
        for column in range(13):
            printRow = ""
            for row in range(9):
                if column == 12 or row == 0:
                    if row == 0 and self._board[row][column] <10:
                        printRow += "  "+str(self._board[row][column])+"   |"
                    else:
                        printRow += "  "+str(self._board[row][column])+"  |"
                else:
                    if self._board[row][column] == None:
                        printRow += "  "+str(self._board[row][column])+"  |"
                    else:
                        printRow += "  "+str(self._board[row][column].getColor()[0:1])+"_"+str(self._board[row][column].getSymbol()[0:2])+"  |"
            print(printRow)
            
    def getCards(self):
        return self._cards

    def getLastCardPlayed(self):
        return self._lastCardPlayed
    
    def addCard(self, card, recycled=False):
        firstSegment = card.getSegments()[0]
        secondSegment = card.getSegments()[1]

        if self._validateSegmentPosition(firstSegment,secondSegment) and self._validateSegmentPosition(secondSegment,firstSegment):
            self._addCardOnBoard(firstSegment,secondSegment)
            if not recycled:
                self._cards.append(card)

            self._lastCardPlayed = card
            return True
            
        return False

    def recycleCard(self, oldCard, newCard):
        recycled = self.addCard(newCard, recycled=True)

        # if the card was not recycled, revert the card to its original state before modification
        if not recycled:
            newCard = oldCard
            return False

        # delete the old card from the board
        segment1, segment2 = oldCard.getSegments()
        self._board[segment1.getLocationX()][segment1.getLocationY()] = None
        self._board[segment2.getLocationX()][segment2.getLocationY()] = None

        self._lastCardPlayed = newCard

        return True

    def getCardToRecycle(self, fromLocationArr):
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

        first_segment_x_location_letter = fromLocationArr[0]
        first_segment_y_location = 12 - int(fromLocationArr[1])
        second_segment_x_location_letter = fromLocationArr[2]
        second_segment_y_location = 12 - int(fromLocationArr[3])

        first_segment_x_location = indices[first_segment_x_location_letter.upper()]
        second_segment_x_location = indices[second_segment_x_location_letter.upper()]

        # find the card to recycle 
        card_to_recycle = None
        for card in self._cards:
            segment1, segment2 = card.getSegments()
            if (segment1.getLocationX() == first_segment_x_location 
                and segment1.getLocationY() == first_segment_y_location
                and segment2.getLocationX() == second_segment_x_location
                and segment2.getLocationY() == second_segment_y_location):
                    card_to_recycle = card
                    break
        
        # check if recycling the card does not leave the board in an illegal state
        if self._canRecycleCard(card_to_recycle):
            return card_to_recycle
    
        return None

    def hasWinner(self):
        firstSegment, secondSegment = self._lastCardPlayed.getSegments()
        return self._horizontalWin(firstSegment, secondSegment) or self._verticalWin(firstSegment, secondSegment) or self._diagonalWin()
    
    def _validateSegmentPosition(self, segment1, segmentTocompare):
        return not self._illegalPosition(segment1,segmentTocompare)

    def _illegalPosition(self, segment1, segmentTocompare):
        positionX = int(segment1.getLocationX())
        positionY = int(segment1.getLocationY())

        if positionX <= 0 or positionX > 8 or positionY <= 0 or positionY > 12:
            return True

        if self._board[positionX][positionY] != None:
            return True

        if self._board[positionX][positionY + 1] == None and segmentTocompare.getLocationY() != positionY + 1:
            return True
            
        return False

    def _addCardOnBoard(self, firstSegment, secondSegment):
        self._board[firstSegment.getLocationX()][firstSegment.getLocationY()] = firstSegment
        self._board[secondSegment.getLocationX()][secondSegment.getLocationY()] = secondSegment

    def _canRecycleCard(self, card):
        segment1, segment2 = card.getSegments()
        return (len(self._cards) == self._MAX_CARDS_ALLOWED
                and self._board[segment1.getLocationX()][segment1.getLocationY() - 1] is None 
                and self._board[segment2.getLocationX()][segment2.getLocationY() - 1] is None
                and card != self._lastCardPlayed)

    def _horizontalWin(self, firstSegment, secondSegment):
        return (self._horizontalCheckDots(firstSegment, 'WDOT') 
            or self._horizontalCheckDots(secondSegment, 'BDOT')
            or self._horizontalCheckColors(firstSegment, 'WHITE') 
            or self._horizontalCheckColors(secondSegment, 'RED'))

    def _horizontalCheckDots(self, segment, symbol):
        countWhiteDots=0
        countBlackDots=0
        for eachColumn in range(1, 9):
            if self._board[eachColumn][segment.getLocationY()] != None:
                if str(self._board[eachColumn][segment.getLocationY()].getSymbol()) == symbol:
                    countWhiteDots += 1
                    countBlackDots = 0
                else:
                    countWhiteDots = 0
                    countBlackDots += 1
                if countWhiteDots == 4 or countBlackDots == 4:
                    return True
            else:
                countWhiteDots = 0
                countBlackDots = 0

        return False

    def _horizontalCheckColors(self, segment, color):
        countWhiteCards = 0
        countRedCards = 0
        for eachColumn in range(1, 9):
            if self._board[eachColumn][segment.getLocationY()] != None:
                if str(self._board[eachColumn][segment.getLocationY()].getColor()) == color:
                    countWhiteCards += 1
                    countRedCards = 0
                else:
                    countWhiteCards = 0
                    countRedCards += 1
                if countWhiteCards == 4 or countRedCards == 4:
                    return True
            else:
                countWhiteCards = 0
                countRedCards = 0

        return False
        
    def _verticalWin(self, firstSegment, secondSegment):
        return (self._verticalCheckDots(firstSegment, 'WDOT') 
            or self._verticalCheckDots(secondSegment, 'BDOT')
            or self._verticalCheckColors(firstSegment, 'WHITE')
            or self._verticalCheckColors(secondSegment, 'RED'))

    def _verticalCheckDots(self, segment, symbol):
        countWhiteDots = 0
        countBlackDots = 0
        for eachRow in range(12):
            if self._board[segment.getLocationX()][eachRow] != None:
                if str(self._board[segment.getLocationX()][eachRow].getSymbol()) == symbol:
                    countWhiteDots += 1
                    countBlackDots = 0
                else:
                    countWhiteDots = 0
                    countBlackDots += 1
                if countWhiteDots == 4 or countBlackDots == 4:
                    return True
            else:
                countWhiteDots = 0
                countBlackDots = 0 

        return False       
        
    def _verticalCheckColors(self, segment, symbol):
        countWhiteCards = 0
        countRedCards = 0
        for eachRow in range(12):
            if self._board[segment.getLocationX()][eachRow] != None:
                if str(self._board[segment.getLocationX()][eachRow].getColor()) == symbol:
                    countWhiteCards += 1
                    countRedCards = 0
                else:
                    countWhiteCards = 0
                    countRedCards += 1
                if countWhiteCards == 4 or countRedCards == 4:
                    return True
            else:
                countWhiteCards = 0
                countRedCards = 0

        return False
    
    def _diagonalWin(self):
        if self._firstDiagonalDots() or self._secondDiagonalDots():
            self._winner = Player.Marker.DOTS
            return True
        elif self._firstDiagonalColors() or self._secondDiagonalColors():
            self._winner = Player.Marker.COLOR
            return True

        return False  

    #\Dots
    def _firstDiagonalDots(self):
        for y in range(9):
            for x in range(1, 6):
                if self._board[x][y] != None and self._board[x+1][y+1] != None and self._board[x+2][y+2] != None and self._board[x+3][y+3] != None:
                    if self._board[x][y].getSymbol() == self._board[x+1][y+1].getSymbol():
                        if self._board[x+1][y+1].getSymbol() == self._board[x+2][y+2].getSymbol():
                            if self._board[x+2][y+2].getSymbol() == self._board[x+3][y+3].getSymbol():
                                return True
        return False 

    #/Dots
    def _secondDiagonalDots(self):
        for y in range(3, 12):
            for x in range(1, 6):
                if self._board[x][y] != None and self._board[x+1][y-1] != None and self._board[x+2][y-2] != None and self._board[x+3][y-3] != None:
                    if self._board[x][y].getSymbol() == self._board[x+1][y-1].getSymbol():
                        if self._board[x+1][y-1].getSymbol() == self._board[x+2][y-2].getSymbol():
                            if self._board[x+2][y-2].getSymbol() == self._board[x+3][y-3].getSymbol():
                                return True
        return False

    #\Colors
    def _firstDiagonalColors(self):
        for y in range(9):
            for x in range(1, 6):
                if self._board[x][y] != None and self._board[x+1][y+1] != None and self._board[x+2][y+2] != None and self._board[x+3][y+3] != None:
                    if self._board[x][y].getColor() == self._board[x+1][y+1].getColor():
                        if self._board[x+1][y+1].getColor() == self._board[x+2][y+2].getColor():
                            if self._board[x+2][y+2].getColor() == self._board[x+3][y+3].getColor():
                                return True
        return False  

    #/Colors
    def _secondDiagonalColors(self):
        for y in range(3, 12):
            for x in range(1, 6):
                if self._board[x][y] != None and self._board[x+1][y-1] != None and self._board[x+2][y-2] != None and self._board[x+3][y-3] != None:
                    if self._board[x][y].getColor() == self._board[x+1][y-1].getColor():
                        if self._board[x+1][y-1].getColor() == self._board[x+2][y-2].getColor():
                            if self._board[x+2][y-2].getColor() == self._board[x+3][y-3].getColor():
                                return True
        return False
