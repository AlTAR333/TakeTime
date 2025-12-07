from assets.board import Board
from assets.deck import Deck
from assets.location import Location
from assets.hand import Hand
import math

class Game():
    def __init__(self):
        pass

    def dealHands(self) -> None:
        self.hands = {player : Hand() for player in self.playersNames}
        player_pointer = 0
        for _ in range(12):
            # Draw card and add it to player's hand
            card = self.deck.draw()
            playerName = self.playersNames[player_pointer]
            self.hands[playerName].addCard(card)

            # Go to the next player
            player_pointer += 1
            if player_pointer == len(self.playersNames):
                player_pointer = 0

    def printHands(self) -> None:
        print("HANDS")
        for player, hand in self.hands.items():
            print(f"{player} : {hand}")

    def printBoard(self) -> None:
        print("BOARD")
        print(f"{self.board}")

    def changeCurrentPlayer(self) -> None:
        self.playerPointer += 1
        if self.playerPointer == len(self.playersNames):
            self.playerPointer = 0
        self.currentPlayer = self.playersNames[self.playerPointer]

    def presets(self, preset:int = 1) -> None:
        """
        Basic game, 24 max per location
        """
        if preset == "1":
            self.deck = Deck(shuffled = True)
            self.board = Board()
        else :
            raise "Preset not found"

    def strategies(self, strategy, turn):
        # First strategy
        if strategy == "1":
            if turn == 0: # Player with the highest card has to start
                max = 0
                for player, hand in self.hands.items():
                    handMax = hand.getMax()
                    if handMax > max :
                        max = handMax
                        self.currentPlayer = player
                self.playerPointer = self.playersNames.index(self.currentPlayer)
            card = self.hands[self.currentPlayer].removeCard("highest") # Player plays his highest card
            value = card[1]
            self.board.addCardtoPos(math.ceil(value/2), card)
        else :
            raise "Strategy not found"

    def main(self) -> None:
        # Players
        self.players = int(input("Number of player : "))
        self.playerConfig = input("Do you want to name the players (Y/N) : ")
        if self.playerConfig == "Y":
            self.playersNames = []
            for i in range(1, self.players+1):
                playerName = input(f"Player {i} : ")
                self.playersNames.append(playerName)
        else :
            self.playersNames = [str(i) for i in range(1, self.players+1)]
        

        # Preset load
        self.preset = input("What preset do you want to load : ")
        self.presets(self.preset)
        
        self.strategy = input("What strategy do you want to use : ")
        
        # Start Game
        win = 0
        for round in range(3):
            self.dealHands()
            print("=============================")
            for turn in range(12):
                print("----------")
                self.printHands()
                self.printBoard()
                self.strategies(self.strategy, turn)
                print(f"Next player : {self.currentPlayer}")
                self.changeCurrentPlayer()
            print("-----FINAL-----")
            self.printHands()
            self.printBoard()
            if self.board.win():
                win += 1
            self.deck.create()
            self.deck.shuffle()
            self.board.clear()
            for hand in self.hands.values():
                hand.clear()


    

game = Game()
game.main()
