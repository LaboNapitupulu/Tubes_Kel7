from collections import deque
import json
from tkinter import Toplevel, Label, Button, StringVar, Radiobutton, messagebox

class Stack:
    def _init_(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop() if self.items else None

    def is_empty(self):
        return len(self.items) == 0

class MuridWindow:
    def _init_(self, root, username, return_to_login):
        self.root = root
        self.root.title(f"Murid - {username}")
        self.root.geometry("500x600")
        self.username = username
        self.return_to_login = return_to_login  # Fungsi untuk kembali ke login

        self.questions = deque(self.load_questions())
        self.history = []
        self.score = 0
        self.total_bobot = 0

        if not self.questions:
            messagebox.showinfo("Info", "Belum ada soal tersedia!")
            root.destroy()
            return

        self.current_question = self.questions.popleft()
        self.answer = StringVar()
        self.options = []  # Untuk menyimpan opsi jawaban RadioButton

        # GUI Soal dan Pilihan
        Label(root, text="Soal").pack()
        self.question_label = Label(root, text="", wraplength=400, justify="left")
        self.question_label.pack(pady=10)

        for i in range(4):  # Buat 4 RadioButton untuk pilihan jawaban
            option = Radiobutton(root, text="", variable=self.answer, value=chr(65 + i))
            option.pack(anchor="w")
            self.options.append(option)

        Button(root, text="Jawab", command=self.jawab_soal).pack(pady=10)
        Button(root, text="Kembali ke Login", command=self.kembali_ke_login).pack(pady=10)

        # Tampilkan soal pertama
        self.update_question()

    def update_question(self):
        """Perbarui soal dan pilihan jawaban di GUI."""
        self.question_label.config(text=self.current_question["soal"])
        for i, opsi in enumerate(self.current_question["opsi"]):
            self.options[i].config(text=f"{chr(65 + i)}. {opsi}")
        self.answer.set("")  # Reset pilihan jawaban

    def jawab_soal(self):
        user_answer = self.answer.get()

        if not user_answer:  # Pastikan user memilih jawaban
            messagebox.showerror("Error", "Pilih jawaban terlebih dahulu!")
            return

        # Simpan jawaban ke history
        self.history.append({
            "soal": self.current_question["soal"],
            "opsi": self.current_question["opsi"],
            "jawaban_benar": self.current_question["jawaban"],
            "jawaban_user": user_answer,
            "bobot": self.current_question["bobot"]
        })

        # Hitung skor jika jawaban benar
        self.total_bobot += self.current_question["bobot"]
        if user_answer == self.current_question["jawaban"]:
            self.score += self.current_question["bobot"]

        # Pindah ke soal berikutnya
        if self.questions:
            self.current_question = self.questions.popleft()
            self.update_question()
        else:
            # Jika soal habis, tampilkan hasil akhir
            self.show_review()

    def show_review(self):
        """Tampilkan review jawaban setelah semua soal selesai."""
        review_window = Toplevel(self.root)
        review_window.title("Review Jawaban")
        review_window.geometry("500x600")

        Label(review_window, text=f"Total Skor Anda: {self.score}/{self.total_bobot}", font=("Arial", 14)).pack(pady=10)

        # Tampilkan semua soal, jawaban benar, dan jawaban user
        for idx, item in enumerate(self.history, start=1):
            Label(review_window, text=f"{idx}. {item['soal']}", wraplength=450, justify="left").pack(anchor="w", pady=5)
            for i, opsi in enumerate(item["opsi"]):
                Label(review_window, text=f"   {chr(65 + i)}. {opsi}", wraplength=450, justify="left").pack(anchor="w")
            Label(review_window, text=f"Jawaban Benar: {item['jawaban_benar']}", fg="green").pack(anchor="w")
            Label(review_window, text=f"Jawaban Anda: {item['jawaban_user']}", fg="blue").pack(anchor="w")

    def kembali_ke_login(self):
        """Tutup jendela dan kembali ke halaman login."""
        confirm = messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin kembali ke login?")
        if confirm:
            self.root.destroy()  # Tutup jendela murid
            self.return_to_login()  # Kembali ke login

    def load_questions(self):
        try:
            with open("D:/Coding/Ular/Tubes_Kel7/data/soal.json", "r") as f: #path sesuaikan dengan file local
                return json.load(f)
        except FileNotFoundError:
            return []
