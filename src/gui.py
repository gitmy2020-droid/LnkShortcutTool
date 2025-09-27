import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
from lnk_creator import LnkCreator

class LnkShortcutGUI(tk.Tk):
    """
    GUI for LNK Shortcut Creator.
    """

    def __init__(self):
        super().__init__()
        self.creator = LnkCreator()
        self.title("🔗 LNK Shortcut Creator - Security Tool")
        self.geometry("650x450")
        self.resizable(False, False)
        self.configure(bg="#f4f4f4")
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="LNK Shortcut Creator", font=("Arial", 16, "bold"), bg="#f4f4f4").pack(pady=10)
        tk.Label(self, text=self.creator.description, font=("Arial", 10), bg="#f4f4f4").pack()

        frame = tk.Frame(self, bg="#f4f4f4")
        frame.pack(padx=20, pady=10, fill="x")

        self.path_var = tk.StringVar()
        self.ip_var = tk.StringVar()
        self.share_var = tk.StringVar()
        self.file_var = tk.StringVar()
        self.icon_var = tk.StringVar()

        fields = [
            ("Save Path:", self.path_var, self.browse_path),
            ("Server IP:", self.ip_var, None),
            ("Share Name:", self.share_var, None),
            ("Target File:", self.file_var, None),
            ("Icon Path (optional):", self.icon_var, self.browse_icon)
        ]

        for i, (label, var, btn_cmd) in enumerate(fields):
            tk.Label(frame, text=label, bg="#f4f4f4").grid(row=i, column=0, sticky="w", pady=5)
            tk.Entry(frame, textvariable=var, width=50).grid(row=i, column=1, pady=5)
            if btn_cmd:
                tk.Button(frame, text="Browse", command=btn_cmd).grid(row=i, column=2, padx=5)

        create_btn = tk.Button(self, text="Create Shortcut", bg="#27ae60", fg="white", font=("Arial", 12, "bold"), command=self.create_shortcut_threaded)
        create_btn.pack(pady=20)

        self.result_text = tk.Text(self, height=8)
        self.result_text.pack(padx=20, pady=10, fill="both", expand=True)

        tk.Label(self, text=f"Version: {self.creator.version} | Security & Educational Use Only", font=("Arial", 8), bg="#f4f4f4").pack(side="bottom", pady=5)

    def browse_path(self):
        path = filedialog.askdirectory()
        if path:
            self.path_var.set(path)

    def browse_icon(self):
        file = filedialog.askopenfilename(filetypes=[("ICO files", "*.ico"), ("DLL files", "*.dll"), ("EXE files", "*.exe"), ("All files", "*.*")])
        if file:
            self.icon_var.set(file)

    def create_shortcut_threaded(self):
        if not all([self.path_var.get(), self.ip_var.get(), self.share_var.get(), self.file_var.get()]):
            messagebox.showerror("Error", "Please fill all required fields")
            return
        threading.Thread(target=self.create_shortcut).start()

    def create_shortcut(self):
        success, msg = self.creator.create_shortcut(
            self.path_var.get(),
            self.ip_var.get(),
            self.share_var.get(),
            self.file_var.get(),
            self.icon_var.get() if self.icon_var.get() else None
        )
        self.update_result(success, msg)

    def update_result(self, success, message):
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, message)
        if success:
            self.result_text.tag_configure("success", foreground="green")
            self.result_text.tag_add("success", 1.0, tk.END)
            messagebox.showinfo("Success", "Shortcut created successfully!")
        else:
            self.result_text.tag_configure("error", foreground="red")
            self.result_text.tag_add("error", 1.0, tk.END)
            messagebox.showerror("Error", "Failed to create shortcut.")
