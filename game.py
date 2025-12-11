from assets.board import Board
from assets.deck import Deck
from assets.location import Location
from assets.hand import Hand
from GUI.configwindow import ConfigWindow
from GUI.simulationwindow import SimulationWindow
import tkinter as tk
import math
import os
import re
import random
from datetime import datetime

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

    def presets(self, preset:str = 1) -> None:
        """
        Create the instances of Deck and Board depending on the chosen preset

        :param preset: String representing the chosen preset
        """
        if preset == "1":
            self.deck = Deck(shuffled = True)
            self.board = Board()
        else :
            raise f"Preset not found : {self.preset}"

    def strategies(self, strategy:str, turn:int) -> None:
        """
        Play a turn depending on the chosen strategy
        
        :param strategy: String representing the chosen strategy
        :param turn: Integer representing the current turn(0-12)
        """
        # First strategy
        if strategy == "1":
            if turn == 0: # Player with the highest card has to start
                max_value = 0
                for player, hand in self.hands.items():
                    handMax = hand.getMax()[1]
                    if handMax > max_value :
                        max_value = handMax
                        self.currentPlayer = player
                self.playerPointer = self.playersNames.index(self.currentPlayer)

            # Player plays his highest card
            card = self.hands[self.currentPlayer].removeCard("highest") 
            value = card[1]

            # Place card on the correct location
            base_location = math.ceil(value / 2)
            is_high_card = (value % 2 == 0)
            direction = 1 if is_high_card else -1  # +1 = clockwise, -1 = counter-clockwise
            location = base_location
            for _ in range(self.board.time*2):
                if self.board.times[location].size < 2:
                    self.board.addCardtoPos(location, card)
                    break
                next_location = location + direction
                # if next would go out of bounds, reverse direction
                if not (1 <= next_location <= self.board.time):
                    direction = -direction
                    next_location = location + direction
                location = next_location

        # Second Strategy, same as first but play random card instead of highest
        elif strategy == "2":
            if turn == 0: # Random player starts
                self.playerPointer = random.randint(0, self.players-1)
                self.currentPlayer = self.playersNames[self.playerPointer]

            # Player plays his highest card
            card = self.hands[self.currentPlayer].removeCard("random") 
            value = card[1]

            # Place card on the correct location
            base_location = math.ceil(value / 2)
            is_high_card = (value % 2 == 0)
            direction = 1 if is_high_card else -1  # +1 = clockwise, -1 = counter-clockwise
            location = base_location
            for _ in range(self.board.time*2):
                if self.board.times[location].size < 2:
                    self.board.addCardtoPos(location, card)
                    break
                next_location = location + direction
                # if next would go out of bounds, reverse direction
                if not (1 <= next_location <= self.board.time):
                    direction = -direction
                    next_location = location + direction
                location = next_location

        # Third Strategy
        elif strategy == "3":
            if turn == 0: # Random player starts
                self.playerPointer = random.randint(0, self.players-1)
                self.currentPlayer = self.playersNames[self.playerPointer]

            # Player plays his highest card
            card = self.hands[self.currentPlayer].removeCard("random") 
            value = card[1]

            # Place card on the correct location
            base_location = math.ceil(value / 2)
            is_high_card = (value % 2 == 0)
            direction = 1 if is_high_card else -1  # +1 = clockwise, -1 = counter-clockwise
            location = base_location
            for _ in range(self.board.time*2):
                if self.board.times[location].size < 2:
                    self.board.addCardtoPos(location, card)
                    break
                next_location = location + direction
                # if next would go out of bounds, reverse direction
                if not (1 <= next_location <= self.board.time):
                    direction = -direction
                    next_location = location + direction
                location = next_location

        else :
            raise f"Strategy not found : {self.strategy}"

    def saveGame(self, won:bool, round:int = None) -> None:
        """
        Write the final state of a game onto the results file

        :param state: string representing wether the game was won or lost
        :param round: integer representing the number of the round
        """
        if round :
            round += 1
        else :
            round = "?"
        if won:
            state = "Won"
        else :
            state = "Lost"
        with open(self.results_filename, "a", encoding="utf-8") as f:
            f.write(f"-----ROUND {round}-----\n")
            f.write("HANDS\n")
            for player, hand in self.hands.items():
                f.write(f"{player} : {hand}\n")
            f.write("BOARD\n")
            f.write(f"{self.board}")
            f.write(f"STATUS\n")
            f.write(f"{state}\n\n")

    def saveSummary(self, win:int) -> None:
        """
        Write the chosen preset, strategy, and number of wins onto the results file

        :param win: integer representing the number of win
        """
        with open(self.results_filename, "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now()}]\n")
            f.write(f"Chosen preset : {self.preset}\n")
            f.write(f"Strategy used : {self.strategy}\n")
            f.write(f"Total round won : {win}/{self.num_round}\n")
            f.write(f"Success rate : {round(win/self.num_round * 100, 2)}%")

    def getResultsFilename(self) -> str:
        """
        Auto-increment results filename and return new one - ChatGPT
        """
        existing_files = [f for f in os.listdir("tests results/") if re.match(r"results\d+\.txt$", f)]
        if existing_files:
            # Extract numbers and find max
            numbers = [int(re.findall(r"results(\d+)\.txt", f)[0]) for f in existing_files]
            next_num = max(numbers) + 1
        else:
            next_num = 1
        return f"tests results/results{next_num}.txt"

    def clearGame(self) -> None:
        """
        Reset the deck and clears the board and the hands.
        """
        self.deck.create()
        self.deck.shuffle()
        self.board.clear()
        for hand in self.hands.values():
            hand.clear()

    def runOneRound(self, display=False) -> bool:
        """
        Simulate a round of the game with the current preset and strategy.
        Returns True if the game was won, else False

        :param display: Boolean, if True, prints the game situation at each turn
        """
        self.dealHands()
        if display :
            print("=============================")
        for turn in range(12):
            if display :
                print("----------")
                self.printHands()
                self.printBoard()
            self.strategies(self.strategy, turn)
            if display :
                print(f"Next player : {self.currentPlayer}")
            self.changeCurrentPlayer()
        if display :
            print("-----FINAL-----")
            self.printHands()
            self.printBoard()

        return self.board.checkConditions()

    def main(self) -> None:
        win = 0
        for round in range(self.num_round):
            gameState = self.runOneRound(display=True)
            if gameState:
                win += 1
            self.saveGame(won=gameState, round=round)
            self.clearGame()
            
        print(f"Total round won : {win}")
        self.saveSummary(win)



if __name__ == "__main__":
    root = tk.Tk()
    config_window = ConfigWindow(root)
    root.mainloop()

    # collect the settings
    config = config_window.config

    game = Game()
    game.players = config["num_players"]
    game.playersNames = config["players"] if config["players"] else [
        f"P{i}" for i in range(1, config["num_players"]+1)
    ]
    game.preset = config["preset"]
    game.strategy = config["strategy"]
    game.num_round = config["num_rounds"]
    game.results_filename = game.getResultsFilename()

    game.presets(game.preset)
    # game.main()

    # --- GUI Simulation ---
    def run_one_round_callback():
        result = game.runOneRound(display=True)
        game.saveGame(won=result)
        game.clearGame()
        return result

    SimulationWindow(config, run_one_round_callback, game)

