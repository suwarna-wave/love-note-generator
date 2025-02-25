import tkinter as tk
from tkinter import ttk, messagebox
import random
import pygame
import json
import os

class LoveNoteRandomizer:
    def __init__(self, root):
        # Initialize pygame for sound
        pygame.mixer.init()
        self.root = root
        self.root.title("Love Note Randomizer: Ultimate Cheeky Adventure")
        self.root.geometry("600x800")
        self.root.configure(bg="#ff99cc")  # Hot pink background

        # Data
        self.notes = {
            "Romantic": ["You’re my galaxy’s brightest star!", "I’d fight dragons for your kiss.", "Every heartbeat sings your name."],
            "Cheeky": ["You’re so hot, you crashed my heart’s server!", "Caught you stealing my breath again.", "You’re my VIP, babe!"],
            "Wild": ["Let’s run away and kiss under every sunset!", "You’re my backstage pass to love.", "Our love’s a rollercoaster—buckle up!"]
        }
        self.dares = ["Wink at me right now!", "Sing me a silly love song!", "Text me 'You’re my hero' and prove it!"]
        self.love_meter = 50  # Starting love meter
        self.player_notes = {"Player1": [], "Player2": []}  # Two-player custom notes
        self.current_player = "Player1"
        self.load_player_notes()

        # UI Setup with Canvas
        self.canvas = tk.Canvas(self.root, bg="#ff99cc", width=600, height=800, highlightthickness=0)
        self.canvas.pack()

        # Title
        self.canvas.create_text(300, 50, text="💖 Love Note Adventure 💖", font=("Comic Sans MS", 28, "bold"), fill="#ff0066")

        # Mood Selector
        self.mood_var = tk.StringVar(value="Cheeky")
        mood_menu = ttk.Combobox(self.root, textvariable=self.mood_var, values=list(self.notes.keys()), width=15)
        self.canvas.create_window(300, 120, window=mood_menu)

        # Spin Button
        self.spin_btn = tk.Button(self.root, text="✨ SPIN THE LOVE! ✨", command=self.spin_note, 
                                 bg="#ff0066", fg="white", font=("Arial", 16, "bold"), relief="raised")
        self.canvas.create_window(300, 180, window=self.spin_btn)

        # Dare Button
        self.dare_btn = tk.Button(self.root, text="🎉 LOVE DARE! 🎉", command=self.love_dare, 
                                 bg="#ffcc00", fg="black", font=("Arial", 16, "bold"), relief="raised")
        self.canvas.create_window(300, 250, window=self.dare_btn)

        # Player Switch
        self.player_var = tk.StringVar(value="Player1")
        player_menu = ttk.Combobox(self.root, textvariable=self.player_var, values=["Player1", "Player2"], width=15)
        self.canvas.create_window(300, 320, window=player_menu)
        self.switch_btn = tk.Button(self.root, text="Switch Player", command=self.switch_player, 
                                   bg="#66ccff", fg="white", font=("Arial", 12))
        self.canvas.create_window(300, 360, window=self.switch_btn)

        # Custom Note Input
        self.custom_entry = tk.Entry(self.root, width=40)
        self.canvas.create_window(300, 420, window=self.custom_entry)
        self.add_note_btn = tk.Button(self.root, text="Leave a Note!", command=self.add_player_note, 
                                     bg="#66ff66", fg="black", font=("Arial", 12))
        self.canvas.create_window(300, 460, window=self.add_note_btn)

        # Note Display
        self.note_text = self.canvas.create_text(300, 550, text="Spin for some love magic!", 
                                                font=("Arial", 18), fill="#ffffff", width=500)

        # Love Meter
        self.meter_text = self.canvas.create_text(300, 700, text=f"Love Meter: {self.love_meter}%", 
                                                 font=("Arial", 14), fill="#ff0066")
        self.hearts = []  # For animations

    def spin_note(self):
        mood = self.mood_var.get()
        other_player = "Player2" if self.current_player == "Player1" else "Player1"
        all_notes = self.notes[mood] + self.player_notes[other_player]
        note = random.choice(all_notes) if all_notes else "No notes yet—leave one, hotshot!"
        
        # Spinning animation
        for i in range(10):
            self.canvas.itemconfig(self.note_text, text=f"Spinning... {i+1}")
            self.root.update()
            self.root.after(100)
        
        self.canvas.itemconfig(self.note_text, text=note)
        self.animate_hearts()
        
        # Sound (you’ll need a "kiss.wav" file in the same directory)
        try:
            pygame.mixer.Sound("kiss.wav").play()
        except:
            print("Sound file 'kiss.wav' not found—add one for extra fun!")
        
        self.pop_surprise()
        
        # Random Love Meter boost
        if random.random() < 0.2:  # 20% chance for a "jackpot"
            self.love_meter = min(100, self.love_meter + 15)
            messagebox.showinfo("JACKPOT!", "Love Jackpot! Meter boosted!")
            self.animate_jackpot()
        self.update_meter()

    def animate_hearts(self):
        self.canvas.delete("heart")
        for _ in range(5):
            x, y = random.randint(200, 400), 700
            heart = self.canvas.create_text(x, y, text="💕", font=("Arial", 20), fill="#ff0066", tags="heart")
            self.hearts.append(heart)
        for i in range(20):
            for heart in self.hearts:
                self.canvas.move(heart, random.randint(-5, 5), -10)
            self.root.update()
            self.root.after(50)
        self.canvas.delete("heart")

    def animate_jackpot(self):
        # Extra confetti for jackpot
        for _ in range(10):
            x, y = random.randint(100, 500), random.randint(100, 700)
            confetti = self.canvas.create_text(x, y, text="✨", font=("Arial", 20), fill="#ffff00", tags="confetti")
            self.root.after(500, lambda: self.canvas.delete(confetti))

    def pop_surprise(self):
        surprises = ["Boom! Love bomb dropped!", "You’re blushing, I know it!", "Too hot to handle, babe!"]
        messagebox.showinfo("Love Alert!", random.choice(surprises))

    def love_dare(self):
        dare = random.choice(self.dares)
        response = messagebox.askyesno("Dare Time!", f"Dare: {dare}\nDid you do it?")
        if response:
            self.love_meter = min(100, self.love_meter + 10)
            messagebox.showinfo("Score!", "Love Meter UP! You’re a legend!")
        else:
            self.love_meter = max(0, self.love_meter - 5)
            messagebox.showinfo("Boo!", "Love Meter DOWN! Don’t chicken out next time!")
        self.update_meter()

    def switch_player(self):
        self.current_player = self.player_var.get()
        messagebox.showinfo("Switch!", f"Now it’s {self.current_player}’s turn!")
        self.canvas.itemconfig(self.note_text, text=f"{self.current_player}, your move!")

    def add_player_note(self):
        note = self.custom_entry.get().strip()
        if note:
            other_player = "Player2" if self.current_player == "Player1" else "Player1"
            self.player_notes[other_player].append(note)
            self.save_player_notes()
            self.custom_entry.delete(0, tk.END)
            messagebox.showinfo("Sent!", f"Note left for {other_player}—sneaky!")
        else:
            messagebox.showwarning("Hey!", "Don’t tease—write something flirty!")

    def update_meter(self):
        self.canvas.itemconfig(self.meter_text, text=f"Love Meter: {self.love_meter}%")
        if self.love_meter == 100:
            messagebox.showinfo("MAX LOVE!", "Love Meter maxed out! You’re soulmate material!")

    def load_player_notes(self):
        if os.path.exists("player_notes.json"):
            with open("player_notes.json", "r") as f:
                return json.load(f)
        return {"Player1": [], "Player2": []}

    def save_player_notes(self):
        with open("player_notes.json", "w") as f:
            json.dump(self.player_notes, f)

if __name__ == "__main__":
    root = tk.Tk()
    app = LoveNoteRandomizer(root)
    root.mainloop()