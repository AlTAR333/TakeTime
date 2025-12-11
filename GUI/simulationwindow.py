# Generated with ChatGPT - Modified by me
import tkinter as tk
from tkinter import ttk
import threading
import time


class SimulationWindow:
    def __init__(self, config, simulate_callback, game):
        """
        config = user config from ConfigWindow.start_game()
        simulate_callback = function that runs ONE simulation round and returns True/False for a win
        """
        self.config = config
        self.simulate_callback = simulate_callback
        self.game = game

        self.root = tk.Tk()
        self.root.title("Running Simulation...")
        self.root.geometry("400x200")

        ttk.Label(self.root, text="Running simulation...", font=("Arial", 14)).pack(pady=10)

        # Progress bar
        self.progress = ttk.Progressbar(self.root, mode="determinate")
        self.progress.pack(fill="x", padx=20, pady=10)

        # Percentage label
        self.label_status = ttk.Label(self.root, text="0%")
        self.label_status.pack()

        # Final result label (appears after simulation)
        self.label_result = ttk.Label(self.root, text="", font=("Arial", 12))
        self.label_result.pack(pady=10)

        # Start simulation in background
        threading.Thread(target=self.run_simulation, daemon=True).start()

        self.root.mainloop()

    def run_simulation(self):
        total = self.config["num_rounds"]
        wins = 0

        for i in range(total):
            # Simulate one round
            if self.simulate_callback():
                wins += 1

            progress_value = int((i + 1) / total * 100)

            # Update UI (must use .after)
            self.root.after(0, self.update_progress, progress_value)

        # When finished
        self.game.saveSummary(wins)
        win_rate = wins / total * 100
        self.root.after(0, self.finish, wins, win_rate)

    def update_progress(self, percent):
        self.progress["value"] = percent
        self.label_status.config(text=f"{percent}%")

    def finish(self, wins, win_rate):
        self.label_result.config(text=f"Simulation completed!\nWins: {wins}\nWin rate: {win_rate:.2f}%")
        tk.Label(self.root, text="Simulation completed!", font=("Arial", 14)).pack(pady=10)
