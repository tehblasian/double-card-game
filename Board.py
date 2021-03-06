import math
import random
from copy import deepcopy
from Card import Card
from Player import Player
import timeit
class Board:
    #initializing the board 8x12
    #ititializing first column with NUMBERS and first row with LETTERS
    def __init__(self, maxCardsAllowed):
        self._board = [[None for column in range(13)] for row in range(9)]
        self._cards = []
        self._recycled_cards = []
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
        #self._profHeuristic()    
        # start = timeit.default_timer()
        # print("The heuristice for Dots is : ",self.heuristic("DOTS"))  
        # print(timeit.default_timer() -start)
    def getCards(self):
        return self._cards

    def getLastCardPlayed(self):
        return self._lastCardPlayed
    
    def addCard(self, card, recycled=False):
        firstSegment = card.getSegments()[0]
        secondSegment = card.getSegments()[1]

        if self._validateSegmentPosition(firstSegment,secondSegment) and self._validateSegmentPosition(secondSegment,firstSegment):
            self._addCardOnBoard(firstSegment,secondSegment)
            if recycled:
                self._recycled_cards.append(card)
            elif not recycled:
                self._cards.append(card)

            self._lastCardPlayed = card
            return True
            
        return False

    def recycleCard(self, oldCard, newCard):
        # fail if new card has same state and location as new card
        if oldCard == newCard:
            return False
  
        # delete the old card from the board
        segment1, segment2 = oldCard.getSegments()
        self._board[segment1.getLocationX()][segment1.getLocationY()] = None
        self._board[segment2.getLocationX()][segment2.getLocationY()] = None

        recycled = self.addCard(newCard, recycled=True)

        # if the card was not recycled, revert the card to its original state before modification
        # re add the card to the board
        if not recycled:
            newCard = oldCard
            self._board[segment1.getLocationX()][segment1.getLocationY()] = segment1
            self._board[segment2.getLocationX()][segment2.getLocationY()] = segment2
            return False

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
        # TODO: the cards in self._cards arent all properly getting updated when recycling
        # find the card to recycle 
        card_to_recycle = None
        for card in (self._cards + self._recycled_cards):
            segment1, segment2 = card.getSegments()
            if ((segment1.getLocationX() == first_segment_x_location 
                and segment1.getLocationY() == first_segment_y_location
                and segment2.getLocationX() == second_segment_x_location
                and segment2.getLocationY() == second_segment_y_location)
                or (segment2.getLocationX() == first_segment_x_location 
                and segment2.getLocationY() == first_segment_y_location
                and segment1.getLocationX() == second_segment_x_location
                and segment1.getLocationY() == second_segment_y_location)):
                    card_to_recycle = card
                    break

        # check if recycling the card does not leave the board in an illegal state
        if self._canRecycleCard(card=card_to_recycle):
            return card_to_recycle
    
        return None

    def hasWinner(self):
        if self._lastCardPlayed is None:
            return False

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

    def _canRecycleCard(self, card=None, segment=None):
        if card is None and segment is None:
            return False

        if segment is None:
            segment1, segment2 = card.getSegments()
        else:
            segment1 = segment
            segment2 = segment.getSibling()

        if segment1.getState() % 2 == 0 and segment2.getState() % 2 == 0:
            return (len(self._cards) == self._MAX_CARDS_ALLOWED
                and self._board[segment2.getLocationX()][segment2.getLocationY() - 1] is None
                and segment1 not in self._lastCardPlayed.getSegments()
                and segment2 not in self._lastCardPlayed.getSegments())
        else:
            return (len(self._cards) == self._MAX_CARDS_ALLOWED
                and self._board[segment1.getLocationX()][segment1.getLocationY() - 1] is None 
                and self._board[segment2.getLocationX()][segment2.getLocationY() - 1] is None
                and segment1 not in self._lastCardPlayed.getSegments()
                and segment2 not in self._lastCardPlayed.getSegments())


    def _removeCard(self, segment):
        if segment is None:
            return False

        sibling = segment._sibling
        self._board[segment.getLocationX()][segment.getLocationY()] = None
        self._board[sibling.getLocationX()][sibling.getLocationY()] = None

        return True
        
    
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

    def regular_recycle_minimax(self, board, depth, ai_piece):
        recyclable = self._getRecyclableCards()

        best_state = None
        best_position = None
        best_score = -math.inf
        card_to_recycle = None
        traceArray =[0,0]
        for segment in recyclable:
            b = deepcopy(board)
            b._removeCard(segment)
            traceArraySegment =[0,0]
            state, position, score,traceArraySegment= b.regular_minimax(b, depth, True, ai_piece,traceArraySegment, initial_board_state=board)

            col, row = position
            if score > best_score:
                best_score = score
                best_position = position
                best_state = state
                card_to_recycle = segment
                traceArray=traceArraySegment

        print('Board before recycle')
        board.printBoard()
        board._removeCard(card_to_recycle)

        return best_state, best_position, best_score,traceArray

    
    def regular_minimax(self, board, depth, maximizing_player, ai_piece,traceArray, initial_board_state=None):
        available_positions = board._getAvailableCellsVerticalCard()
        
        # return score if depth is reached or node is terminal
        is_terminal_node = board.hasWinner()
        if depth == 0 or is_terminal_node:
            traceArray[0] = traceArray[0]+1
            #score = board.heuristic(ai_piece)
            score = board.heuristic(ai_piece)

            return None, None, score,traceArray

        if maximizing_player:
            best_score = -math.inf
            best_position = random.choice(available_positions)
            best_card_state = None

            # look at vertical positions 
            for position in available_positions:
                col, lowest_open_cell = position
                for state in range(1, 9):
                    # created fake board simulate a drop
                    b = deepcopy(board)
                    c = Card(state, [str(self._getColumnLetterFromIndex(col)), str(lowest_open_cell)])

                    legal_move = b.addCard(c)
                    if not legal_move:
                        continue

                    # ignore moves that leave the board in the same state as the initial (for recycling)
                    if initial_board_state is not None:
                        b_hash = hash(b)
                        ogb_hash = hash(initial_board_state)

                        if b_hash == ogb_hash:
                            pass
                    
                    minmaxValue = self.regular_minimax(b, depth-1, False, ai_piece,traceArray, initial_board_state=initial_board_state)
                    new_score = minmaxValue[2]
                    traceArray = minmaxValue[3]

                    # if the new score is better than the previous max, update
                    if new_score > best_score:
                        best_score = new_score
                        best_position = position
                        best_card_state = state
            if depth == 1:
                traceArray.append(best_score)
            if depth ==2:
                traceArray[1] = best_score
            return best_card_state, best_position, best_score,traceArray
        else:
            best_score = math.inf
            best_position = random.choice(available_positions)
            best_card_state = None
            for position in available_positions:
                col, lowest_open_cell = position
                for state in range(1, 9):
                    b = deepcopy(board)
                    c = Card(state, [str(self._getColumnLetterFromIndex(col)), str(lowest_open_cell)])

                    legal_move = b.addCard(c)
                    if not legal_move:
                        continue

                    # ignore moves that leave the board in the same state as the initial (for recycling)
                    if initial_board_state is not None:
                        b_hash = hash(b)
                        ogb_hash = hash(initial_board_state)

                        if b_hash == ogb_hash:
                            pass
                            
                    minmaxValue = self.regular_minimax(b, depth-1, True, ai_piece,traceArray, initial_board_state=initial_board_state)
                    new_score = minmaxValue[2]
                    traceArray = minmaxValue[3]

                    if new_score < best_score:
                        best_score = new_score
                        best_position = position
                        best_card_state = state
            if depth == 1:
                traceArray.append(best_score)
            if depth ==2:
                traceArray[1] = best_score
            return best_card_state, best_position, best_score,traceArray
    
    def minimax(self, board, depth, alpha, beta, maximizingPlayer, ai_piece, cache, initial_board_state=None):
        # if depth = 0 or node is a terminal node then
        #     return the heuristic value of node
        # if maximizingPlayer then
        #     value := −∞
        #     for each child of node do
        #         value := max(value, minimax(child, depth − 1, FALSE))
        #     return value
        # else (* minimizing player *)
        #     value := +∞
        #     for each child of node do
        #         value := min(value, minimax(child, depth − 1, TRUE))
        #     return value
        available_positions = board._getAvailableCellsVerticalCard()

        # here we will check if the score for this state has already been calculated
        # return the value or update alpha and beta if needed

        # get hash of board and check if in cache
        b_hash = hash(board)
        b_hash_entry = cache.get(b_hash)

        # only consider the stored value if we are at a greater or equal depth
        if b_hash_entry is not None and b_hash_entry[4] >= depth:
            entry_state = b_hash_entry[0]
            entry_position = b_hash_entry[1]
            entry_score = b_hash_entry[2]
            entry_type = b_hash_entry[3]

            # the stored score is from a leaf node
            if entry_type == 'EXACT':
                return entry_state, entry_position, entry_score

            # max player seeks to make alpha bigger
            if entry_type == 'LOWERBOUND':
                alpha = max(alpha, entry_score)

            # min player seeks to make beta smaller
            elif entry_type == 'UPPERBOUND':
                beta = min(beta, entry_score)

            
            # alpha-beta cutoff
            if alpha >= beta:
                return entry_state, entry_position, entry_score

        # return score if depth is reached or node is terminal
        is_terminal_node = board.hasWinner()
        if depth == 0 or is_terminal_node:
            score = board.heuristic(ai_piece)
      
            if score <= alpha:
                cache[b_hash] = (None, None, score, 'UPPERBOUND', depth)
            elif score >= beta:
                cache[b_hash] = (None, None, score, 'LOWERBOUND', depth)
            else:
                cache[b_hash] = (None, None, score, 'EXACT', depth)

            return None, None, score

        if maximizingPlayer:
            best_score = -math.inf
            best_position = random.choice(available_positions)
            best_card_state = None

            # look at vertical positions 
            for position in available_positions:
                col, lowest_open_cell = position
                for state in range(1, 9):
                    # created fake board simulate a drop
                    b = deepcopy(board)
                    c = Card(state, [str(self._getColumnLetterFromIndex(col)), str(lowest_open_cell)])
                    legal_move = b.addCard(c)
                    if not legal_move:
                        continue
                    new_score = self.minimax(b, depth-1, alpha, beta, False, ai_piece, cache)[2]

                    # if the new score is better than the previous max, update
                    if new_score > best_score:
                        best_score = new_score
                        best_position = position
                        best_card_state = state

                    # alpha beta pruning
                    alpha = max(alpha, best_score)
                    if alpha >= beta:
                        break

            if best_score <= alpha:
                cache[b_hash] = (state, position, new_score, 'UPPERBOUND', depth)
            if best_score >= beta:
                cache[b_hash] = (state, position, new_score, 'LOWERBOUND', depth)
            else:
                cache[b_hash] = (state, position, new_score, 'EXACT', depth)  
            return best_card_state, best_position, best_score
        else:
            best_score = math.inf
            best_position = random.choice(available_positions)
            best_card_state = None
            for position in available_positions:
                col, lowest_open_cell = position
                for state in range(1, 9):
                    # created fake board simulate a drop
                    b = deepcopy(board)
                    c = Card(state, [str(self._getColumnLetterFromIndex(col)), str(lowest_open_cell)])
                    legal_move = b.addCard(c)
                    if not legal_move:
                        continue

                    new_score = self.minimax(b, depth-1, alpha, beta, True, ai_piece, cache)[2]

                    if new_score < best_score:
                        best_score = new_score
                        best_position = position
                        best_card_state = state

                    # alpha-beta pruning
                    beta = min(beta, best_score)
                    if alpha >= beta:
                        break    

            if best_score <= alpha:
                cache[b_hash] = (state, position, new_score, 'UPPERBOUND', depth)
            if best_score >= beta:
                cache[b_hash] = (state, position, new_score, 'LOWERBOUND', depth)
            else:
                cache[b_hash] = (state, position, new_score, 'EXACT', depth)   

            return best_card_state, best_position, best_score

    
    def recycle_minimax(self, board, depth, ai_piece, cache):
        recyclable = self._getRecyclableCards()

        best_state = None
        best_position = None
        best_score = -math.inf
        card_to_recycle = None
        for segment in recyclable:
            b = deepcopy(board)
            b._removeCard(segment)

            state, position, score = b.minimax(b, depth, -math.inf, math.inf, True, ai_piece, cache, initial_board_state=None)

            # ensure that the best move found is not to play the same card in the same location and state
            col, row = position
            if score > best_score:
                best_score = score
                best_position = position
                best_state = state
                card_to_recycle = segment

        print('Board before recycle')
        board.printBoard()
        board._removeCard(card_to_recycle)

        return best_state, best_position, best_score
    
    def _getColumnLetterFromIndex(self, columnLetter):
        indices = {
            1: 'A',
            2: 'B',
            3: 'C',
            4: 'D',
            5: 'E',
            6: 'F',
            7: 'G',
            8: 'H',
        }

        return indices[columnLetter]
    
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

    def _score_window(self, window: list, marker, opponent_markers):
        window = [s.getSymbol() if s is not None else None for s in window]
        score = 0
        if window.count(marker) == 4:
            score += 1000000

        if window.count(marker) == 3 and window.count(None) == 1:
            score += 100000
        
        if window.count(marker) == 2 and window.count(None) == 2:
            score += 2000

        for opponent_marker in opponent_markers:
            if window.count(opponent_marker) == 3 and window.count(None) == 1:
                score -= 100000

        return score

    def _heuristicDots(self,isAI) :
        total = 0
        total = total + self._horizontalInARowDots('WDOT','BDOT',isAI)

        total = total + self._verticalInARowDots('WDOT','BDOT',isAI)

        #\
        total = total + self._firstDiagonalInARowDots('WDOT','BDOT',isAI)

        #/
        total = total + self._secondDiagonalInARowDots('WDOT','BDOT',isAI)
        # print("Dots total:",total)
        return total

    def _heuristicColors(self,isAI):
        total = 0
        total = total + self._horizontalInARowColors('WHITE','RED',isAI)

        total = total + self._verticalInARowColors('WHITE','RED',isAI)

        #\
        total = total + self._firstDiagonalInARowColors('WHITE','RED',isAI)

        #/
        total = total + self._secondDiagonalInARowColors('WHITE','RED',isAI)
        # print("Colors total:",total)
        return total
    
    def _horizontalInARowDots(self,whiteDot,blackDot,isAI):
        subTotal=0
        for y in range(0,12):   
            for x in range(1,6):
                counterWhite=0
                counterBlack=0

                counterWhite,subTotal = self._checkFourInARowDot(self._board[x][y],whiteDot,counterWhite,subTotal,isAI)
                counterWhite,subTotal = self._checkFourInARowDot(self._board[x+1][y],whiteDot,counterWhite,subTotal,isAI)
                counterWhite,subTotal = self._checkFourInARowDot(self._board[x+2][y],whiteDot,counterWhite,subTotal,isAI)
                counterWhite,subTotal = self._checkFourInARowDot(self._board[x+3][y],whiteDot,counterWhite,subTotal,isAI)

                counterBlack,subTotal = self._checkFourInARowDot(self._board[x][y],blackDot,counterBlack,subTotal,isAI)
                counterBlack,subTotal = self._checkFourInARowDot(self._board[x+1][y],blackDot,counterBlack,subTotal,isAI)
                counterBlack,subTotal = self._checkFourInARowDot(self._board[x+2][y],blackDot,counterBlack,subTotal,isAI)
                counterBlack,subTotal = self._checkFourInARowDot(self._board[x+3][y],blackDot,counterBlack,subTotal,isAI)

                window = [self._board[x][y], self._board[x+1][y], self._board[x+2][y], self._board[x+3][y]]
                subTotal += self._score_window(window, whiteDot, ['RED', 'WHITE'])
                subTotal += self._score_window(window, blackDot, ['RED', 'WHITE'])
        return subTotal
    def _verticalInARowDots(self,whiteDot,blackDot,isAI):
        subTotal=0
        for y in range(0,9):
            for x in range(1,9):
                counterWhite=0
                counterBlack=0

                counterWhite,subTotal = self._checkFourInARowDot(self._board[x][y],whiteDot,counterWhite,subTotal,isAI)
                counterWhite,subTotal = self._checkFourInARowDot(self._board[x][y+1],whiteDot,counterWhite,subTotal,isAI)
                counterWhite,subTotal = self._checkFourInARowDot(self._board[x][y+2],whiteDot,counterWhite,subTotal,isAI)
                counterWhite,subTotal = self._checkFourInARowDot(self._board[x][y+3],whiteDot,counterWhite,subTotal,isAI)

                counterBlack,subTotal = self._checkFourInARowDot(self._board[x][y],blackDot,counterBlack,subTotal,isAI)
                counterBlack,subTotal = self._checkFourInARowDot(self._board[x][y+1],blackDot,counterBlack,subTotal,isAI)
                counterBlack,subTotal = self._checkFourInARowDot(self._board[x][y+2],blackDot,counterBlack,subTotal,isAI)
                counterBlack,subTotal = self._checkFourInARowDot(self._board[x][y+3],blackDot,counterBlack,subTotal,isAI)

                window = [self._board[x][y], self._board[x][y+1], self._board[x][y+2], self._board[x][y+3]]
                subTotal += self._score_window(window, whiteDot, ['RED', 'WHITE'])
                subTotal += self._score_window(window, blackDot, ['RED', 'WHITE'])

        return subTotal

    def _firstDiagonalInARowDots(self,whiteDot,blackDot,isAI):
        subTotal=0
        for y in range(9):
            for x in range(1,6):
                counterWhite=0
                counterBlack=0

                counterWhite,subTotal = self._checkFourInARowDot(self._board[x][y],whiteDot,counterWhite,subTotal,isAI)
                counterWhite,subTotal = self._checkFourInARowDot(self._board[x+1][y+1],whiteDot,counterWhite,subTotal,isAI)
                counterWhite,subTotal = self._checkFourInARowDot(self._board[x+2][y+2],whiteDot,counterWhite,subTotal,isAI)
                counterWhite,subTotal = self._checkFourInARowDot(self._board[x+3][y+3],whiteDot,counterWhite,subTotal,isAI)

                counterBlack,subTotal = self._checkFourInARowDot(self._board[x][y],blackDot,counterBlack,subTotal,isAI)
                counterBlack,subTotal = self._checkFourInARowDot(self._board[x+1][y+1],blackDot,counterBlack,subTotal,isAI)
                counterBlack,subTotal = self._checkFourInARowDot(self._board[x+2][y+2],blackDot,counterBlack,subTotal,isAI)
                counterBlack,subTotal = self._checkFourInARowDot(self._board[x+3][y+3],blackDot,counterBlack,subTotal,isAI)

                window = [self._board[x][y], self._board[x+1][y+1], self._board[x+2][y+2], self._board[x+3][y+3]]
                subTotal += self._score_window(window, whiteDot, ['RED', 'WHITE'])
                subTotal += self._score_window(window, blackDot, ['RED', 'WHITE'])
                
        return subTotal
    def _secondDiagonalInARowDots(self,whiteDot,blackDot,isAI):
        subTotal=0
        for y in range(3,12):
            for x in range(1,6):
                counterWhite=0
                counterBlack=0

                counterWhite,subTotal = self._checkFourInARowDot(self._board[x][y],whiteDot,counterWhite,subTotal,isAI)
                counterWhite,subTotal = self._checkFourInARowDot(self._board[x+1][y-1],whiteDot,counterWhite,subTotal,isAI)
                counterWhite,subTotal = self._checkFourInARowDot(self._board[x+2][y-2],whiteDot,counterWhite,subTotal,isAI)
                counterWhite,subTotal = self._checkFourInARowDot(self._board[x+3][y-3],whiteDot,counterWhite,subTotal,isAI)

                counterBlack,subTotal = self._checkFourInARowDot(self._board[x][y],blackDot,counterBlack,subTotal,isAI)
                counterBlack,subTotal = self._checkFourInARowDot(self._board[x+1][y-1],blackDot,counterBlack,subTotal,isAI)
                counterBlack,subTotal = self._checkFourInARowDot(self._board[x+2][y-2],blackDot,counterBlack,subTotal,isAI)
                counterBlack,subTotal = self._checkFourInARowDot(self._board[x+3][y-3],blackDot,counterBlack,subTotal,isAI)
                
                window = [self._board[x][y], self._board[x+1][y-1], self._board[x+2][y-2], self._board[x+3][y-3]]
                subTotal += self._score_window(window, whiteDot, ['RED', 'WHITE'])
                subTotal += self._score_window(window, blackDot, ['RED', 'WHITE'])

        return subTotal
    
    def _checkFourInARowDot(self,element,dotType,counter,subTotal,isAI):
        if element is None :
            counter = 0
            subTotal = subTotal + 5 
            return counter,subTotal
        if element.getSymbol() == dotType :
            counter,subTotal = self._howManyInARow(counter,subTotal,isAI)
            return counter,subTotal
        counter = 0
        if isAI :
            subTotal = subTotal - 100
        else :
            subTotal = subTotal -5
        return counter,subTotal



    def _horizontalInARowColors(self,whiteColor,redColor,isAI):
        subTotal=0
        for y in range(0,12):
            for x in range(1,6):
                counterWhite=0
                counterRed=0

                counterWhite,subTotal = self._checkFourInARowColors(self._board[x][y],whiteColor,counterWhite,subTotal,isAI)
                counterWhite,subTotal = self._checkFourInARowColors(self._board[x+1][y],whiteColor,counterWhite,subTotal,isAI)
                counterWhite,subTotal = self._checkFourInARowColors(self._board[x+2][y],whiteColor,counterWhite,subTotal,isAI)
                counterWhite,subTotal = self._checkFourInARowColors(self._board[x+3][y],whiteColor,counterWhite,subTotal,isAI)

                counterRed,subTotal = self._checkFourInARowColors(self._board[x][y],redColor,counterRed,subTotal,isAI)
                counterRed,subTotal = self._checkFourInARowColors(self._board[x+1][y],redColor,counterRed,subTotal,isAI)
                counterRed,subTotal = self._checkFourInARowColors(self._board[x+2][y],redColor,counterRed,subTotal,isAI)
                counterRed,subTotal = self._checkFourInARowColors(self._board[x+3][y],redColor,counterRed,subTotal,isAI)
                
                window = [self._board[x][y], self._board[x+1][y], self._board[x+2][y], self._board[x+3][y]]
                subTotal += self._score_window(window, whiteColor, ['BDOT', 'WDOT'])
                subTotal += self._score_window(window, redColor, ['BDOT', 'WDOT'])

        return subTotal
    def _verticalInARowColors(self,whiteColor,redColor,isAI):
        subTotal=0
        for y in range(0,9):
            for x in range(1,9):
                counterWhite=0
                counterRed=0

                counterWhite,subTotal = self._checkFourInARowColors(self._board[x][y],whiteColor,counterWhite,subTotal,isAI)
                counterWhite,subTotal = self._checkFourInARowColors(self._board[x][y+1],whiteColor,counterWhite,subTotal,isAI)
                counterWhite,subTotal = self._checkFourInARowColors(self._board[x][y+2],whiteColor,counterWhite,subTotal,isAI)
                counterWhite,subTotal = self._checkFourInARowColors(self._board[x][y+3],whiteColor,counterWhite,subTotal,isAI)

                counterRed,subTotal = self._checkFourInARowColors(self._board[x][y],whiteColor,counterRed,subTotal,isAI)
                counterRed,subTotal = self._checkFourInARowColors(self._board[x][y+1],whiteColor,counterRed,subTotal,isAI)
                counterRed,subTotal = self._checkFourInARowColors(self._board[x][y+2],whiteColor,counterRed,subTotal,isAI)
                counterRed,subTotal = self._checkFourInARowColors(self._board[x][y+3],whiteColor,counterRed,subTotal,isAI)

                window = [self._board[x][y], self._board[x][y+1], self._board[x][y+2], self._board[x][y+3]]
                subTotal += self._score_window(window, whiteColor, ['BDOT', 'WDOT'])
                subTotal += self._score_window(window, redColor, ['BDOT', 'WDOT'])
        return subTotal

    def _firstDiagonalInARowColors(self,whiteColor,redColor,isAI):
        subTotal=0
        for y in range(9):
            for x in range(1,6):
                counterWhite=0
                counterRed=0

                counterWhite,subTotal = self._checkFourInARowColors(self._board[x][y],whiteColor,counterWhite,subTotal,isAI)
                counterWhite,subTotal = self._checkFourInARowColors(self._board[x+1][y+1],whiteColor,counterWhite,subTotal,isAI)
                counterWhite,subTotal = self._checkFourInARowColors(self._board[x+2][y+2],whiteColor,counterWhite,subTotal,isAI)
                counterWhite,subTotal = self._checkFourInARowColors(self._board[x+3][y+3],whiteColor,counterWhite,subTotal,isAI)

                counterRed,subTotal = self._checkFourInARowColors(self._board[x][y],redColor,counterRed,subTotal,isAI)
                counterRed,subTotal = self._checkFourInARowColors(self._board[x+1][y+1],redColor,counterRed,subTotal,isAI)
                counterRed,subTotal = self._checkFourInARowColors(self._board[x+2][y+2],redColor,counterRed,subTotal,isAI)
                counterRed,subTotal = self._checkFourInARowColors(self._board[x+3][y+3],redColor,counterRed,subTotal,isAI)

                window = [self._board[x][y], self._board[x+1][y+1], self._board[x+2][y+2], self._board[x+3][y+3]]
                subTotal += self._score_window(window, whiteColor, ['BDOT', 'WDOT'])
                subTotal += self._score_window(window, redColor, ['BDOT', 'WDOT'])
        return subTotal
    def _secondDiagonalInARowColors(self,whiteColor,redColor,isAI):
        subTotal=0
        for y in range(3,12):
            for x in range(1,6):
                counterWhite=0
                counterRed=0

                counterWhite,subTotal = self._checkFourInARowColors(self._board[x][y],whiteColor,counterWhite,subTotal,isAI)
                counterWhite,subTotal = self._checkFourInARowColors(self._board[x+1][y-1],whiteColor,counterWhite,subTotal,isAI)
                counterWhite,subTotal = self._checkFourInARowColors(self._board[x+2][y-2],whiteColor,counterWhite,subTotal,isAI)
                counterWhite,subTotal = self._checkFourInARowColors(self._board[x+3][y-3],whiteColor,counterWhite,subTotal,isAI)

                counterRed,subTotal = self._checkFourInARowColors(self._board[x][y],redColor,counterRed,subTotal,isAI)
                counterRed,subTotal = self._checkFourInARowColors(self._board[x+1][y-1],redColor,counterRed,subTotal,isAI)
                counterRed,subTotal = self._checkFourInARowColors(self._board[x+2][y-2],redColor,counterRed,subTotal,isAI)
                counterRed,subTotal = self._checkFourInARowColors(self._board[x+3][y-3],redColor,counterRed,subTotal,isAI)

                window = [self._board[x][y], self._board[x+1][y-1], self._board[x+2][y-2], self._board[x+3][y-3]]
                subTotal += self._score_window(window, whiteColor, ['BDOT', 'WDOT'])
                subTotal += self._score_window(window, redColor, ['BDOT', 'WDOT'])
        return subTotal
    
    def _checkFourInARowColors(self,element,colors,counter,subTotal,isAI):
        if element is None :
            counter = 0
            subTotal = subTotal + 5 
            return counter,subTotal
        if element.getColor() == colors :
            counter,subTotal = self._howManyInARow(counter,subTotal,isAI)
            return counter,subTotal
        counter = 0
        if isAI :
            subTotal = subTotal - 100
        else :
            subTotal = subTotal - 5
        return counter,subTotal

    def _howManyInARow(self,counter,subTotal,isAI):
        if counter == 0:
            counter = counter + 1
            subTotal = subTotal +10
            return counter,subTotal
        elif counter == 1:
            counter = counter + 1
            if not isAI:
                subTotal = subTotal +70
            else:
                subTotal = subTotal +40
            return counter,subTotal
        elif counter == 2:
            counter = counter + 1
            if not isAI:
                subTotal = subTotal +10000
            else:
                subTotal = subTotal +200
            return counter,subTotal
        elif counter == 3:
            counter = counter + 1
            subTotal = subTotal +1000000
            return counter,subTotal
        elif counter == 4: 
            subTotal += 1000000
            return counter,subTotal

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
        # print("PROF HEURISTIC")
        # print(countWhiteO + countWhiteX - countRedX - countRedO)
        # print(a)
        # print(b)
        # print(c)
        # print(d)

        return countWhiteO + countWhiteX - countRedX - countRedO


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

    def _findTopMostFilledCell(self, col):
        return 12 - self._findLowestOpenCell(col) + 1

    def _getRecyclableCards(self):
        recyclable = []
        for col in range(1,9):
            topmostFilledCellInColumn = self._findTopMostFilledCell(col)
            segment = self._board[col][topmostFilledCellInColumn]

            if (isinstance(segment, Card.CardSegment) 
                and (self._canRecycleCard(segment=segment) or self._canRecycleCard(segment=segment.getSibling()))
                and segment.getSibling() not in recyclable 
                and segment not in self._lastCardPlayed.getSegments()):
                    recyclable.append(segment)

        return recyclable

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

    def __hash__(self):
        h = 0
        for col in range(1, 9):
            for row in range(1, 13):
                h ^= hash(self._board[col][row])

        return h

    
if __name__ == '__main__':
    b = Board(6)
    c1 = Card(4, ['A', '1'])
    c2 = Card(5, ['C', '1'])
    c3 = Card(3, ['E', '1'])
    c5 = Card(2, ['B', '1'])
    c6 = Card(5, ['D', '2'])
    c7 = Card(6, ['E', '3'])

    b.addCard(c1)
    b.addCard(c2)
    b.addCard(c3)
    b.addCard(c5)
    b.addCard(c6)
    b.addCard(c7)

    b.printBoard()

    print('Open horizontal positions: ', b._getAvailableCellsHorizontalCard())
    print('Open vertical positions: ', b._getAvailableCellsVerticalCard())
    recyclable = b._getRecyclableCards()
    print(recyclable)
    for r in recyclable:
        print(r)
