# Generated with ChatGPT - Modified by me
import tkinter as tk
from tkinter import ttk
import threading
import time

def center_window(window, width, height):
    window.update_idletasks()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")

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
        center_window(self.root, 400, 200)
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
            if self.simulate_callback():
                wins += 1

            progress_value = int((i + 1) / total * 100)
            self.root.after(0, self.update_progress, progress_value)

        self.game.saveSummary(wins)
        win_rate = wins / total * 100

        # Close the simulation window and open results
        self.root.after(0, self.show_results_and_close, wins, total, win_rate)

    def update_progress(self, percent):
        self.progress["value"] = percent
        self.label_status.config(text=f"{percent}%")

    def show_results_and_close(self, wins, total, win_rate):
        # Close the old window
        self.root.destroy()

        # Open the results window
        results = tk.Tk()
        center_window(results, 300, 200)
        results.title("Simulation Results")
        results.geometry("300x200")

        ttk.Label(results, text="Simulation Results", font=("Arial", 14)).pack(pady=10)
        ttk.Label(results, text=f"Total rounds: {total}").pack(pady=5)
        ttk.Label(results, text=f"Wins: {wins}").pack(pady=5)
        ttk.Label(results, text=f"Win rate: {win_rate:.2f}%").pack(pady=5)

        ttk.Button(results, text="Close", command=results.destroy).pack(pady=15)

        results.mainloop()
