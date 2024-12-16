import json
from tkinter import Toplevel, Label, Entry, Button, StringVar, messagebox
from admin_gui import AdminWindow
from murid_gui import MuridWindow

class LoginWindow:
    def _init_(self, root):
        self.root = root
        self.root.geometry("300x200")

        # Variabel
        self.username = StringVar()
        self.password = StringVar()

        # GUI Login
        Label(root, text="Username").pack(pady=5)
        Entry(root, textvariable=self.username).pack(pady=5)
        Label(root, text="Password").pack(pady=5)
        Entry(root, textvariable=self.password, show="*").pack(pady=5)
        Button(root, text="Login", command=self.login).pack(pady=10)

    def login(self):
        username = self.username.get()
        password = self.password.get()

        users = self.load_users()
        if username in users and users[username]["password"] == password:
            role = users[username]["role"]
            messagebox.showinfo("Login Berhasil", f"Selamat datang, {username}!")
            self.root.withdraw()  # Menyembunyikan jendela login
            if role == "admin":
                self.open_admin_window()
            elif role == "murid":
                self.open_murid_window(username)
        else:
            messagebox.showerror("Login Gagal", "Username atau password salah.")

    def load_users(self):
        try:
            with open("D:/Coding/Ular/Tubes_Kel7/data/user.json", "r") as f: #path sesuaikan dengan file local
                return json.load(f)
        except FileNotFoundError:
            return {}

    def open_admin_window(self):
        admin_root = Toplevel(self.root)
        AdminWindow(admin_root, return_to_login=self.return_to_login)

    def open_murid_window(self, username):
        murid_root = Toplevel(self.root)
        MuridWindow(murid_root, username, return_to_login=self.return_to_login)

    def return_to_login(self):
        """Fungsi untuk kembali ke halaman login."""
        self.root.deiconify()  # Menampilkan kembali jendela login
