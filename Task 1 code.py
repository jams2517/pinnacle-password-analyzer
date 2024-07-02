import re
import random
import string
import tkinter as tk
from tkinter import messagebox

class PasswordEvaluator:
    def __init__(self):
        self.common_passwords = set([
            "123456", "password", "123456789", "12345678", "12345", "1234567",
            "qwerty", "abc123", "football", "123123", "111111", "letmein", "welcome",
            "monkey", "password1", "passw0rd", "admin", "admin123"
        ])
        self.dictionary_words = set(["password", "welcome", "admin", "letmein", "football", "monkey", "shadow", "sunshine", "princess", "qwerty"])
    
    def evaluate(self, password):
        score = 0
        recommendations = []
        strength = "Weak"
        
        # Check length
        if len(password) >= 16:
            score += 2
        elif len(password) >= 12:
            score += 1
        else:
            recommendations.append("Password should be at least 12 characters long, preferably 16 or more.")
        
        # Check for uppercase letters
        if re.search(r'[A-Z]', password):
            score += 1
        else:
            recommendations.append("Add at least one uppercase letter.")
        
        # Check for lowercase letters
        if re.search(r'[a-z]', password):
            score += 1
        else:
            recommendations.append("Add at least one lowercase letter.")
        
        # Check for digits
        if re.search(r'[0-9]', password):
            score += 1
        else:
            recommendations.append("Add at least one digit.")
        
        # Check for special characters
        if re.search(r'[\W_]', password):
            score += 1
        else:
            recommendations.append("Add at least one special character.")
        
        # Check for common passwords
        if password.lower() in self.common_passwords:
            recommendations.append("Avoid common passwords.")
        
        # Check for dictionary words
        if any(word in password.lower() for word in self.dictionary_words):
            recommendations.append("Avoid dictionary words.")
        
        # Check for patterns
        if re.search(r'(.)\1{2,}', password):
            recommendations.append("Avoid patterns or repeated characters.")
        
        # Avoid commonly used substitutions
        if re.search(r'[@$!%*?&]', password) and any(char in password.lower() for char in ["p", "a", "s", "o"]):
            recommendations.append("Avoid commonly used substitutions (e.g., 'P@ssw0rd').")
        
        # Determine strength
        if score >= 7:
            strength = "Very Strong"
        elif score >= 5:
            strength = "Strong"
        elif score >= 3:
            strength = "Medium"
        
        # Determine types present in password
        password_types = []
        if re.search(r'[A-Z]', password):
            password_types.append("Uppercase Letters")
        if re.search(r'[a-z]', password):
            password_types.append("Lowercase Letters")
        if re.search(r'[0-9]', password):
            password_types.append("Digits")
        if re.search(r'[\W_]', password):
            password_types.append("Special Characters")

        return {
            "strength": strength,
            "score": score,
            "recommendations": recommendations,
            "password_types": password_types
        }

    def generate_strong_password(self, length=16):
        if length < 16:
            length = 16
        
        all_characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(all_characters) for _ in range(length))
        
        # Ensure the generated password meets all criteria
        while (not re.search(r'[A-Z]', password) or not re.search(r'[a-z]', password) or
               not re.search(r'[0-9]', password) or not re.search(r'[\W_]', password)):
            password = ''.join(random.choice(all_characters) for _ in range(length))
        
        return password

def evaluate_password():
    password = password_entry.get()
    result = evaluator.evaluate(password)
    
    result_text = f"Password Strength: {result['strength']}\n"
    result_text += f"Score: {result['score']}/7\n"
    
    if result['recommendations']:
        result_text += "Recommendations:\n"
        for recommendation in result['recommendations']:
            result_text += f"- {recommendation}\n"
    else:
        result_text += "No recommendations, your password is strong!"

    result_text += "\nPassword Types:\n"
    for password_type in result['password_types']:
        result_text += f"- {password_type}\n"
    
    result_label.config(text=result_text)
    
    # Change label color based on strength
    if result['strength'] == "Very Strong":
        result_label.config(fg="green")
    elif result['strength'] == "Strong":
        result_label.config(fg="blue")
    elif result['strength'] == "Medium":
        result_label.config(fg="orange")
    else:
        result_label.config(fg="red")

def generate_password():
    generated_password = evaluator.generate_strong_password()
    messagebox.showinfo("Generated Strong Password", f"Suggested Strong Password:\n{generated_password}")

def toggle_password():
    if show_password_var.get():
        password_entry.config(show="")
    else:
        password_entry.config(show="*")

# Create the main window
root = tk.Tk()
root.title("Password Strength Evaluator")

evaluator = PasswordEvaluator()

# Create and place the widgets
tk.Label(root, text="Enter a password to evaluate:").pack(pady=10)

password_entry = tk.Entry(root, show='*', width=30)
password_entry.pack(pady=5)

show_password_var = tk.BooleanVar()
show_password_check = tk.Checkbutton(root, text="Show Password", variable=show_password_var, command=toggle_password)
show_password_check.pack(pady=5)

evaluate_button = tk.Button(root, text="Evaluate Password", command=evaluate_password)
evaluate_button.pack(pady=10)

generate_button = tk.Button(root, text="Generate Strong Password", command=generate_password)
generate_button.pack(pady=10)

result_label = tk.Label(root, text="", justify="left", wraplength=400)
result_label.pack(pady=10)

# Run the main event loop
root.mainloop()
