from tkinter import Tk
from auth_gui import LoginWindow

def main():
    root = Tk()
    root.title("Aplikasi Kuis")
    app = LoginWindow(root)  # Memulai halaman login
    root.mainloop()

if __name__ == "__main__":
    main()
