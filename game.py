from assets.board import Board
from assets.deck import Deck
from assets.location import Location
from assets.hand import Hand
import math
import os
import re

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
                max_value = 0
                for player, hand in self.hands.items():
                    handMax = hand.getMax()
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

        elif strategy == "2":
            if turn == 0:
                # Player with highest card starts
                max_value = 0
                for player, hand in self.hands.items():
                    handMax = hand.getMax()
                    if handMax > max_value:
                        max_value = handMax
                        self.currentPlayer = player
                self.playerPointer = self.playersNames.index(self.currentPlayer)

            hand = self.hands[self.currentPlayer]

            # Compute ideal sums based on all remaining cards
            remaining_cards = [card for h in self.hands.values() for card in h.hand]
            total_remaining = sum(card[1] for card in remaining_cards)
            ideal_sum_per_location = total_remaining / self.board.time

            best_card = None
            best_location = None
            best_score = float("inf")

            for card in hand.hand:
                value = card[1]
                for loc_index in range(1, self.board.time + 1):
                    loc = self.board.times[loc_index]
                    if loc.size >= 2:
                        continue  # Skip full locations

                    # Simulate placement
                    temp_sums = [self.board.times[i].getSum() for i in range(1, self.board.time + 1)]
                    temp_sums[loc_index - 1] += value

                    # Score = sum of absolute differences to ideal
                    score = sum(abs(s - ideal_sum_per_location) for s in temp_sums)

                    # Penalize locations that will exceed max size
                    if loc.size + 1 > 2:
                        score += 100  # large penalty

                    if score < best_score:
                        best_score = score
                        best_card = card
                        best_location = loc_index

            # Play the best card
            hand.removeCard(best_card)
            self.board.addCardtoPos(best_location, best_card)

        else :
            raise "Strategy not found"

    def saveGame(self, state, round):
        with open(self.results_filename, "a", encoding="utf-8") as f:
            f.write(f"-----ROUND {round+1}-----\n")
            f.write("HANDS\n")
            for player, hand in self.hands.items():
                f.write(f"{player} : {hand}\n")
            f.write("BOARD\n")
            f.write(f"{self.board}")
            f.write(f"STATUS\n")
            f.write(f"{state}\n\n")

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
            self.playersNames = ["P"+str(i) for i in range(1, self.players+1)]

        # Preset and Strategy load
        self.preset = input("What preset do you want to load : ")
        self.presets(self.preset)
        self.strategy = input("What strategy do you want to use : ")
        
        # Auto-increment results filename - ChatGPT
        existing_files = [f for f in os.listdir("tests results/") if re.match(r"results\d+\.txt$", f)]
        if existing_files:
            # Extract numbers and find max
            numbers = [int(re.findall(r"tests results/results(\d+)\.txt", f)[0]) for f in existing_files]
            next_num = max(numbers) + 1
        else:
            next_num = 1

        self.results_filename = f"tests results/results{next_num}.txt"
        
        # Start Game
        win = 0
        for round in range(10):
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
            if self.board.checkConditions():
                win += 1
                state = "Won"
            else :
                state = "Lost"
            self.saveGame(state, round)
            self.deck.create()
            self.deck.shuffle()
            self.board.clear()
            for hand in self.hands.values():
                hand.clear()
        print(f"Total round won : {win}")



game = Game()
game.main()
