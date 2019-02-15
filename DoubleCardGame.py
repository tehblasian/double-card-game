from Board import Board
from Player import Player

class DoubleCardGame:
    _MAX_ROUNDS = 60
    _MAX_CARDS_PER_PLAYER = 12

    def __init__(self, board, players):
        self._board = board
        self._players = players
        self._hasWinner = False

    def playGame(self):
        rounds = 0
        while not self._hasWinner:
            if not rounds < DoubleCardGame._MAX_ROUNDS:
                print('The maximum number of turns ({}) has been reached!\nThe game has ended in a draw.'.format(DoubleCardGame._MAX_ROUNDS))
                break
 
            self._playRound()
            rounds += 1

    def getPlayers(self):
        return self._players

    def _playRound(self):
        for player in self._players:
            player.takeTurn()
            self._board.printBoard()
            if self._board.hasWinner():
                self._hasWinner = True 
                player1, player2 = self._players
                winning_marker = self._board.getWinner()
                if player1.getMarker() == winning_marker:
                    print('{} has won!'.format(player1.getName()))
                else:
                    print('{} has won!'.format(player2.getName()))
            
                break

if __name__ == '__main__':
    print('Let\'s play DoubleCardGame!\n')
        
    mode = input('Select the game mode:\n\t1 - Human vs. Human\n\t2 - Human vs. AI\n')
    if int(mode) == 2:
        print('AI NOT IMPLEMEMTED')
        exit(0)
        
    player1_name = input('\nEnter player 1\'s name: ')
    player1_marker = input('\nSelect player 1\'s marker:\n1 - Dots \n2 - Color\n')
    player2_marker = None

    if int(player1_marker) == 1:
        player1_marker = Player.Marker.DOTS
        player2_marker = Player.Marker.COLOR
    elif int(player1_marker) == 2:
        player1_marker = Player.Marker.COLOR
        player2_marker = Player.Marker.DOTS
    
    player2_name = input('\nEnter player 2\'s name: \n')

    board = Board(DoubleCardGame._MAX_CARDS_PER_PLAYER * 2)
    player1 = Player(player1_name, player1_marker, board, DoubleCardGame._MAX_CARDS_PER_PLAYER)
    player2 = Player(player2_name, player2_marker, board, DoubleCardGame._MAX_CARDS_PER_PLAYER)
    
    game = DoubleCardGame(board, [player1, player2])

    game.playGame()
