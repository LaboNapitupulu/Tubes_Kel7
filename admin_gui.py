import json
from tkinter import Label, Entry, Button, Listbox, StringVar, Toplevel, messagebox

class TreeNode:
    def __init__(self, data):
        self.data = data
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def traverse(self, result=None):
        if result is None:
            result = []
        if isinstance(self.data, dict):  # Hanya soal yang disimpan
            result.append(self.data)
        for child in self.children:
            child.traverse(result)
        return result

class AdminWindow:
    def __init__(self, root, return_to_login):
        self.root = root
        self.root.geometry("600x700")  # Ukuran jendela yang lebih besar
        self.root.title("Admin - Kelola Soal")
        self.return_to_login = return_to_login

        # Variabel untuk input
        self.soal = StringVar()
        self.opsi_a = StringVar()
        self.opsi_b = StringVar()
        self.opsi_c = StringVar()
        self.opsi_d = StringVar()
        self.jawaban = StringVar()
        self.bobot = StringVar()
        self.kategori = StringVar()

        # GUI Input
        Label(root, text="Kategori (Mudah/Sedang/Sulit)").pack(pady=5)
        Entry(root, textvariable=self.kategori).pack(pady=5)
        Label(root, text="Pertanyaan").pack(pady=5)
        Entry(root, textvariable=self.soal).pack(pady=5)
        Label(root, text="Opsi A").pack(pady=5)
        Entry(root, textvariable=self.opsi_a).pack(pady=5)
        Label(root, text="Opsi B").pack(pady=5)
        Entry(root, textvariable=self.opsi_b).pack(pady=5)
        Label(root, text="Opsi C").pack(pady=5)
        Entry(root, textvariable=self.opsi_c).pack(pady=5)
        Label(root, text="Opsi D").pack(pady=5)
        Entry(root, textvariable=self.opsi_d).pack(pady=5)
        Label(root, text="Jawaban Benar (A/B/C/D)").pack(pady=5)
        Entry(root, textvariable=self.jawaban).pack(pady=5)
        Label(root, text="Bobot Nilai").pack(pady=5)
        Entry(root, textvariable=self.bobot).pack(pady=5)

        Button(root, text="Tambah Soal", command=self.tambah_soal).pack(pady=5)
        Button(root, text="Tampilkan Semua Soal", command=self.tampilkan_soal).pack(pady=5)
        Button(root, text="Hapus Soal", command=self.hapus_soal).pack(pady=5)
        Button(root, text="Hapus Semua Soal", command=self.hapus_semua_soal).pack(pady=5)

        # Bangun tree dari soal yang sudah ada di soal.json
        self.tree_root = self.load_questions()

        # Tombol kembali ke login di bagian bawah
        self.kembali_button = Button(root, text="Kembali ke Login", command=self.kembali_ke_login)
        self.kembali_button.pack(side="bottom", pady=10)

    def build_tree(self):
        root = TreeNode("Kuis")
        root.add_child(TreeNode("Mudah"))
        root.add_child(TreeNode("Sedang"))
        root.add_child(TreeNode("Sulit"))
        return root

    def load_questions(self, file="D:/Coding/Ular/Tubes_Kel7/data/soal.json"): #path sesuaikan dengan file local
        try:
            with open(file, "r") as f:
                questions = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            questions = []

        tree_root = self.build_tree()

        # Menempatkan soal ke kategori yang sesuai
        for question in questions:
            kategori = question.get("kategori", "Mudah")  # Default kategori jika tidak ada
            node = self.find_category_node(tree_root, kategori)
            if node:
                node.add_child(TreeNode(question))

        return tree_root

    def save_questions(self, node, file="D:/Coding/Ular/Tubes_Kel7/data/soal.json"):
        questions = []

        # Traverse TreeNode untuk mengumpulkan soal
        def traverse(node):
            if isinstance(node.data, dict):
                questions.append(node.data)
            for child in node.children:
                traverse(child)

        traverse(node)  # Traverse mulai dari root
        with open(file, "w") as f:
            json.dump(questions, f, indent=4)

    def find_category_node(self, tree, kategori):
        for child in tree.children:
            if child.data == kategori:
                return child
        return None

    def tambah_soal(self):
        kategori = self.kategori.get()
        soal = self.soal.get()
        opsi = [self.opsi_a.get(), self.opsi_b.get(), self.opsi_c.get(), self.opsi_d.get()]
        jawaban = self.jawaban.get().upper()
        try:
            bobot = int(self.bobot.get())
        except ValueError:
            messagebox.showerror("Error", "Bobot nilai harus berupa angka!")
            return

        if not kategori or not soal or not jawaban or len(opsi) < 4:
            messagebox.showerror("Error", "Lengkapi semua data!")
            return

        node = self.find_category_node(self.tree_root, kategori)
        if node:
            node.add_child(TreeNode({
                "kategori": kategori,
                "soal": soal,
                "opsi": opsi,
                "jawaban": jawaban,
                "bobot": bobot
            }))
            self.save_questions(self.tree_root)  # Simpan soal ke soal.json
            messagebox.showinfo("Sukses", "Soal berhasil ditambahkan!")
        else:
            messagebox.showerror("Error", "Kategori tidak valid! Gunakan Mudah/Sedang/Sulit.")

    def tampilkan_soal(self):
        questions = self.tree_root.traverse()

        soal_window = Toplevel(self.root)
        soal_window.title("Daftar Soal")
        listbox = Listbox(soal_window, width=80, height=20)
        listbox.pack(fill="both", expand=True)

        for question in questions:
            if isinstance(question, dict):
                listbox.insert("end", f"[{question['kategori']}] {question['soal']} - Bobot: {question['bobot']}")

    def hapus_soal(self):
        questions = self.tree_root.traverse()
        if not questions:
            messagebox.showinfo("Info", "Tidak ada soal yang tersedia untuk dihapus.")
            return

        soal_window = Toplevel(self.root)
        soal_window.title("Hapus Soal")
        listbox = Listbox(soal_window, width=80, height=20)
        listbox.pack(fill="both", expand=True)

        for idx, question in enumerate(questions):
            if isinstance(question, dict):
                listbox.insert("end", f"[{idx+1}] {question['kategori']} - {question['soal']}")

        def hapus_terpilih():
            selected = listbox.curselection()
            if not selected:
                messagebox.showerror("Error", "Pilih soal yang ingin dihapus.")
                return

            # Mendapatkan index soal yang dipilih
            index = selected[0]

            # Hapus soal dari TreeNode berdasarkan index
            self.remove_question_from_tree(questions[index])
            
            # Simpan perubahan ke soal.json
            self.save_questions(self.tree_root)
            soal_window.destroy()
            messagebox.showinfo("Sukses", "Soal berhasil dihapus!")

        Button(soal_window, text="Hapus Terpilih", command=hapus_terpilih).pack(pady=10)

    def hapus_semua_soal(self):
        confirm = messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin menghapus semua soal?")
        if confirm:
            self.tree_root = self.build_tree()  # Reset TreeNode
            self.save_questions(self.tree_root)
            messagebox.showinfo("Sukses", "Semua soal berhasil dihapus!")

    def remove_question_from_tree(self, question_to_remove):
        """Hapus soal tertentu dari TreeNode."""
        def traverse_and_remove(node):
            node.children = [child for child in node.children if child.data != question_to_remove]
            for child in node.children:
                traverse_and_remove(child)

        traverse_and_remove(self.tree_root)

    def kembali_ke_login(self):
        # Menampilkan konfirmasi sebelum keluar
        confirm = messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin kembali ke halaman login?")
        if confirm:
            self.root.destroy()  # Tutup jendela Admin
            self.return_to_login()  # Kembali ke login
