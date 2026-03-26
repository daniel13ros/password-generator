import customtkinter as ctk    # Modern UI framework
import secrets                 # Cryptographically strong random numbers for security
import string                  # Pre-defined character sets (ASCII letters, digits, etc.)
import pyperclip               # Cross-platform clipboard management
import random                  # Used for shuffling the final list (non-security critical)
import re                      # Regular Expressions for parsing and analyzing text strings

# Global UI Configuration
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class PasswordGeneratorApp(ctk.CTk):
    """
    Main application class for the Secure Password Generator.
    Inherits from ctk.CTk to create the main window.
    """
    def __init__(self):
        super().__init__()

        # --- Window Metadata & Constraints ---
        self.title("Secure Password Generator Pro")
        self.geometry("520x680")
        self.resizable(False, False)

        # --- Header Label ---
        self.label = ctk.CTkLabel(self, text="Password Generator", font=ctk.CTkFont(size=24, weight="bold"))
        self.label.pack(pady=(30, 10))

        # --- Main Password Entry Box ---
        # Allows both manual typing and automatic generation display
        self.password_display = ctk.CTkEntry(
            self, width=400, height=50, font=ctk.CTkFont(size=18), 
            justify="center", placeholder_text="Type or generate a password..."
        )
        self.password_display.pack(pady=10)
        
        # --- Real-Time Event Binding ---
        # Trigger 'check_manual_strength' whenever a key is released inside the entry box
        self.password_display.bind("<KeyRelease>", self.check_manual_strength)

        # --- Strength Meter UI ---
        # Provides visual feedback on password security levels
        self.strength_label = ctk.CTkLabel(self, text="Strength: ---", font=ctk.CTkFont(size=13, weight="bold"))
        self.strength_label.pack(pady=(5, 0))
        
        self.strength_bar = ctk.CTkProgressBar(self, width=350, height=10)
        self.strength_bar.set(0) # Default to 0 until a password is typed/generated
        self.strength_bar.pack(pady=10)

        # --- Password Length Slider ---
        self.length_label = ctk.CTkLabel(self, text="Length: 12", font=ctk.CTkFont(size=14))
        self.length_label.pack(pady=(15, 0))
        
        self.length_slider = ctk.CTkSlider(self, from_=8, to=32, number_of_steps=24, command=self.update_ui_on_slider)
        self.length_slider.set(12)
        self.length_slider.pack(pady=10)

        # --- Parameter Variables (Boolean) ---
        self.upper_var, self.lower_var = ctk.BooleanVar(value=True), ctk.BooleanVar(value=True)
        self.digits_var, self.symbols_var = ctk.BooleanVar(value=True), ctk.BooleanVar(value=True)

        # --- Checkbox Container (Frame) ---
        self.check_frame = ctk.CTkFrame(self)
        self.check_frame.pack(pady=20, padx=40, fill="x")

        # Layout checkboxes using a 2x2 Grid system
        ctk.CTkCheckBox(self.check_frame, text="Uppercase", variable=self.upper_var).grid(row=0, column=0, pady=12, padx=20, sticky="w")
        ctk.CTkCheckBox(self.check_frame, text="Lowercase", variable=self.lower_var).grid(row=1, column=0, pady=12, padx=20, sticky="w")
        ctk.CTkCheckBox(self.check_frame, text="Numbers", variable=self.digits_var).grid(row=0, column=1, pady=12, padx=20, sticky="w")
        ctk.CTkCheckBox(self.check_frame, text="Symbols", variable=self.symbols_var).grid(row=1, column=1, pady=12, padx=20, sticky="w")

        # --- Functional Buttons ---
        self.generate_btn = ctk.CTkButton(self, text="GENERATE", command=self.generate_password, height=45, font=ctk.CTkFont(weight="bold"))
        self.generate_btn.pack(pady=10)

        self.copy_btn = ctk.CTkButton(self, text="Copy to Clipboard", fg_color="transparent", border_width=2, command=self.copy_to_clipboard)
        self.copy_btn.pack(pady=10)

        # --- Theme Switcher ---
        self.mode_switch = ctk.CTkSwitch(self, text="Dark Mode", command=self.toggle_mode)
        self.mode_switch.select() # Default to dark mode
        self.mode_switch.pack(pady=(20, 10))

    # --- UI & Transition Methods ---

    def update_ui_on_slider(self, value):
        """Dynamic update of the length label when the slider moves."""
        self.length_label.configure(text=f"Length: {int(value)}")

    def toggle_mode(self):
        """Delays the theme swap slightly to allow for a smoother UI switch animation."""
        self.after(200, self._apply_theme_change)

    def _apply_theme_change(self):
        """Actually applies the Light/Dark mode change."""
        if self.mode_switch.get() == 1:
            ctk.set_appearance_mode("dark")
        else:
            ctk.set_appearance_mode("light")

    # --- Core Security & Analysis Logic ---

    def evaluate_strength(self, password):
        """
        Analyzes password strength based on real-time content.
        Uses Regex to detect character variety and calculates a normalized score (0 to 1.0).
        """
        if not password:
            return 0, "---", "gray"

        length = len(password)
        
        # Regex scans to verify presence of specific character types
        has_upper = 1 if re.search(r'[A-Z]', password) else 0
        has_lower = 1 if re.search(r'[a-z]', password) else 0
        has_digits = 1 if re.search(r'[0-9]', password) else 0
        # Re.escape ensures special punctuation marks are treated as literals
        has_symbols = 1 if re.search(r'[{}]'.format(re.escape(string.punctuation)), password) else 0
        
        variety_score = has_upper + has_lower + has_digits + has_symbols
        
        # Security Metric: Length counts for 60%, Variety counts for 40%
        score = min(1.0, (length / 24) * 0.6 + (variety_score / 4) * 0.4)
        
        # Classification thresholds
        if score < 0.3 or variety_score < 2:
            return score, "Weak", "#e74c3c"    # Red
        elif score < 0.6:
            return score, "Medium", "#f39c12"  # Orange
        else:
            return score, "Strong", "#2ecc71"  # Green

    def check_manual_strength(self, event=None):
        """Callback for keyboard events to update the strength meter in real-time."""
        password = self.password_display.get()
        score, text, color = self.evaluate_strength(password)
        
        # Update UI components with new metrics
        self.strength_bar.set(score)
        self.strength_bar.configure(progress_color=color)
        self.strength_label.configure(text=f"Strength: {text}", text_color=color)

    def generate_password(self):
        """
        Creates a new secure password based on user constraints.
        Enforces a minimum 25% quota for each selected character type for maximum entropy.
        """
        pools = []
        if self.upper_var.get(): pools.append(string.ascii_uppercase)
        if self.lower_var.get(): pools.append(string.ascii_lowercase)
        if self.digits_var.get(): pools.append(string.digits)
        if self.symbols_var.get(): pools.append(string.punctuation)

        if not pools:
            self.password_display.delete(0, 'end')
            self.password_display.insert(0, "Select at least one option!")
            return

        length = int(self.length_slider.get())
        password_list = []
        
        # Quota Phase: Fill 1/4 of total length with each selected character pool
        quota = length // 4
        for pool in pools:
            for _ in range(quota):
                password_list.append(secrets.choice(pool))
        
        # Filling Phase: Randomly select from the union of all pools to reach full length
        remaining = length - len(password_list)
        all_chars = "".join(pools)
        for _ in range(remaining):
            password_list.append(secrets.choice(all_chars))
            
        # Shuffle Phase: Randomize list order (since items were added in specific pool blocks)
        random.shuffle(password_list)
        final_password = "".join(password_list)
        
        # Update Display and reset Strength Meter
        self.password_display.delete(0, 'end')
        self.password_display.insert(0, final_password)
        self.check_manual_strength()

    def copy_to_clipboard(self):
        """Transfers current password text to system clipboard and updates button text."""
        content = self.password_display.get()
        if content:
            pyperclip.copy(content)
            self.copy_btn.configure(text="Copied!", fg_color="#2ecc71")
            # Return button to original state after 2 seconds
            self.after(2000, lambda: self.copy_btn.configure(text="Copy to Clipboard", fg_color="transparent"))

if __name__ == "__main__":
    app = PasswordGeneratorApp()
    app.mainloop()