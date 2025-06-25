import tkinter as tk
import random
from tkinter import messagebox
from collections import deque

class SnakeGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Enhanced Snake Game")
        self.master.resizable(False, False)
        
        # Game constants
        self.cell_size = 25  # Increased size for better visibility
        self.width = 25
        self.height = 20
        self.speed = 120  # Faster game
        self.speed_increase = 5  # Speed increase per food
        
        # Colors
        self.bg_color = "#121212"
        self.snake_color = "#4CAF50"
        self.head_color = "#2E7D32"
        self.food_color = "#FF5252"
        self.border_color = "#333333"
        self.text_color = "white"
        
        # Initialize game state
        self.snake = deque([(10, 10), (10, 9), (10, 8)])
        self.direction = "Right"
        self.next_direction = "Right"
        self.food = self.create_food()
        self.score = 0
        self.high_score = 0
        self.game_over = False
        self.paused = False
        
        # Create canvas with border
        self.canvas = tk.Canvas(
            master, 
            width=self.width * self.cell_size + 2,
            height=self.height * self.cell_size + 2,
            bg=self.border_color,
            highlightthickness=0
        )
        self.canvas.pack(pady=10)
        
        # Inner canvas for game area
        self.game_canvas = tk.Canvas(
            self.canvas,
            width=self.width * self.cell_size,
            height=self.height * self.cell_size,
            bg=self.bg_color,
            highlightthickness=0
        )
        self.game_canvas.place(x=1, y=1)
        
        # Score display
        self.score_frame = tk.Frame(master, bg=self.bg_color)
        self.score_frame.pack(fill=tk.X, padx=10)
        
        self.score_label = tk.Label(
            self.score_frame, 
            text=f"Score: {self.score}", 
            font=('Arial', 14, 'bold'),
            fg=self.text_color,
            bg=self.bg_color
        )
        self.score_label.pack(side=tk.LEFT)
        
        self.high_score_label = tk.Label(
            self.score_frame, 
            text=f"High Score: {self.high_score}", 
            font=('Arial', 14, 'bold'),
            fg=self.text_color,
            bg=self.bg_color
        )
        self.high_score_label.pack(side=tk.RIGHT)
        
        # Control buttons
        self.button_frame = tk.Frame(master, bg=self.bg_color)
        self.button_frame.pack(pady=5)
        
        self.pause_button = tk.Button(
            self.button_frame,
            text="Pause (Space)",
            command=self.toggle_pause,
            font=('Arial', 10),
            bg="#333333",
            fg="white"
        )
        self.pause_button.pack(side=tk.LEFT, padx=5)
        
        self.restart_button = tk.Button(
            self.button_frame,
            text="Restart (R)",
            command=self.reset_game,
            font=('Arial', 10),
            bg="#333333",
            fg="white"
        )
        self.restart_button.pack(side=tk.LEFT, padx=5)
        
        # Bind keyboard events
        self.master.bind("<KeyPress>", self.handle_keypress)
        
        # Start the game
        self.update()
    
    def create_food(self):
        while True:
            food = (
                random.randint(0, self.width - 1),
                random.randint(0, self.height - 1)
            )
            if food not in self.snake:
                return food
    
    def draw_snake(self):
        self.game_canvas.delete("snake")
        for i, segment in enumerate(self.snake):
            x, y = segment
            color = self.head_color if i == 0 else self.snake_color
            self.game_canvas.create_rectangle(
                x * self.cell_size,
                y * self.cell_size,
                (x + 1) * self.cell_size,
                (y + 1) * self.cell_size,
                fill=color,
                outline=self.bg_color,
                width=2,
                tag="snake"
            )
    
    def draw_food(self):
        self.game_canvas.delete("food")
        x, y = self.food
        # Draw food with a shine effect
        self.game_canvas.create_oval(
            x * self.cell_size + 2,
            y * self.cell_size + 2,
            (x + 1) * self.cell_size - 2,
            (y + 1) * self.cell_size - 2,
            fill=self.food_color,
            outline="",
            tag="food"
        )
        self.game_canvas.create_oval(
            x * self.cell_size + 5,
            y * self.cell_size + 5,
            x * self.cell_size + 10,
            y * self.cell_size + 10,
            fill="white",
            outline="",
            tag="food"
        )
    
    def handle_keypress(self, event):
        key = event.keysym
        if key == "space":
            self.toggle_pause()
        elif key == "r":
            self.reset_game()
        elif key in ["Up", "Down", "Left", "Right"] and not self.paused:
            if (key == "Up" and self.direction != "Down") or \
               (key == "Down" and self.direction != "Up") or \
               (key == "Left" and self.direction != "Right") or \
               (key == "Right" and self.direction != "Left"):
                self.next_direction = key
    
    def move_snake(self):
        if self.paused:
            return
            
        self.direction = self.next_direction
        head = self.snake[0]
        
        if self.direction == "Up":
            new_head = (head[0], head[1] - 1)
        elif self.direction == "Down":
            new_head = (head[0], head[1] + 1)
        elif self.direction == "Left":
            new_head = (head[0] - 1, head[1])
        elif self.direction == "Right":
            new_head = (head[0] + 1, head[1])
        
        # Check for collision with walls or self
        if (new_head[0] < 0 or new_head[0] >= self.width or 
            new_head[1] < 0 or new_head[1] >= self.height or 
            new_head in self.snake):
            self.game_over = True
            return
        
        self.snake.appendleft(new_head)
        
        # Check if snake ate food
        if new_head == self.food:
            self.score += 10
            self.speed = max(50, self.speed - self.speed_increase)  # Increase speed
            self.score_label.config(text=f"Score: {self.score}")
            self.food = self.create_food()
        else:
            self.snake.pop()
    
    def toggle_pause(self):
        self.paused = not self.paused
        if self.paused:
            self.pause_button.config(text="Resume (Space)")
            self.game_canvas.create_text(
                self.width * self.cell_size / 2,
                self.height * self.cell_size / 2,
                text="PAUSED",
                font=('Arial', 36, 'bold'),
                fill="white",
                tag="pause"
            )
        else:
            self.pause_button.config(text="Pause (Space)")
            self.game_canvas.delete("pause")
    
    def update(self):
        if not self.game_over:
            self.move_snake()
            self.draw_snake()
            self.draw_food()
            self.master.after(self.speed, self.update)
        else:
            self.high_score = max(self.high_score, self.score)
            self.high_score_label.config(text=f"High Score: {self.high_score}")
            
            result = messagebox.askyesno(
                "Game Over", 
                f"Game Over! Your score: {self.score}\nHigh Score: {self.high_score}\n\nPlay again?"
            )
            if result:
                self.reset_game()
            else:
                self.master.destroy()
    
    def reset_game(self):
        self.snake = deque([(10, 10), (10, 9), (10, 8)])
        self.direction = "Right"
        self.next_direction = "Right"
        self.food = self.create_food()
        self.score = 0
        self.score_label.config(text=f"Score: {self.score}")
        self.speed = 120
        self.game_over = False
        self.paused = False
        self.pause_button.config(text="Pause (Space)")
        self.game_canvas.delete("pause")
        self.update()

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()
