import tkinter as tk
from tkinter import ttk
import time

# Top 20 widely spoken languages
languages = [
    "English", "Mandarin Chinese", "Hindi", "Spanish", "French",
    "Arabic", "Bengali", "Russian", "Portuguese", "Urdu",
    "Indonesian", "German", "Japanese", "Swahili", "Marathi",
    "Telugu", "Turkish", "Korean", "Vietnamese", "Tamil"
]

class TypingSpeedTester:
    def __init__(self, root):
        self.root = root
        self.root.title("🌐 Typing Speed Tester")
        self.root.geometry("950x500")
        self.root.configure(bg="#f0f4f7")

        self.language = tk.StringVar(value="English")
        self.start_time = 0
        self.timer_running = False

        self.create_widgets()

    def create_widgets(self):
        # Title label
        title = tk.Label(self.root, text="Typing Speed Tester", font=("Helvetica", 20, "bold"), bg="#f0f4f7", fg="#333")
        title.pack(pady=10)

        # Language selector
        frame_top = tk.Frame(self.root, bg="#f0f4f7")
        frame_top.pack()

        language_label = tk.Label(frame_top, text="Select Language:", font=("Arial", 12), bg="#f0f4f7")
        language_label.pack(side=tk.LEFT, padx=(10, 5))

        language_menu = ttk.Combobox(frame_top, textvariable=self.language, values=languages, state="readonly", width=25)
        language_menu.pack(side=tk.LEFT, padx=5)

        # Timer
        self.timer_label = tk.Label(frame_top, text="Time: 0s", font=("Arial", 12, "bold"), bg="#f0f4f7", fg="#007acc")
        self.timer_label.pack(side=tk.RIGHT, padx=(10, 20))

        # Input box
        self.input_text = tk.Text(self.root, height=10, width=100, font=("Courier", 12), wrap=tk.WORD, bd=2, relief=tk.SOLID)
        self.input_text.pack(pady=20, padx=20)
        self.input_text.bind("<KeyRelease>", self.start_timer)
        self.input_text.bind("<Return>", self.calculate_speed)

        # Result display
        self.result_label = tk.Label(self.root, text="", font=("Arial", 14, "bold"), bg="#f0f4f7", fg="#006400")
        self.result_label.pack(pady=10)

    def start_timer(self, event=None):
        if not self.timer_running:
            self.start_time = time.time()
            self.timer_running = True
            self.update_timer()

    def update_timer(self):
        if self.timer_running:
            elapsed = int(time.time() - self.start_time)
            self.timer_label.config(text=f"Time: {elapsed}s")
            self.root.after(1000, self.update_timer)

    def calculate_speed(self, event=None):
        if not self.timer_running:
            return

        elapsed_time = max(1, int(time.time() - self.start_time))
        typed_text = self.input_text.get(1.0, tk.END).strip()
        word_count = len(typed_text.split())

        speed = (word_count * 60) // elapsed_time
        lang = self.language.get()
        self.result_label.config(text=f"{lang} - Typing Speed: {speed} WPM")

        self.timer_running = False
        return "break"  # Prevent newline from being added

# Launch GUI
root = tk.Tk()
app = TypingSpeedTester(root)
root.mainloop()
root.mainloop()