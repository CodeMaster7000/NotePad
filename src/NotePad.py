import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

class NotepadApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Untitled - Notepad")
        self.textarea = tk.Text(self.master, undo=True)
        self.textarea.pack(fill=tk.BOTH, expand=True)
        self.menubar = tk.Menu(self.master)
        self.master.config(menu=self.menubar)
        self.file_menu = tk.Menu(self.menubar, tearoff=0)
        self.file_menu.add_command(label="New", command=self.new_file)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_command(label="Save As", command=self.save_as_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.exit_app)
        self.menubar.add_cascade(label="File", menu=self.file_menu)
        self.edit_menu = tk.Menu(self.menubar, tearoff=0)
        self.edit_menu.add_command(label="Undo", command=self.textarea.edit_undo)
        self.edit_menu.add_command(label="Redo", command=self.textarea.edit_redo)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Cut", command=self.cut_text)
        self.edit_menu.add_command(label="Copy", command=self.copy_text)
        self.edit_menu.add_command(label="Paste", command=self.paste_text)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Find", command=self.find_text)
        self.edit_menu.add_command(label="Replace", command=self.replace_text)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Select All", command=self.select_all)
        self.menubar.add_cascade(label="Edit", menu=self.edit_menu)
        self.format_menu = tk.Menu(self.menubar, tearoff=0)
        self.format_menu.add_command(label="Font", command=self.change_font)
        self.menubar.add_cascade(label="Format", menu=self.format_menu)
        self.statusbar = tk.Label(self.master, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.statusbar.pack(side=tk.BOTTOM, fill=tk.X)

    def new_file(self):
        self.textarea.delete(1.0, tk.END)

    def open_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, "r") as file:
                self.textarea.delete(1.0, tk.END)
                self.textarea.insert(1.0, file.read())

    def save_file(self):
        pass  

    def save_as_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                  filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "w") as file:
                file.write(self.textarea.get(1.0, tk.END))

    def exit_app(self):
        self.master.destroy()

    def cut_text(self):
        self.textarea.event_generate("<<Cut>>")

    def copy_text(self):
        self.textarea.event_generate("<<Copy>>")

    def paste_text(self):
        self.textarea.event_generate("<<Paste>>")

    def find_text(self):
        find_str = simpledialog.askstring("Find", "Enter text to find:")
        if find_str:
            start_pos = self.textarea.search(find_str, "1.0", tk.END)
            if start_pos:
                end_pos = f"{start_pos}+{len(find_str)}c"
                self.textarea.tag_add(tk.SEL, start_pos, end_pos)
                self.textarea.mark_set(tk.INSERT, end_pos)
                self.textarea.see(tk.INSERT)

    def replace_text(self):
        find_str = simpledialog.askstring("Replace", "Enter text to find:")
        if find_str:
            replace_str = simpledialog.askstring("Replace", f"Replace '{find_str}' with:")
            if replace_str:
                self.textarea.replace(tk.SEL_FIRST, tk.SEL_LAST, replace_str)

    def select_all(self):
        self.textarea.tag_add(tk.SEL, "1.0", tk.END)
        self.textarea.mark_set(tk.INSERT, "1.0")
        self.textarea.see(tk.INSERT)
        return 'break'

    def change_font(self):
        font = simpledialog.askstring("Font", "Enter font name (e.g., Arial):", initialvalue=self.textarea.cget("font"))
        if font:
            size = simpledialog.askinteger("Font Size", "Enter font size:", initialvalue=int(self.textarea.cget("size")))
            if size:
                self.textarea.config(font=(font, size))

if __name__ == "__main__":
    root = tk.Tk()
    app = NotepadApp(root)
    root.mainloop()
