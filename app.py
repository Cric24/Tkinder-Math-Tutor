import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import random
import time
import json
from PIL import Image, ImageTk  # Pillow library for images

class MathTutorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Math Tutor")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        self.root.configure(bg="#1a1a1a")  # Set root background to dark grey
        
        # Apply styles
        self.style = ttk.Style()
        self.style.configure('TButton', font=('Roboto', 12), padding=10, relief='flat', background='#4CAF50', foreground='#000000')  # Button text color to black
        self.style.map('TButton', background=[('active', '#45a049')])
        self.style.configure('TLabel', font=('Roboto', 14), background='#1a1a1a', foreground='#ffffff')  # Labels with white text on dark grey background
        self.style.configure('TEntry', font=('Roboto', 14), padding=5)
        
        # Variables to track progress
        self.total_problems = 0
        self.correct_answers = 0
        self.incorrect_answers = 0
        
        # Load users and scores data
        self.load_data()

        # Create main menu
        self.create_login_menu()
    
    def load_data(self):
        try:
            with open('users.json', 'r') as file:
                self.users = json.load(file)
        except FileNotFoundError:
            self.users = {}
        
        try:
            with open('leaderboard.json', 'r') as file:
                self.leaderboard = json.load(file)
        except FileNotFoundError:
            self.leaderboard = []

    def save_data(self):
        with open('users.json', 'w') as file:
            json.dump(self.users, file)
        
        with open('leaderboard.json', 'w') as file:
            json.dump(self.leaderboard, file)
    
    def create_login_menu(self):
        self.clear_frame()
        self.login_frame = tk.Frame(self.root, bg="#1a1a1a", bd=5, relief='raised')
        self.login_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ttk.Label(self.login_frame, text="Math Tutor", font=("Roboto", 20, 'bold'), background="#1a1a1a", foreground="#ffffff").pack(pady=20)
        ttk.Label(self.login_frame, text="Login", font=("Roboto", 16), background="#1a1a1a", foreground="#ffffff").pack(pady=10)
        
        self.username_entry = ttk.Entry(self.login_frame, font=("Roboto", 14))
        self.username_entry.pack(pady=10)
        self.username_entry.insert(0, "Username")
        
        self.password_entry = ttk.Entry(self.login_frame, font=("Roboto", 14), show="*")
        self.password_entry.pack(pady=10)
        self.password_entry.insert(0, "Password")
        
        ttk.Button(self.login_frame, text="Login", command=self.login).pack(pady=10)
        ttk.Button(self.login_frame, text="Register", command=self.register).pack(pady=10)

        self.show_password_var = tk.BooleanVar(value=False)
        self.show_password_checkbox = tk.Checkbutton(self.login_frame, text="Show Password", variable=self.show_password_var, onvalue=True, offvalue=False, command=self.toggle_password_visibility, bg="#1a1a1a", fg="#ffffff", selectcolor="#1a1a1a")
        self.show_password_checkbox.pack(pady=10)

    def toggle_password_visibility(self):
       if self.show_password_var.get():
           self.password_entry.config(show="")
       else:
           self.password_entry.config(show="*")


    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if username in self.users and self.users[username] == password:
            self.current_user = username
            self.create_main_menu()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")
    
    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if username in self.users:
            messagebox.showerror("Register Failed", "Username already exists")
        else:
            self.users[username] = password
            self.save_data()
            messagebox.showinfo("Register Success", "User registered successfully")
    
    def create_main_menu(self):
        self.clear_frame()
        self.main_frame = tk.Frame(self.root, bg="#1a1a1a", bd=5, relief='raised')
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ttk.Label(self.main_frame, text=f"Welcome, {self.current_user}", font=("Roboto", 20, 'bold'), background="#1a1a1a", foreground="#ffffff").pack(pady=20)
        
        ttk.Button(self.main_frame, text="Practice", command=self.open_practice).pack(pady=10)
        ttk.Button(self.main_frame, text="Quiz", command=self.open_quiz).pack(pady=10)
        ttk.Button(self.main_frame, text="Progress", command=self.view_progress).pack(pady=10)
        ttk.Button(self.main_frame, text="Leaderboard", command=self.view_leaderboard).pack(pady=10)
        ttk.Button(self.main_frame, text="Settings", command=self.open_settings).pack(pady=10)
        ttk.Button(self.main_frame, text="Logout", command=self.create_login_menu).pack(pady=10)
    
    def open_practice(self):
       self.clear_frame()
       self.practice_frame = tk.Frame(self.root, bg="#1a1a1a", bd=5, relief='raised')
       self.practice_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
       self.problem_label = ttk.Label(self.practice_frame, text="", background="#1a1a1a", foreground="#ffffff")
       self.problem_label.pack(pady=20)
    
       self.answer_entry = ttk.Entry(self.practice_frame)
       self.answer_entry.pack(pady=10)
    
       ttk.Button(self.practice_frame, text="Submit", command=self.check_practice_answer).pack(pady=10)
       ttk.Button(self.practice_frame, text="New Problem", command=self.generate_problem).pack(pady=10)
    
       self.feedback_label = ttk.Label(self.practice_frame, text="", background="#1a1a1a", foreground="#ffffff")
       self.feedback_label.pack(pady=20)
    
       ttk.Button(self.practice_frame, text="Back to Menu", command=self.create_main_menu).pack(pady=20)
    
       self.generate_problem()

    
    def generate_problem(self):
        self.num1 = random.randint(1, 10)
        self.num2 = random.randint(1, 10)
        self.operator = random.choice(["+", "-", "*", "/"])
        
        if self.operator == "+":
            self.correct_answer = self.num1 + self.num2
        elif self.operator == "-":
            self.correct_answer = self.num1 - self.num2
        elif self.operator == "*":
            self.correct_answer = self.num1 * self.num2
        else:
            self.correct_answer = round(self.num1 / self.num2, 2)
        
        self.problem_label.config(text=f"{self.num1} {self.operator} {self.num2}")
        self.answer_entry.delete(0, tk.END)
        self.feedback_label.config(text="")
    
    def check_practice_answer(self):
        try:
            user_answer = float(self.answer_entry.get())
            if user_answer == self.correct_answer:
                self.feedback_label.config(text="Correct!", foreground="green")
                self.correct_answers += 1
            else:
                self.feedback_label.config(text=f"Incorrect. The correct answer is {self.correct_answer}", foreground="red")
                self.incorrect_answers += 1
            self.total_problems += 1
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter a valid number")
    
    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def open_quiz(self):
        self.clear_frame()
        self.quiz_frame = tk.Frame(self.root, bg="#1a1a1a", bd=5, relief='raised')
        self.quiz_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.problem_label = ttk.Label(self.quiz_frame, text="", background="#1a1a1a", foreground="#ffffff")
        self.problem_label.pack(pady=20)
        
        self.answer_entry = ttk.Entry(self.quiz_frame)
        self.answer_entry.pack(pady=10)
        
        self.feedback_label = ttk.Label(self.quiz_frame, text="", background="#1a1a1a", foreground="#ffffff")
        self.feedback_label.pack(pady=20)
        
        ttk.Button(self.quiz_frame, text="Submit", command=self.check_quiz_answer).pack(pady=10)
        
        self.start_quiz()
    
    def start_quiz(self):
        self.quiz_problems = 0
        self.quiz_correct = 0
        self.quiz_incorrect = 0
        self.generate_quiz_problem()
        self.start_time = time.time()
    
    def generate_quiz_problem(self):
        self.num1 = random.randint(1, 10)
        self.num2 = random.randint(1, 10)
        self.operator = random.choice(["+", "-", "*", "/"])
        
        if self.operator == "+":
            self.correct_answer = self.num1 + self.num2
        elif self.operator == "-":
            self.correct_answer = self.num1 - self.num2
        elif self.operator == "*":
            self.correct_answer = self.num1 * self.num2
        else:
            self.correct_answer = round(self.num1 / self.num2, 2)
        
        self.problem_label.config(text=f"{self.num1} {self.operator} {self.num2}")
        self.answer_entry.delete(0, tk.END)
        self.feedback_label.config(text="")
    
    def check_quiz_answer(self):
        try:
            user_answer = float(self.answer_entry.get())
            if user_answer == self.correct_answer:
                self.quiz_correct += 1
            else:
                self.quiz_incorrect += 1
            self.quiz_problems += 1
            if self.quiz_problems < 10:
                self.generate_quiz_problem()
            else:
                self.end_quiz()
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter a valid number")
    
    def end_quiz(self):
        end_time = time.time()
        elapsed_time = round(end_time - self.start_time, 2)
        score = self.quiz_correct * 10 - self.quiz_incorrect * 5
        messagebox.showinfo("Quiz Finished", f"You answered {self.quiz_correct} questions correctly out of 10.\nYour score is {score}\nTime taken: {elapsed_time} seconds")
        self.leaderboard.append((self.current_user, score, elapsed_time))
        self.save_data()
        self.create_main_menu()
    
    def view_progress(self):
        self.clear_frame()
        self.progress_frame = tk.Frame(self.root, bg="#1a1a1a", bd=5, relief='raised')
        self.progress_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ttk.Label(self.progress_frame, text="Progress", font=("Roboto", 20, 'bold'), background="#1a1a1a", foreground="#ffffff").pack(pady=20)
        
        progress_text = f"Total Problems: {self.total_problems}\nCorrect Answers: {self.correct_answers}\nIncorrect Answers: {self.incorrect_answers}"
        ttk.Label(self.progress_frame, text=progress_text, background="#1a1a1a", foreground="#ffffff").pack(pady=20)
        
        ttk.Button(self.progress_frame, text="Back to Menu", command=self.create_main_menu).pack(pady=20)
    
    def view_leaderboard(self):
        self.clear_frame()
        self.leaderboard_frame = tk.Frame(self.root, bg="#1a1a1a", bd=5, relief='raised')
        self.leaderboard_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ttk.Label(self.leaderboard_frame, text="Leaderboard", font=("Roboto", 20, 'bold'), background="#1a1a1a", foreground="#ffffff").pack(pady=20)
        
        leaderboard_text = "\n".join([f"{user}: {score} points, {time}s" for user, score, time in sorted(self.leaderboard, key=lambda x: x[1], reverse=True)[:10]])
        ttk.Label(self.leaderboard_frame, text=leaderboard_text, background="#1a1a1a", foreground="#ffffff").pack(pady=20)
        
        ttk.Button(self.leaderboard_frame, text="Back to Menu", command=self.create_main_menu).pack(pady=20)
    
    def open_settings(self):
        self.clear_frame()
        self.settings_frame = tk.Frame(self.root, bg="#1a1a1a", bd=5, relief='raised')
        self.settings_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ttk.Label(self.settings_frame, text="Settings", font=("Roboto", 20, 'bold'), background="#1a1a1a", foreground="#ffffff").pack(pady=20)
        
        ttk.Label(self.settings_frame, text="Background Color", background="#1a1a1a", foreground="#ffffff").pack(pady=10)
        
        self.bg_color_var = tk.StringVar(value="#1a1a1a")
        ttk.Entry(self.settings_frame, textvariable=self.bg_color_var).pack(pady=10)
        
        ttk.Button(self.settings_frame, text="Save", command=self.save_settings).pack(pady=20)
        ttk.Button(self.settings_frame, text="Back to Menu", command=self.create_main_menu).pack(pady=20)
    
    def save_settings(self):
        self.root.configure(bg=self.bg_color_var.get())
        self.settings_frame.configure(bg=self.bg_color_var.get())
        self.create_main_menu()

if __name__ == "__main__":
    root = tk.Tk()
    app = MathTutorApp(root)
    root.mainloop()
