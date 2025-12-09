import json
import tkinter as tk
from tkinter import messagebox, filedialog

DATA_FILE = "tasks.json"

class TodoApp:
    def __init__(self, root):
        self.root = root
        root.title("To-Do GUI — Abdullah's Task")
        root.geometry("420x520")
        root.resizable(False, False)

        self.frame = tk.Frame(root, padx=12, pady=12)
        self.frame.pack(fill="both", expand=True)

        header = tk.Label(self.frame, text="قائمة المهام", font=("Segoe UI", 16, "bold"))
        header.pack(pady=(0, 8))

        self.entry = tk.Entry(self.frame, font=("Segoe UI", 12))
        self.entry.pack(fill="x", pady=(0, 8))
        self.entry.bind("<Return>", lambda e: self.add_task())

        btn_frame = tk.Frame(self.frame)
        btn_frame.pack(fill="x", pady=(0, 8))

        add_btn = tk.Button(btn_frame, text="إضافة", command=self.add_task, width=10)
        add_btn.pack(side="left", padx=(0, 8))

        del_btn = tk.Button(btn_frame, text="حذف المحدد", command=self.delete_selected, width=12)
        del_btn.pack(side="left", padx=(0, 8))

        save_btn = tk.Button(btn_frame, text="حفظ", command=self.save_tasks, width=8)
        save_btn.pack(side="left")

        load_btn = tk.Button(btn_frame, text="تحميل", command=self.load_tasks, width=8)
        load_btn.pack(side="left", padx=(8, 0))

        self.listbox = tk.Listbox(self.frame, font=("Segoe UI", 12), selectmode=tk.SINGLE, activestyle='none')
        self.listbox.pack(fill="both", expand=True, pady=(8, 0))

        self.listbox.bind("<Double-Button-1>", self.toggle_complete)

        self.status = tk.Label(self.frame, text="عدد المهام: 0", anchor="w")
        self.status.pack(fill="x", pady=(8, 0))

        self.load_tasks()

    def add_task(self):
        text = self.entry.get().strip()
        if not text:
            messagebox.showinfo("تنبيه", "اكتب مهمة قبل الإضافة.")
            return
        self.listbox.insert(tk.END, text)
        self.entry.delete(0, tk.END)
        self.update_status()

    def delete_selected(self):
        sel = self.listbox.curselection()
        if not sel:
            messagebox.showinfo("تنبيه", "اختر مهمة للحذف.")
            return
        self.listbox.delete(sel[0])
        self.update_status()

    def toggle_complete(self, event=None):
        sel = self.listbox.curselection()
        if not sel:
            return
        i = sel[0]
        text = self.listbox.get(i)
        if text.startswith("✓ "):
            text = text[2:]
        else:
            text = "✓ " + text
        self.listbox.delete(i)
        self.listbox.insert(i, text)
        self.update_status()

    def update_status(self):
        count = self.listbox.size()
        completed = sum(1 for i in range(count) if self.listbox.get(i).startswith("✓ "))
        self.status.config(text=f"عدد المهام: {count} — منجزة: {completed}")

    def save_tasks(self):
        tasks = [self.listbox.get(i) for i in range(self.listbox.size())]
        path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON", "*.json")], initialfile=DATA_FILE)
        if not path:
            return
        with open(path, "w", encoding="utf-8") as f:
            json.dump(tasks, f, ensure_ascii=False, indent=2)
        messagebox.showinfo("نجاح", f"تم حفظ {len(tasks)} مهمة في:\n{path}")

    def load_tasks(self):
        path = filedialog.askopenfilename(defaultextension=".json", filetypes=[("JSON", "*.json")])
        if not path:
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    tasks = json.load(f)
            except Exception:
                tasks = []
        else:
            try:
                with open(path, "r", encoding="utf-8") as f:
                    tasks = json.load(f)
            except Exception as e:
                messagebox.showerror("خطأ", f"فشل تحميل الملف:\n{e}")
                return

        self.listbox.delete(0, tk.END)
        for t in tasks:
            self.listbox.insert(tk.END, t)
        self.update_status()

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
