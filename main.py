import tkinter as tk
from welcome_page import WelcomePage

def main():
    """Main entry point for the application"""
    root = tk.Tk()
    welcome = WelcomePage(root)
    root.mainloop()

if __name__ == "__main__":
    main()

