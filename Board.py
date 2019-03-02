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
        self._winningMarkers = []

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
        self._profHeuristic()    
        #print("The heuristice for Dots is : ",self.heuristic("DOTS"))  
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
    
    def getWinningMarkers(self):
        return self._winningMarkers
    
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
        win = False
        if self._horizontalCheckDots(firstSegment, 'WDOT') or self._horizontalCheckDots(secondSegment, 'BDOT'):
            win = True
            self._winningMarkers.append(Player.Marker.DOTS)
        if self._horizontalCheckColors(firstSegment, 'WHITE') or self._horizontalCheckColors(secondSegment, 'RED'):
            win = True
            self._winningMarkers.append(Player.Marker.COLOR)

        return win

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
        win = False
        if self._verticalCheckDots(firstSegment, 'WDOT') or self._verticalCheckDots(secondSegment, 'BDOT'):
            win = True
            self._winningMarkers.append(Player.Marker.DOTS)
        if self._verticalCheckColors(firstSegment, 'WHITE') or self._verticalCheckColors(secondSegment, 'RED'):
            win = True
            self._winningMarkers.append(Player.Marker.COLOR)

        return win

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
        win = False
        if self._firstDiagonalDots() or self._secondDiagonalDots():
            win = True
            self._winningMarkers.append(Player.Marker.DOTS)
        if self._firstDiagonalColors() or self._secondDiagonalColors():
            win = True
            self._winningMarkers.append(Player.Marker.COLOR)

        return win

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

    def heuristic(self,typeOfAI):
        # Algorithm
        # Look for 4 consecutive segment
        # if segment is NONE +5points
        # if 1 segment of correct type +10points
        # 2 consecutives +50points
        # 3 consecutives +100points
        # 4 consecutives +1 000 000points
        # SPECIAL CASE -10points if the the opposite type break the sequence ex: the opposite of WhiteDots is BlackDots

        if typeOfAI == Player.Marker.DOTS:
            return (self._heuristicDots(True) - self._heuristicColors(False))
        else :
            return (self._heuristicColors(True) - self._heuristicDots(False))

    def _heuristicDots(self,isAI) :
        total = 0
        total = total + self._horizontalInARowDots('WDOT',isAI)
        total = total + self._horizontalInARowDots('BDOT',isAI)

        total = total + self._verticalInARowDots('WDOT',isAI)
        total = total + self._verticalInARowDots('BDOT',isAI)

        #\
        total = total + self._firstDiagonalInARowDots('WDOT',isAI)
        total = total + self._firstDiagonalInARowDots('BDOT',isAI)

        #/
        total = total + self._secondDiagonalInARowDots('WDOT',isAI)
        total = total + self._secondDiagonalInARowDots('BDOT',isAI)
        print("Dots total:",total)
        return total
    def _heuristicColors(self,isAI):
        total = 0
        total = total + self._horizontalInARowColors('WHITE',isAI)
        total = total + self._horizontalInARowColors('RED',isAI)

        total = total + self._verticalInARowColors('WHITE',isAI)
        total = total + self._verticalInARowColors('RED',isAI)

        #\
        total = total + self._firstDiagonalInARowColors('WHITE',isAI)
        total = total + self._firstDiagonalInARowColors('RED',isAI)

        #/
        total = total + self._secondDiagonalInARowColors('WHITE',isAI)
        total = total + self._secondDiagonalInARowColors('RED',isAI)
        print("Colors total:",total)
        return total
    
    def _horizontalInARowDots(self,dotType,isAI):
        subTotal=0
        for y in range(0,12):
            for x in range(1,6):
                if subTotal >= 1000000:
                    return subTotal
                counter=0
                counter,subTotal = self._checkFourInARowDot(self._board[x][y],dotType,counter,subTotal,isAI)
                counter,subTotal = self._checkFourInARowDot(self._board[x+1][y],dotType,counter,subTotal,isAI)
                counter,subTotal = self._checkFourInARowDot(self._board[x+2][y],dotType,counter,subTotal,isAI)
                counter,subTotal = self._checkFourInARowDot(self._board[x+3][y],dotType,counter,subTotal,isAI)
        return subTotal
    def _verticalInARowDots(self,dotType,isAI):
        subTotal=0
        for y in range(0,9):
            for x in range(1,9):
                if subTotal >= 1000000:
                    return subTotal
                counter=0
                counter,subTotal = self._checkFourInARowDot(self._board[x][y],dotType,counter,subTotal,isAI)
                counter,subTotal = self._checkFourInARowDot(self._board[x][y+1],dotType,counter,subTotal,isAI)
                counter,subTotal = self._checkFourInARowDot(self._board[x][y+2],dotType,counter,subTotal,isAI)
                counter,subTotal = self._checkFourInARowDot(self._board[x][y+3],dotType,counter,subTotal,isAI)
        return subTotal

    def _firstDiagonalInARowDots(self,dotType,isAI):
        subTotal=0
        for y in range(9):
            for x in range(1, 6):
                if subTotal >= 1000000:
                    return subTotal
                counter=0
                counter,subTotal = self._checkFourInARowDot(self._board[x][y],dotType,counter,subTotal,isAI)
                counter,subTotal = self._checkFourInARowDot(self._board[x+1][y+1],dotType,counter,subTotal,isAI)
                counter,subTotal = self._checkFourInARowDot(self._board[x+2][y+2],dotType,counter,subTotal,isAI)
                counter,subTotal = self._checkFourInARowDot(self._board[x+3][y+3],dotType,counter,subTotal,isAI)
        return subTotal
    def _secondDiagonalInARowDots(self,dotType,isAI):
        subTotal=0
        for y in range(3,12):
            for x in range(1, 6):
                if subTotal >= 1000000:
                    return subTotal
                counter=0
                counter,subTotal = self._checkFourInARowDot(self._board[x][y],dotType,counter,subTotal,isAI)
                counter,subTotal = self._checkFourInARowDot(self._board[x+1][y-1],dotType,counter,subTotal,isAI)
                counter,subTotal = self._checkFourInARowDot(self._board[x+2][y-2],dotType,counter,subTotal,isAI)
                counter,subTotal = self._checkFourInARowDot(self._board[x+3][y-3],dotType,counter,subTotal,isAI)
        return subTotal
    
    def _checkFourInARowDot(self,element,dotType,counter,subTotal,isAI):
        if element is None :
            counter = 0
            subTotal = subTotal + 5 
            return counter,subTotal
        if element.getSymbol() == dotType :
            counter,subTotal = self._howManyInARow(counter)
            return counter,subTotal
        else :
            counter = 0
            if isAI :
                subTotal = subTotal - 10
            else :
                subTotal = subTotal -5
            return counter,subTotal



    def _horizontalInARowColors(self,colors,isAI):
        subTotal=0
        for y in range(0,12):
            for x in range(1,6):
                if subTotal >= 1000000:
                    return subTotal
                counter=0
                counter,subTotal = self._checkFourInARowColors(self._board[x][y],colors,counter,subTotal,isAI)
                counter,subTotal = self._checkFourInARowColors(self._board[x+1][y],colors,counter,subTotal,isAI)
                counter,subTotal = self._checkFourInARowColors(self._board[x+2][y],colors,counter,subTotal,isAI)
                counter,subTotal = self._checkFourInARowColors(self._board[x+3][y],colors,counter,subTotal,isAI)
        return subTotal
    def _verticalInARowColors(self,colors,isAI):
        subTotal=0
        for y in range(0,9):
            for x in range(1,9):
                if subTotal >= 1000000:
                    return subTotal
                counter=0
                counter,subTotal = self._checkFourInARowColors(self._board[x][y],colors,counter,subTotal,isAI)
                counter,subTotal = self._checkFourInARowColors(self._board[x][y+1],colors,counter,subTotal,isAI)
                counter,subTotal = self._checkFourInARowColors(self._board[x][y+2],colors,counter,subTotal,isAI)
                counter,subTotal = self._checkFourInARowColors(self._board[x][y+3],colors,counter,subTotal,isAI)
        return subTotal

    def _firstDiagonalInARowColors(self,colors,isAI):
        subTotal=0
        for y in range(9):
            for x in range(1, 6):
                if subTotal >= 1000000:
                    return subTotal
                counter=0
                counter,subTotal = self._checkFourInARowColors(self._board[x][y],colors,counter,subTotal,isAI)
                counter,subTotal = self._checkFourInARowColors(self._board[x+1][y+1],colors,counter,subTotal,isAI)
                counter,subTotal = self._checkFourInARowColors(self._board[x+2][y+2],colors,counter,subTotal,isAI)
                counter,subTotal = self._checkFourInARowColors(self._board[x+3][y+3],colors,counter,subTotal,isAI)
        return subTotal
    def _secondDiagonalInARowColors(self,colors,isAI):
        subTotal=0
        for y in range(3,12):
            for x in range(1, 6):
                if subTotal >= 1000000:
                    return subTotal
                counter=0
                counter,subTotal = self._checkFourInARowColors(self._board[x][y],colors,counter,subTotal,isAI)
                counter,subTotal = self._checkFourInARowColors(self._board[x+1][y-1],colors,counter,subTotal,isAI)
                counter,subTotal = self._checkFourInARowColors(self._board[x+2][y-2],colors,counter,subTotal,isAI)
                counter,subTotal = self._checkFourInARowColors(self._board[x+3][y-3],colors,counter,subTotal,isAI)
        return subTotal
    
    def _checkFourInARowColors(self,element,colors,counter,subTotal,isAI):
        if element is None :
            counter = 0
            subTotal = subTotal + 5 
            return counter,subTotal
        if element.getColor() == colors :
            counter,subTotal = self._howManyInARow(counter)
            return counter,subTotal
        else :
            counter = 0
            if isAI :
                subTotal = subTotal - 10
            else :
                subTotal = subTotal - 5
            return counter,subTotal

    def _howManyInARow(self,counter):
        if counter == 0:
            counter = counter + 1
            return counter,10
        elif counter == 1:
            counter = counter + 1
            return counter,40
        elif counter == 2:
            counter = counter + 1
            return counter,50
        elif counter == 3:
            counter = counter + 1
            return counter,1000000

    def _profHeuristic(self):
        self._FakeBoard = [[None for column in range(13)] for row in range(9)]
        for row in range(0,12):
            self._FakeBoard[0][row] = 12-row

        self._FakeBoard[1][12] = " A  "
        self._FakeBoard[2][12] = " B  "
        self._FakeBoard[3][12] = " C  "
        self._FakeBoard[4][12] = " D  "
        self._FakeBoard[5][12] = " E  "
        self._FakeBoard[6][12] = " F  "
        self._FakeBoard[7][12] = " G  "
        self._FakeBoard[8][12] = " H  "
        
        self._FakeBoard[0][12] = 0

        for y in range (0,12):
            for x in range(1,9):
                self._FakeBoard[x][y] = 110 -(10*y) +x

        countWhiteO =0
        a = [0]
        countWhiteX =0
        b = [0]
        countRedX = 0
        c = [0]
        countRedO =0
        d = [0]

        for y in range (0,12):
            for x in range(1,9):
                if self._board[x][y] is not None:
                    if self._board[x][y].getColor() == "WHITE" and self._board[x][y].getSymbol() == "WDOT":
                        countWhiteO = countWhiteO + self._FakeBoard[x][y]
                        a.append(self._FakeBoard[x][y])
                    if self._board[x][y].getColor() == "WHITE" and self._board[x][y].getSymbol() == "BDOT":
                        countWhiteX = countWhiteX + 3*self._FakeBoard[x][y]
                        b.append(self._FakeBoard[x][y])
                    if self._board[x][y].getColor() == "RED" and self._board[x][y].getSymbol() == "BDOT":
                        countRedX = countRedX + 2*self._FakeBoard[x][y]
                        c.append(self._FakeBoard[x][y])
                    if self._board[x][y].getColor() == "RED" and self._board[x][y].getSymbol() == "WDOT":
                        countRedO = countRedO + 1.5*self._FakeBoard[x][y]
                        d.append(self._FakeBoard[x][y])
        print("PROF HEURISTIC")
        print(countWhiteO + countWhiteX - countRedX - countRedO)
        print(a)
        print(b)
        print(c)
        print(d)


      #  for column in range(13):
       #     printRow = ""
        #    for row in range(9):
         #       if column == 12 or row == 0:
          #          if row == 0 and self._FakeBoard[row][column] <10:
           #             printRow += "  "+str(self._FakeBoard[row][column])+"   |"
            #        else:
             #           printRow += "  "+str(self._FakeBoard[row][column])+"  |"
              #  else:
               #     if self._FakeBoard[row][column] == None:
                #        printRow += "  "+str(self._FakeBoard[row][column])+"  |"
                 #   else:
                  #      printRow += "   "+str(self._FakeBoard[row][column])+"   |"
            #print(printRow)

    def _findLowestOpenCell(self, col):
        column = self._board[col]
        for i in range(13):
            if column[12-i] is None:
                return i

        return None

    def _validateVerticalPosition(self, currentCol, lowestCellInCol):
        if self._board[currentCol][12-lowestCellInCol] is None:
            cellAbove = 12-lowestCellInCol-1
            if cellAbove < 0:
                return None
            
            if self._board[currentCol][cellAbove] is None:
                return (currentCol, lowestCellInCol)

    def _getAvailableCellsVerticalCard(self):
        validPositions = []
        for i in range(1,9):
            lowestOpenCellInColumn = self._findLowestOpenCell(i)
            position = self._validateVerticalPosition(i, lowestOpenCellInColumn)
            if position is not None:
                validPositions.append(position) 

        return validPositions

    def _validateHorizontalPosition(self, currentCol, lowestCellInCol):
        if (self._board[currentCol][12-lowestCellInCol] is None 
            and self._board[currentCol+1][12-lowestCellInCol] is None
            and self._board[currentCol+1][12-lowestCellInCol+1] is not None):
            return (currentCol, lowestCellInCol)

        return None
    
    def _getAvailableCellsHorizontalCard(self): 
        validPositions = []
        for i in range(1,8):
            lowestOpenCellInColumn = self._findLowestOpenCell(i)
            position = self._validateHorizontalPosition(i, lowestOpenCellInColumn)
            if position is not None:
                validPositions.append(position)

        return validPositions
    
if __name__ == '__main__':
    b = Board(24)
    c1 = Card(5, ['A', '1'])
    c2 = Card(5, ['A', '2'])
    c3 = Card(5, ['A', '3'])
    c4 = Card(5, ['A', '4'])
    c5 = Card(5, ['A', '5'])
    c6 = Card(5, ['A', '6'])
    c7 = Card(5, ['A', '7'])
    c8 = Card(5, ['A', '8'])
    c9 = Card(5, ['A', '9'])
    c10 = Card(5, ['A', '10'])
    c11 = Card(5, ['A', '11'])
    c12 = Card(4, ['C', '1'])
    c13 = Card(5, ['D', '1'])
    c14 = Card(4, ['F', '1'])
    c15 = Card(4, ['H', '1'])

    b.addCard(c1)
    b.addCard(c2)
    b.addCard(c3)
    b.addCard(c4)
    b.addCard(c5)
    b.addCard(c6)
    b.addCard(c7)
    b.addCard(c8)
    b.addCard(c9)
    b.addCard(c10)
    b.addCard(c11)
    b.addCard(c12)
    b.addCard(c13)
    b.addCard(c14)
    b.addCard(c15)

    b.printBoard()

    print('Open horizontal positions: ', b._getAvailableCellsHorizontalCard())
    print('Open vertical positions: ', b._getAvailableCellsVerticalCard())
