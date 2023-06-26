import tkinter as tk
from tkinter import messagebox
from random import randint

class YahtzeeGame:
    def __init__(self, players):
        self.roll_count = 0
        self.dice = [0] * 5
        self.hold = [False] * 5
        self.scores = {player: {} for player in players}
        self.current_player = players[0]
        self.players = players
        self.categories = ["Ones", "Twos", "Threes", "Fours", "Fives", "Sixes", "3 of a Kind", "4 of a Kind", "Full House", "Small Straight", "Large Straight", "Yahtzee!", "Chance"]
        self.total_score = {}


    def roll_dice(self):
        if self.roll_count < 3:
            for i in range(5):
                if not self.hold[i]:
                    self.dice[i] = randint(1, 6)
            self.roll_count += 1

    def toggle_hold(self, index):
        self.hold[index] = not self.hold[index]

    def reset_dice(self):
        self.roll_count = 0
        self.dice = [0] * 5
        self.hold = [False] * 5

    def reset_game(self):
        self.reset_dice()
        self.scores = {player: {} for player in self.players}
        self.current_player = self.players[0]

    def score_dice(self, category, player):
        if category in self.scores[player]:
            messagebox.showinfo("Yahtzee", "Category already scored!")
        else:
            score = self.calculate_score(category)
            self.scores[player][category] = score
            messagebox.showinfo("Yahtzee", f"{player} scored {score} points in {category}!")
            self.current_player = self.get_next_player()
            self.reset_dice()

    def get_next_player(self):
        current_index = self.players.index(self.current_player)
        next_index = (current_index + 1) % len(self.players)
        return self.players[next_index]

    def calculate_score(self, category):
        if category in self.scores[self.current_player]:
            return 0

        if category in ["Ones", "Twos", "Threes", "Fours", "Fives", "Sixes"]:
            if category == "Ones":
                return self.dice.count(1)
            elif category == "Twos":
                return self.dice.count(2) * 2
            elif category == "Threes":
                return self.dice.count(3) * 3
            elif category == "Fours":
                return self.dice.count(4) * 4
            elif category == "Fives":
                return self.dice.count(5) * 5
            elif category == "Sixes":
                return self.dice.count(6) * 6
            else:
                return 0

        sorted_dice = sorted(self.dice)

        if category == "3 of a Kind":
            for value in sorted_dice:
                if sorted_dice.count(value) >= 3:
                    return sum(sorted_dice)
            return 0

        if category == "4 of a Kind":
            for value in sorted_dice:
                if sorted_dice.count(value) >= 4:
                    return sum(sorted_dice)
            return 0

        if category == "Full House":
            if len(set(sorted_dice)) == 2 and sorted_dice.count(sorted_dice[0]) in [2, 3]:
                return 25
            return 0

        if category == "Small Straight":
            sorted_dice = sorted(set(self.dice))
            distinct_values = len(sorted_dice)
            if distinct_values >= 4:
                for i in range(distinct_values - 3):
                    sub_sequence = sorted_dice[i: i + 4]
                    if sub_sequence == list(range(sub_sequence[0], sub_sequence[-1] + 1)):
                        return 30
            return 0

        if category == "Large Straight":
            if set(sorted_dice) in [{1, 2, 3, 4, 5}, {2, 3, 4, 5, 6}]:
                return 40
            return 0

        if category == "Yahtzee!":
            if len(set(sorted_dice)) == 1:
                return 50
            return 0

        if category == "Chance":
            return sum(sorted_dice)

        return 0

    def get_winner(self):
        player_scores = {player: sum(scores.values()) for player, scores in self.scores.items()}
        max_score = max(player_scores.values())
        winners = [player for player, score in player_scores.items() if score == max_score]
        return winners[0]

    def save_game(self, filename):
        with open(filename, "a") as file:
            file.write("\n\n-----------New-Game-----------")
            file.write("Players:\n")
            for player in self.players:
                file.write(f"- {player}\n")
            file.write("\n")
            file.write("Scores:\n")
            for player, scores in self.scores.items():
                final_score = 0
                file.write(f"{player}:\n")
                for category, score in scores.items():
                    final_score = final_score + score
                    file.write(f"- {category}: {score}\n")
                file.write(f"Final score: {final_score}\n\n")

class YahtzeeGUI:
    def __init__(self, window, game, players):
        self.window = window
        self.window.title("Yahtzee")
        self.game = game
        self.players = players

        self.dice_labels = []
        self.total_score_labels = {}


        for i in range(5):
            label = tk.Label(window, text="-", font=("Arial", 24))
            label.grid(row=0, column=i, padx=5)
            self.dice_labels.append(label)

        self.roll_button = tk.Button(window, text="Roll Dice", font=("Arial", 14), command=self.roll_dice)
        self.roll_button.grid(row=1, columnspan=5, pady=10)

        self.hold_buttons = []
        for i in range(5):
            button = tk.Button(window, text="Hold", font=("Arial", 12), width=11, command=lambda idx=i: self.toggle_hold(idx))
            button.grid(row=2, column=i)
            self.hold_buttons.append(button)

        self.score_buttons = []
        self.score_labels = {}
        for i, player in enumerate(self.players):
            label = tk.Label(window, text=player, font=("Arial", 16))
            label.grid(row=3, column=2*i, padx=5, pady=5)
            for j, category in enumerate(self.game.categories):
                button = tk.Button(window, text=category, font=("Arial", 12), command=lambda p=player, cat=category: self.score_dice(cat, p))
                button.grid(row=4+j, column=2*i, padx=5, pady=5)
                self.score_buttons.append(button)

                score_label = tk.Label(window, text="0", font=("Arial", 12))
                score_label.grid(row=4+j, column=2*i+1, padx=5, pady=5)
                self.score_labels[(player, category)] = score_label

        self.reset_game_button = tk.Button(window, text="Reset Game", font=("Arial", 14), command=self.reset_game)
        self.reset_game_button.grid(row=4+len(self.game.categories), columnspan=5, pady=10)
        for i, player in enumerate(self.players):
            label = tk.Label(self.window, text="0", font=("Arial", 12))
            label.grid(row=5 + len(self.game.categories), column=2 * i + 1, padx=5, pady=5)
            self.total_score_labels[player] = label
        self.update_dice_labels()

        self.current_player_label = tk.Label(window, text=f"Current Player: {self.game.current_player}", font=("Arial", 12))
        self.current_player_label.grid(row=6 + len(self.game.categories), columnspan=5, pady=5)

        self.update_dice_labels()

    def update_current_player_label(self):
        self.current_player_label.config(text=f"Current Player: {self.game.current_player}")

    def update_dice_labels(self):
        for i in range(5):
            self.dice_labels[i].config(text=str(self.game.dice[i]))

    def roll_dice(self):
        self.game.roll_dice()
        self.update_dice_labels()

        if self.game.roll_count == 3:
            self.roll_button.config(state="disabled")

    def toggle_hold(self, index):
        self.game.toggle_hold(index)
        hold_text = "Hold" if not self.game.hold[index] else "Release"
        self.hold_buttons[index].config(text=hold_text)

    def reset_game(self):
        self.game.reset_game()
        self.update_dice_labels()
        self.roll_button.config(state="normal")


        for i in range(5):
            self.game.hold[i] = False
            self.hold_buttons[i].config(text="Hold")


        for button in self.score_buttons:
            button.config(state="normal")


        for (player, category), label in self.score_labels.items():
            label.config(text="0")


        self.update_total_score_labels()

    def announce_winner(self):
        max_score = 0
        winners = []

        for player, scores in self.game.scores.items():
            total_score = sum(scores.values())
            if total_score > max_score:
                max_score = total_score
                winners = [player]
            elif total_score == max_score:
                winners.append(player)

        if len(winners) == 1:
            winner = winners[0]
            message = f"{winner} wins with a score of {max_score} points!"
        else:
            message = f"It's a tie between {', '.join(winners)} with a score of {max_score} points!"

        game.save_game("game_data.txt")
        messagebox.showinfo("Yahtzee - Game Over", message)

    def score_dice(self, category, player):
        self.game.score_dice(category, player)
        for button in self.score_buttons:
            if (
                    button.cget("text") == category
                    and button.grid_info()
                    and button.grid_info()["row"] - 4 == self.game.categories.index(category)
                    and button.grid_info()["column"] // 2 == self.players.index(player)
            ):
                button.config(state="disabled")

        self.reset_dice()

        self.update_score_labels()

        self.update_total_score_labels()

        if all(len(self.game.scores[p]) == len(self.game.categories) for p in self.players):

            self.update_total_score_labels()

            winner = game.get_winner()
            messagebox.showinfo("Yahtzee", f"{winner} wins!")

            self.game.save_game("yahtzee_game_data.txt")

        self.update_total_score_labels()

        self.update_current_player_label()

    def reset_dice(self):
        self.game.roll_count = 0
        self.game.dice = [0] * 5
        self.update_dice_labels()
        self.roll_button.config(state="normal")
        for i in range(5):
            self.game.hold[i] = False
            self.hold_buttons[i].config(text="Hold")

    def update_score_labels(self):
        for (player, category), label in self.score_labels.items():
            if category in self.game.scores[player]:
                score = self.game.scores[player][category]
                label.config(text=str(score))
            else:
                label.config(text="0")

    def update_total_score_labels(self):
        for player in self.players:
            total_score = sum(self.game.scores[player].values())
            self.total_score_labels[player].config(text=str(total_score))


players = ["Player 1", "Player 2"]
game = YahtzeeGame(players)
window = tk.Tk()
yahtzee_gui = YahtzeeGUI(window, game, players)
window.mainloop()
