# Generated with ChatGPT - Modified by me
import tkinter as tk
from tkinter import ttk

class ConfigWindow:
    def __init__(self, root):
        self.root = root
        root.title("Take Time - Setup")
        root.minsize(270, 290)

        # Variables
        self.num_players = tk.IntVar(value=3)
        self.name_players = tk.BooleanVar(value=False)
        self.player_names = []
        self.preset = tk.StringVar(value="1")
        self.strategy = tk.StringVar(value="1")
        self.num_rounds = tk.IntVar(value=1000)

        # Top: number of players
        frame_players = ttk.LabelFrame(root, text="Players")
        frame_players.pack(fill="x", padx=10, pady=10)

        ttk.Label(frame_players, text="Number of Players:").grid(row=0, column=0, sticky="w")
        ttk.Spinbox(frame_players, from_=2, to=6, textvariable=self.num_players,
                    width=5, command=self.refresh_names).grid(row=0, column=1)

        # Checkbox: naming players or not
        ttk.Checkbutton(frame_players, text="Name players",
                        variable=self.name_players,
                        command=self.refresh_names).grid(row=1, column=0, columnspan=2, sticky="w")

        # Dynamic area for player name fields
        self.names_frame = ttk.Frame(frame_players)
        self.names_frame.grid(row=2, column=0, columnspan=2, sticky="w")

        # Presets
        frame_preset = ttk.LabelFrame(root, text="Preset")
        frame_preset.pack(fill="x", padx=10, pady=5)
        ttk.Label(frame_preset, text="Select preset:").pack(side="left", padx=5)
        ttk.Combobox(frame_preset, textvariable=self.preset, values=["1"],
                     state="readonly", width=10).pack(side="left")

        # Strategies
        frame_strategy = ttk.LabelFrame(root, text="Strategy")
        frame_strategy.pack(fill="x", padx=10, pady=5)
        ttk.Label(frame_strategy, text="Select strategy:").pack(side="left", padx=5)
        ttk.Combobox(frame_strategy, textvariable=self.strategy, values=["1", "2"],
                     state="readonly", width=10).pack(side="left")
        
        # Number of rounds
        frame_rounds = ttk.LabelFrame(root, text="Rounds")
        frame_rounds.pack(fill="x", padx=10, pady=10)

        ttk.Label(frame_rounds, text="Number of Rounds :").grid(row=0, column=0, sticky="w")
        ttk.Spinbox(frame_rounds, from_=1, to=2000, textvariable=self.num_rounds,
                    width=5).grid(row=0, column=1)

        # Start button
        ttk.Button(root, text="Start Game", command=self.start_game).pack(pady=10)

        self.refresh_names()

    def refresh_names(self):
        """
        Refresh the names of the player, remove the empty space if turned off
        """
        # Clear existing fields
        for widget in self.names_frame.winfo_children():
            widget.destroy()

        self.player_names = []

        if self.name_players.get():
            self.names_frame.grid()
            for i in range(self.num_players.get()):
                var = tk.StringVar(value=f"Player {i+1}")
                self.player_names.append(var)
                ttk.Label(self.names_frame, text=f"Player {i+1}:").grid(row=i, column=0, sticky="w")
                ttk.Entry(self.names_frame, textvariable=var, width=15).grid(row=i, column=1)

        else :
            self.names_frame.grid_remove()

    def start_game(self):
        """
        Save all the selected infos and destroy the window
        """
        # Collect final config
        self.config = {
            "num_players": self.num_players.get(),
            "use_names": self.name_players.get(),
            "players": [v.get() for v in self.player_names] if self.name_players.get() else None,
            "preset": self.preset.get(),
            "strategy": self.strategy.get(),
            "num_rounds": self.num_rounds.get()
        }
        self.root.quit()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ConfigWindow(root)
    root.mainloop()
