from Card import Card
from Player import Player

class Board:
    
    #initializing the board 8x12
    #ititializing first column with NUMBERS and first row with LETTERS
    def __init__(self):
        self.board = [[None for column in range(13)] for row in range(9)]

        for row in range(0,12):
            self.board[0][row] = 12-row

        self.board[1][12] = " A  "
        self.board[2][12] = " B  "
        self.board[3][12] = " C  "
        self.board[4][12] = " D  "
        self.board[5][12] = " E  "
        self.board[6][12] = " F  "
        self.board[7][12] = " G  "
        self.board[8][12] = " H  "
        
        self.board[0][12] = 0
    
    def printBoard(self):
        for column in range(13):
            printRow = ""
            for row in range(9):
                if column == 12 or row == 0 :
                    if row == 0 and self.board[row][column] <10 :
                        printRow += "  "+str(self.board[row][column])+"   |"
                    else:
                        printRow += "  "+str(self.board[row][column])+"  |"
                else :
                    if self.board[row][column] == None :
                        printRow += "  "+str(self.board[row][column])+"  |"
                    else:
                        printRow += "  "+str(self.board[row][column].getColor()[0:1])+"_"+str(self.board[row][column].getSymbol()[0:2])+"  |"
            print(printRow)
            
    #this is the method you call not the sub-one except if you need them
    def addCard(self,card):
        firstSegment = card.getSegments()[0]
        secondSegment = card.getSegments()[1]

        print(firstSegment)
        print(secondSegment)

        if self.valideSegmentPosition(firstSegment,secondSegment) and self.valideSegmentPosition(secondSegment,firstSegment) :
            self.addCardOnBoard(firstSegment,secondSegment)
            return True # can also return "Card added on board"
        return False # can also return "Move cannot be done"

    def valideSegmentPosition(self,segment1,segmentTocompare):
        if self.illegalPosition(segment1,segmentTocompare) :
            return False
        return True

    def illegalPosition(self,segment1,segmentTocompare):
        positionX = int(segment1.getLocationX())
        positionY = int(segment1.getLocationY())

        if positionX <=0 or positionX > 8 or positionY <= 0 or positionY >12 :
            return True

        if self.board[positionX][positionY] != None :
            return True

        if self.board[positionX][positionY + 1 ] == None and segmentTocompare.getLocationY() != positionY + 1 :
            return True
            
        return False

    def addCardOnBoard(self,firstSegment,secondSegment):
        self.board[firstSegment.getLocationX()][firstSegment.getLocationY()] = firstSegment
        self.board[secondSegment.getLocationX()][secondSegment.getLocationY()] = secondSegment
    
    #this is the method you call not the sub-one except if you need them
    def moveCard(self,card,firstSegmentXLocation,firstSegmentYLocation,secondSegmentXLocation,secondSegmentYLocation):
        firstSegment = card.getSegments()[0]
        secondSegment = card.getSegments()[1]
        if self.canMoveCard(firstSegment,firstSegmentXLocation,firstSegmentYLocation,secondSegmentXLocation,secondSegmentYLocation) and self.canMoveCard(secondSegment,secondSegmentXLocation,secondSegmentYLocation,firstSegmentXLocation,firstSegmentYLocation) :
            self.board[firstSegmentXLocation][firstSegmentYLocation] =firstSegment
            self.board[secondSegmentXLocation][secondSegmentYLocation] =secondSegment
            self.board[firstSegment.getLocationX()][firstSegment.getLocationY()] =None
            self.board[secondSegment.getLocationX()][secondSegment.getLocationY()] =None

            return True
        return False
        
    def canMoveCard(self,segment,newLocationX,newLocationY,newLocationXSecond,newLocationYSecond):
        if newLocationX <=0 or newLocationX > 8 or newLocationY <= 0 or newLocationY >12 :
            #not inside the Board
            return False
        if segment.getLocationX() == newLocationX and segment.getLocationY() == newLocationY:
            #same location
            return False
        if self.board[segment.getLocationX()][segment.getLocationY()-1] != None and self.board[segment.getLocationX()][segment.getLocationY() -1].getParent() != segment.getParent():
            #check if the block onTopOf is from the same parents
            
            return False
        if self.board[newLocationX][newLocationY] != None :
            #check if the new location is empty
            
            return False
        if self.board[newLocationX][newLocationY+1] == None and newLocationY+1 != 12:
            if newLocationX != newLocationXSecond and newLocationXSecond != newLocationY+1:
                return False
        return True
        
        
    #this is the method you call not the sub-one except if you need them
    #Can use this method twice for each Player for the same card put in the board
    def isWinner(self,player,card) :
        firstSegment = card.getSegments()[0]
        secondSegment = card.getSegments()[1]
        if self.horizontalWin(player,firstSegment,secondSegment) or self.verticalWin(player,firstSegment,secondSegment) or self.diagonalWin(player) : 
            return True
        return False

    def horizontalWin(self,player,firstSegment,secondSegment) :
        if player.getMarker() == Player.Marker.DOTS :
            if self.horizontalCheckDots(firstSegment,Card.CardSymbol.WHITE_DOT) or self.horizontalCheckDots(secondSegment,Card.CardSymbol.WHITE_DOT) :
                return True
            return False
        else :
            if self.horizontalCheckColors(firstSegment,Card.CardColor.WHITE) or self.horizontalCheckColors(secondSegment,Card.CardColor.WHITE) :
                return True
            return False    

    def horizontalCheckDots(self,segment,symbol) :
        countWhiteDots=0
        countBlackDots=0
        for eachColumn in range(1,9) :
            if self.board[eachColumn][segment.getLocationY()] != None :
                if str(self.board[eachColumn][segment.getLocationY()].getSymbol()) == symbol :
                    countWhiteDots += 1
                    countBlackDots = 0
                else :
                    countWhiteDots = 0
                    countBlackDots += 1
                if countWhiteDots == 4 or countBlackDots == 4 :
                    return True
            else :
                countWhiteDots=0
                countBlackDots=0
        return False

    def horizontalCheckColors(self,segment,color) :
        countWhiteCards=0
        countRedCards=0
        for eachColumn in range(1,9) :
            if self.board[eachColumn][segment.getLocationY()] != None:
                if str(self.board[eachColumn][segment.getLocationY()].getColor()) == color :
                    countWhiteCards += 1
                    countRedCards = 0
                else :
                    countWhiteCards = 0
                    countRedCards += 1
                if countWhiteCards == 4 or countRedCards == 4 :
                    return True
            else :
                countWhiteCards=0
                countRedCards=0
        return False
        
    def verticalWin(self,player,firstSegment,secondSegment) :
        if player.getMarker() == Player.Marker.DOTS :
            if self.verticalCheckDots(firstSegment,Card.CardSymbol.WHITE_DOT) or self.verticalCheckDots(secondSegment,Card.CardSymbol.WHITE_DOT) :
                return True
            return False
        else :
            if self.verticalCheckColors(firstSegment,Card.CardColor.WHITE) or self.verticalCheckColors(secondSegment,Card.CardColor.WHITE) :
                return True
            return False  
        pass

    def verticalCheckDots(self,segment,symbol):
        countWhiteDots=0
        countBlackDots=0
        for eachRow in range(12) :
            if self.board[segment.getLocationX()][eachRow] != None :
                if str(self.board[segment.getLocationX()][eachRow].getSymbol()) == symbol :
                    countWhiteDots += 1
                    countBlackDots = 0
                else :
                    countWhiteDots = 0
                    countBlackDots += 1
                if countWhiteDots == 4 or countBlackDots == 4 :
                    return True
            else :
                countWhiteDots=0
                countBlackDots=0 
        return False       
        
    def verticalCheckColors(self,segment,symbol):
        countWhiteCards=0
        countRedCards=0
        for eachRow in range(12) :
            if self.board[segment.getLocationX()][eachRow] != None :
                if str(self.board[segment.getLocationX()][eachRow].getColor()) == symbol :
                    countWhiteCards += 1
                    countRedCards = 0
                else :
                    countWhiteCards = 0
                    countRedCards += 1
                if countWhiteCards == 4 or countRedCards == 4 :
                    return True
            else :
                countWhiteCards=0
                countRedCards=0
        return False
    
    def diagonalWin(self,player) :
        if player.getMarker() == Player.Marker.DOTS :
            if self.firstDiagonalDots() or self.secondDiagonalDots() :
                return True
            return False
        else :
            if self.firstDiagonalColors() or self.secondDiagonalColors() :
                return True
            return False  
        pass

    #\Dots
    def firstDiagonalDots(self):
        for y in range(9):
            for x in range(1,6):
                if self.board[x][y] != None and self.board[x+1][y+1] != None and self.board[x+2][y+2] != None and self.board[x+3][y+3] != None :
                    if self.board[x][y].getSymbol() == self.board[x+1][y+1].getSymbol() :
                        if self.board[x+1][y+1].getSymbol() == self.board[x+2][y+2].getSymbol() :
                            if self.board[x+2][y+2].getSymbol() == self.board[x+3][y+3].getSymbol() :
                                return True
        return False 

    #/Dots
    def secondDiagonalDots(self):
        for y in range(3,12):
            for x in range(1,6):
                if self.board[x][y] != None and self.board[x+1][y-1] != None and self.board[x+2][y-2] != None and self.board[x+3][y-3] != None :
                    if self.board[x][y].getSymbol() == self.board[x+1][y-1].getSymbol() :
                        if self.board[x+1][y-1].getSymbol() == self.board[x+2][y-2].getSymbol() :
                            if self.board[x+2][y-2].getSymbol() == self.board[x+3][y-3].getSymbol() :
                                return True
        return False

    #\Colors
    def firstDiagonalColors(self):
        for y in range(9):
            for x in range(1,6):
                if self.board[x][y] != None and self.board[x+1][y+1] != None and self.board[x+2][y+2] != None and self.board[x+3][y+3] != None :
                    if self.board[x][y].getColor() == self.board[x+1][y+1].getColor() :
                        if self.board[x+1][y+1].getColor() == self.board[x+2][y+2].getColor() :
                            if self.board[x+2][y+2].getColor() == self.board[x+3][y+3].getColor() :
                                return True
        return False  

    #/Colors
    def secondDiagonalColors(self):
        for y in range(3,12):
            for x in range(1,6):
                if self.board[x][y] != None and self.board[x+1][y-1] != None and self.board[x+2][y-2] != None and self.board[x+3][y-3] != None :
                    if self.board[x][y].getColor() == self.board[x+1][y-1].getColor() :
                        if self.board[x+1][y-1].getColor() == self.board[x+2][y-2].getColor() :
                            if self.board[x+2][y-2].getColor() == self.board[x+3][y-3].getColor() :
                                return True
        return False



# TEST
# class Card:
#     def __init__(self,firstsegment,secondsegment):
#         self.segment = [0 for i in range(2)]
#         self.segment[0]=firstsegment
#         self.segment[1]=secondsegment

#     def getSegments(self):
#         return self.segment

# class Segment:
#     def __init__(self,x,y,symbol,color,parent):
#         self.locationx = x
#         self.locationy = y
#         self.symbol = symbol
#         self.color = color
#         self.parent = parent


#     def getLocationX(self):
#         return self.locationx
#     def getLocationY(self):
#         return self.locationy
#     def getSymbol(self):
#         return self.symbol
#     def getColor(self):
#         return self.color
#     def getParent(self):
#         return self.parent

# class Player:
#     def __init__(self,marker):
#         self.marker = marker
#     def getMarker(self):
#         return self.marker

# person1 = Player("DOTS")

# board1 = Board()
# segment1 = Segment(6,11,Card.CardSymbol.WHITE_DOT,Card.CardColor.WHITE,12)
# segment2 = Segment(6,10,"BLACK_DOT","RED",12)
# card1 = Card(segment1,segment2)

# print(board1.addCard(card1))
# board1.printBoard()


# segment1 = Segment(5,10,Card.CardSymbol.WHITE_DOT,Card.CardColor.WHITE,12)
# segment2 = Segment(5,11,"BLACK_DOT","RED",12)
# card1 = Card(segment1,segment2)

# print(board1.addCard(card1))
# board1.printBoard()

# segment1 = Segment(4,11,Card.CardSymbol.WHITE_DOT,Card.CardColor.WHITE,12)
# segment2 = Segment(4,10,"BLACK_DOT","RED",12)
# card1 = Card(segment1,segment2)

# print(board1.addCard(card1))
# board1.printBoard()



# segment1 = Segment(3,11,Card.CardSymbol.WHITE_DOT,Card.CardColor.WHITE,12)
# segment2 = Segment(3,10,"BLACK_DOT","RED",12)
# card1 = Card(segment1,segment2)

# print(board1.addCard(card1))
# board1.printBoard()

# segment1 = Segment(3,8,Card.CardSymbol.WHITE_DOT,Card.CardColor.WHITE,12)
# segment2 = Segment(3,9,"BLACK_DOT","RED",12)
# card1 = Card(segment1,segment2)

# print(board1.addCard(card1))
# board1.printBoard()

# segment1 = Segment(3,6,Card.CardSymbol.WHITE_DOT,Card.CardColor.WHITE,12)
# segment2 = Segment(3,7,"BLACK_DOT","RED",12)
# card2 = Card(segment1,segment2)

# print(board1.addCard(card2))
# board1.printBoard()

# segment1 = Segment(4,9,Card.CardSymbol.WHITE_DOT,Card.CardColor.WHITE,12)
# segment2 = Segment(5,9,"BLACK_DOT","RED",12)
# card1 = Card(segment1,segment2)


# print(board1.addCard(card1))
# board1.printBoard()
# print(board1.moveCard(card1,1,11,2,11))

# board1.printBoard()
# print(board1.moveCard(card2,1,9,1,10))

# board1.printBoard()

# segment1 = Segment(2,9,Card.CardSymbol.WHITE_DOT,Card.CardColor.WHITE,12)
# segment2 = Segment(2,10,"BLACK_DOT","RED",12)
# card1 = Card(segment1,segment2)
# print(board1.addCard(card1))
# board1.printBoard()

# print(board1.isWinner(person1,card1))