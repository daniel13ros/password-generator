# This is the main file for the password generator application.
# It imports the necessary modules and runs the application.

import customtkinter as ctk
import secrets
import string
import pyperclip  

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class PasswordGeneratorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Password Generator")
        self.geometry("460x520")

        self.label = ctk.CTkLabel(self, text="Password Generator", font=ctk.CTkFont(size=20, weight="bold"))
        self.label.pack(pady=20)

        self.password_display = ctk.CTkEntry(self, width=350, height=50, font=ctk.CTkFont(size=18), justify="center")
        self.password_display.pack(pady=10)

        self.length_label = ctk.CTkLabel(self, text="Length: 12", font=ctk.CTkFont(size=14))
        self.length_label.pack(pady=(10, 0))
        
        self.length_slider = ctk.CTkSlider(self, from_=8, to=32, number_of_steps=24, command=self.update_label)
        self.length_slider.set(12)
        self.length_slider.pack(pady=10)

        self.upper_var = ctk.BooleanVar(value=True)
        self.lower_var = ctk.BooleanVar(value=True)
        self.digits_var = ctk.BooleanVar(value=True)
        self.symbols_var = ctk.BooleanVar(value=True)

        self.check_frame = ctk.CTkFrame(self)
        self.check_frame.pack(pady=20, padx=40, fill="x")

        self.cb_upper = ctk.CTkCheckBox(self.check_frame, text="Upper case (A-Z)", variable=self.upper_var)
        self.cb_upper.grid(row=0, column=0, pady=10, padx=20, sticky="w")

        self.cb_lower = ctk.CTkCheckBox(self.check_frame, text="Lower case (a-z)", variable=self.lower_var)
        self.cb_lower.grid(row=1, column=0, pady=10, padx=20, sticky="w")

        self.cb_digits = ctk.CTkCheckBox(self.check_frame, text="Numbers (0-9)", variable=self.digits_var)
        self.cb_digits.grid(row=0, column=1, pady=10, padx=20, sticky="w")

        self.cb_symbols = ctk.CTkCheckBox(self.check_frame, text="Symbols (!@#$)", variable=self.symbols_var)
        self.cb_symbols.grid(row=1, column=1, pady=10, padx=20, sticky="w")

        self.generate_btn = ctk.CTkButton(self, text="Generate Password", command=self.generate_password, height=40, font=ctk.CTkFont(weight="bold"))
        self.generate_btn.pack(pady=10)

        self.copy_btn = ctk.CTkButton(self, text="Copy to Clipboard", fg_color="transparent", border_width=2, command=self.copy_to_clipboard)
        self.copy_btn.pack(pady=10)

    def update_label(self, value):
        self.length_label.configure(text=f"Length: {int(value)}")

    def generate_password(self):
        characters = ""
        if self.upper_var.get(): characters += string.ascii_uppercase
        if self.lower_var.get(): characters += string.ascii_lowercase
        if self.digits_var.get(): characters += string.digits
        if self.symbols_var.get(): characters += string.punctuation

        if not characters:
            self.password_display.delete(0, 'end')
            self.password_display.insert(0, "Please select at least one parameter")
            return

        length = int(self.length_slider.get())
        password = ''.join(secrets.choice(characters) for _ in range(length))
        
        self.password_display.delete(0, 'end')
        self.password_display.insert(0, password)

    def copy_to_clipboard(self):
        password = self.password_display.get()
        if password and password != "Please select at least one parameter":
            pyperclip.copy(password)
            self.copy_btn.configure(text="Copied!", fg_color="#2ecc71")
            self.after(2000, lambda: self.copy_btn.configure(text="Copy to Clipboard", fg_color="transparent"))

if __name__ == "__main__":
    app = PasswordGeneratorApp()
    app.mainloop()