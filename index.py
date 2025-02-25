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
        self.root.title("Love Note Randomizer: Spicy & Sensual Edition")
        self.root.geometry("600x800")
        self.root.configure(bg="#ff99cc")  # Hot pink background

        # Expanded Notes - More Wild, Cheeky, Romantic, and Sensual
        self.notes = {
            "Romantic": [
                "You’re the fire in my soul, burning me alive.", 
                "Every kiss from you is a star lighting my night.", 
                "I’d chase you across the universe just to hold you.", 
                "Your touch is my forever addiction.", 
                "Our love drowns out the world—pure ecstasy."
            ],
            "Cheeky": [
                "You’re so hot, my heart’s filing a restraining order!", 
                "Caught you sneaking into my dirtiest dreams again.", 
                "I’d fight a lion for that smirk—worth it!", 
                "You’re my naughty little secret, aren’t you?", 
                "Stealing your kisses is my full-time gig now."
            ],
            "Wild": [
                "Let’s ditch the world and make out on a rooftop!", 
                "You’re my feral fantasy—untamed and mine.", 
                "Our love’s a wildfire—burn it all down with me!", 
                "Rip off my inhibitions and let’s run naked in the rain!", 
                "One night with you? I’d break every rule in the book."
            ],
            "Sensual": [
                "Your skin on mine is my sweetest sin.", 
                "I crave the taste of you like a forbidden fruit.", 
                "Whisper my name and watch me unravel, slow and deep.", 
                "Every curve of you is a map I’d explore all night.", 
                "Let’s tangle up and melt into the sheets together."
            ]
        }

        # Expanded Dares - Wilder, More Exciting, and Sensual
        self.dares = [
            "Bite your lip and stare at me like you mean it!", 
            "Whisper something naughty in my ear—make me blush!", 
            "Trace your fingers down my back—slowly.", 
            "Steal a kiss when I least expect it!", 
            "Dance for me like nobody’s watching—sexy vibes only!", 
            "Text me your wildest fantasy right now!", 
            "Lick your lips and wink—drive me crazy!", 
            "Press up close and breathe on my neck—tease me!", 
            "Take off one piece of clothing and smirk at me!", 
            "Tell me how you’d seduce me tonight—details, babe!"
        ]

        self.love_meter = 50  # Starting love meter
        self.player_notes = {"Player1": [], "Player2": []}  # Two-player custom notes
        self.current_player = "Player1"
        self.load_player_notes()

        # UI Setup with Canvas
        self.canvas = tk.Canvas(self.root, bg="#ff99cc", width=600, height=800, highlightthickness=0)
        self.canvas.pack()

        # Title
        self.canvas.create_text(300, 50, text="💋 Spicy Love Adventure 💋", font=("Comic Sans MS", 28, "bold"), fill="#ff0066")

        # Mood Selector
        self.mood_var = tk.StringVar(value="Sensual")
        mood_menu = ttk.Combobox(self.root, textvariable=self.mood_var, values=list(self.notes.keys()), width=15)
        self.canvas.create_window(300, 120, window=mood_menu)

        # Spin Button
        self.spin_btn = tk.Button(self.root, text="🔥 SPIN THE HEAT! 🔥", command=self.spin_note, 
                                 bg="#ff0066", fg="white", font=("Arial", 16, "bold"), relief="raised")
        self.canvas.create_window(300, 180, window=self.spin_btn)

        # Dare Button
        self.dare_btn = tk.Button(self.root, text="💦 HOT DARE! 💦", command=self.love_dare, 
                                 bg="#ffcc00", fg="black", font=("Arial", 16, "bold"), relief="raised")
        self.canvas.create_window(300, 250, window=self.dare_btn)

        # Player Switch
        self.player_var = tk.StringVar(value="Player1")
        player_menu = ttk.Combobox(self.root, textvariable=self.player_var, values=["Player1", "Player2"], width=15)
        self.canvas.create_window(300, 320, window=player_menu)
        self.switch_btn = tk.Button(self.root, text="Switch Lover", command=self.switch_player, 
                                   bg="#66ccff", fg="white", font=("Arial", 12))
        self.canvas.create_window(300, 360, window=self.switch_btn)

        # Custom Note Input
        self.custom_entry = tk.Entry(self.root, width=40)
        self.canvas.create_window(300, 420, window=self.custom_entry)
        self.add_note_btn = tk.Button(self.root, text="Drop a Sexy Note!", command=self.add_player_note, 
                                     bg="#66ff66", fg="black", font=("Arial", 12))
        self.canvas.create_window(300, 460, window=self.add_note_btn)

        # Note Display
        self.note_text = self.canvas.create_text(300, 550, text="Spin for some steamy magic!", 
                                                font=("Arial", 18), fill="#ffffff", width=500)

        # Love Meter
        self.meter_text = self.canvas.create_text(300, 700, text=f"Love Meter: {self.love_meter}%", 
                                                 font=("Arial", 14), fill="#ff0066")
        self.hearts = []  # For animations

    def spin_note(self):
        mood = self.mood_var.get()
        other_player = "Player2" if self.current_player == "Player1" else "Player1"
        all_notes = self.notes[mood] + self.player_notes[other_player]
        note = random.choice(all_notes) if all_notes else "No notes yet—tease me with one!"
        
        # Spinning animation
        for i in range(10):
            self.canvas.itemconfig(self.note_text, text=f"Heating up... {i+1}")
            self.root.update()
            self.root.after(100)
        
        self.canvas.itemconfig(self.note_text, text=note)
        self.animate_hearts()
        
        # Sound (download "kiss.wav" or skip)
        try:
            pygame.mixer.Sound("kiss.wav").play()
        except:
            print("Sound file 'kiss.wav' not found—add it for extra heat!")
        
        self.pop_surprise()
        
        # Jackpot chance
        if random.random() < 0.3:  # 30% chance for a spicy jackpot
            self.love_meter = min(100, self.love_meter + 20)
            messagebox.showinfo("HOT JACKPOT!", "Things just got steamy—Meter spiked!")
            self.animate_jackpot()
        self.update_meter()

    def animate_hearts(self):
        self.canvas.delete("heart")
        for _ in range(8):  # More hearts for extra spice
            x, y = random.randint(150, 450), 700
            heart = self.canvas.create_text(x, y, text="💋", font=("Arial", 24), fill="#ff0066", tags="heart")
            self.hearts.append(heart)
        for i in range(25):
            for heart in self.hearts:
                self.canvas.move(heart, random.randint(-7, 7), -12)
            self.root.update()
            self.root.after(40)
        self.canvas.delete("heart")

    def animate_jackpot(self):
        # Spicy confetti
        for _ in range(15):
            x, y = random.randint(100, 500), random.randint(100, 700)
            confetti = self.canvas.create_text(x, y, text="🔥", font=("Arial", 20), fill="#ffcc00", tags="confetti")
            self.root.after(600, lambda: self.canvas.delete(confetti))

    def pop_surprise(self):
        surprises = [
            "Ooh, things are getting steamy!", 
            "You’re turning me on—stop it (don’t)!", 
            "Too sexy for words, babe!", 
            "Caught you melting my heart again!"
        ]
        messagebox.showinfo("Heat Alert!", random.choice(surprises))

    def love_dare(self):
        dare = random.choice(self.dares)
        response = messagebox.askyesno("Hot Dare!", f"Dare: {dare}\nDid you dare to do it?")
        if response:
            self.love_meter = min(100, self.love_meter + 15)
            messagebox.showinfo("Score!", "Love Meter SOARS! You’re on fire!")
        else:
            self.love_meter = max(0, self.love_meter - 10)
            messagebox.showinfo("Boo!", "Love Meter dips—don’t tease me like that!")
        self.update_meter()

    def switch_player(self):
        self.current_player = self.player_var.get()
        messagebox.showinfo("Switch!", f"Now it’s {self.current_player}’s turn to heat things up!")
        self.canvas.itemconfig(self.note_text, text=f"{self.current_player}, turn me on!")

    def add_player_note(self):
        note = self.custom_entry.get().strip()
        if note:
            other_player = "Player2" if self.current_player == "Player1" else "Player1"
            self.player_notes[other_player].append(note)
            self.save_player_notes()
            self.custom_entry.delete(0, tk.END)
            messagebox.showinfo("Sent!", f"Note dropped for {other_player}—make it naughty!")
        else:
            messagebox.showwarning("Hey!", "Don’t play coy—give me something spicy!")

    def update_meter(self):
        self.canvas.itemconfig(self.meter_text, text=f"Love Meter: {self.love_meter}%")
        if self.love_meter == 100:
            messagebox.showinfo("MAX HEAT!", "Love Meter maxed! We’re burning up together!")

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