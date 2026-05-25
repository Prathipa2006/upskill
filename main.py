import json
import random
import tkinter as tk
from tkinter import messagebox
with open("questions.json") as f:
    questions = json.load(f)
 
random.shuffle(questions)  # Randomize order every time
 
current_question = 0
score = 0
 
window = tk.Tk()
window.title("Quiz Game")
window.geometry("600x450")
window.config(bg="#f0f4f8")
window.resizable(False, False)
 

# Top bar: question number and score
top_frame = tk.Frame(window, bg="#2c3e50", pady=10)
top_frame.pack(fill="x")
 
question_number_label = tk.Label(
    top_frame, text="Question 1 of 10",
    font=("Arial", 11), bg="#2c3e50", fg="white"
)
question_number_label.pack(side="left", padx=20)
 
score_label = tk.Label(
    top_frame, text="Score: 0",
    font=("Arial", 11, "bold"), bg="#2c3e50", fg="#2ecc71"
)
score_label.pack(side="right", padx=20)
 
# Question text
question_label = tk.Label(
    window, text="", font=("Arial", 14, "bold"),
    bg="#f0f4f8", fg="#2c3e50",
    wraplength=540, justify="center", pady=20
)
question_label.pack(pady=30)
 
# Feedback label (Correct! / Wrong!)
feedback_label = tk.Label(
    window, text="", font=("Arial", 11, "bold"),
    bg="#f0f4f8"
)
feedback_label.pack()
 
# Frame for 4 option buttons (2x2 grid)
options_frame = tk.Frame(window, bg="#f0f4f8")
options_frame.pack(pady=10)
 
option_buttons = []
for i in range(4):
    btn = tk.Button(
        options_frame, text="", font=("Arial", 11),
        width=25, height=2,
        bg="white", fg="#2c3e50",
        relief="groove", cursor="hand2",
        command=lambda i=i: check_answer(i)
    )
    row = i // 2
    col = i % 2
    btn.grid(row=row, column=col, padx=10, pady=8)
    option_buttons.append(btn)
 
 
def load_question():
    """Load and display the current question"""
    global current_question
 
    q = questions[current_question]
 
    # Update question number and score
    question_number_label.config(
        text=f"Question {current_question + 1} of {len(questions)}"
    )
    score_label.config(text=f"Score: {score}")
 
    # Display question text
    question_label.config(text=q["question"])
 
    # Clear feedback
    feedback_label.config(text="")
 
    # Display options on buttons
    for i, btn in enumerate(option_buttons):
        btn.config(
            text=q["options"][i],
            bg="white", fg="#2c3e50",
            state="normal"
        )
 
 
def check_answer(index):
    """Check if the selected answer is correct"""
    global score, current_question
 
    selected = questions[current_question]["options"][index]
    correct = questions[current_question]["answer"]
 
    # Disable all buttons so user can't click again
    for btn in option_buttons:
        btn.config(state="disabled")
 
    if selected == correct:
        score += 1
        feedback_label.config(text="Correct!", fg="green")
        option_buttons[index].config(bg="#2ecc71", fg="white")
    else:
        feedback_label.config(
            text=f"Wrong!  Correct answer is: {correct}", fg="red"
        )
        option_buttons[index].config(bg="#e74c3c", fg="white")
        # Highlight the correct answer in green
        for i, btn in enumerate(option_buttons):
            if questions[current_question]["options"][i] == correct:
                btn.config(bg="#2ecc71", fg="white")
 
    # Wait 1.5 seconds then go to next question
    window.after(1500, next_question)
 
 
def next_question():
    """Move to the next question or show final score"""
    global current_question
 
    current_question += 1
 
    if current_question < len(questions):
        load_question()
    else:
        show_final_score()
 
 
def show_final_score():
    """Clear screen and show the final score"""
    # Hide all widgets
    top_frame.pack_forget()
    question_label.pack_forget()
    feedback_label.pack_forget()
    options_frame.pack_forget()
 
    total = len(questions)
    percentage = (score / total) * 100
 
    if percentage >= 70:
        result_text = "Excellent! Well done!"
        result_color = "#2ecc71"
    elif percentage >= 40:
        result_text = "Good effort! Keep practicing."
        result_color = "#f39c12"
    else:
        result_text = "Better luck next time!"
        result_color = "#e74c3c"
 
    # Final score screen
    tk.Label(window, text="Quiz Completed!",
             font=("Arial", 22, "bold"),
             bg="#f0f4f8", fg="#2c3e50").pack(pady=40)
 
    tk.Label(window, text=f"Your Score: {score} / {total}",
             font=("Arial", 18),
             bg="#f0f4f8", fg="#2c3e50").pack()
 
    tk.Label(window, text=f"{percentage:.0f}%",
             font=("Arial", 36, "bold"),
             bg="#f0f4f8", fg=result_color).pack(pady=10)
 
    tk.Label(window, text=result_text,
             font=("Arial", 13),
             bg="#f0f4f8", fg=result_color).pack()
 
    # Play Again button
    tk.Button(window, text="Play Again",
              font=("Arial", 12, "bold"),
              bg="#2c3e50", fg="white",
              width=15, height=2,
              cursor="hand2",
              command=restart_game).pack(pady=30)
 
 
def restart_game():
    """Restart the quiz from the beginning"""
    global current_question, score
 
    current_question = 0
    score = 0
    random.shuffle(questions)
 
    # Show all widgets again
    top_frame.pack(fill="x")
    question_label.pack(pady=30)
    feedback_label.pack()
    options_frame.pack(pady=10)
 
    # Remove the final score widgets
    for widget in window.winfo_children():
        if widget not in [top_frame, question_label, feedback_label, options_frame]:
            widget.destroy()
 
    load_question()
 
load_question()
window.mainloop()