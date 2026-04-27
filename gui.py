import os
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from file_manager import FileManager
from cloud_manager import CloudManager


class SmartDiskCleanerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Disk Cleaner - Made by Sultan Aljedani")
        self.root.geometry("1150x720")
        self.root.configure(bg="#f8fafc")

        self.file_manager = None
        self.cloud_manager = CloudManager()
        self.current_folder = ""
        self.path_map = {}

        self.build_ui()

    # ---------------- UI ---------------- #

    def build_ui(self):
        top = tk.Frame(self.root, bg="#0f172a", height=70)
        top.pack(fill="x")

        title = tk.Label(
            top,
            text="Smart Disk Cleaner",
            font=("Segoe UI", 22, "bold"),
            fg="white",
            bg="#0f172a"
        )
        title.pack(side="left", padx=20, pady=15)

        author = tk.Label(
            top,
            text="Made by Sultan Aljidani",
            font=("Segoe UI", 10, "bold"),
            fg="#cbd5e1",
            bg="#0f172a"
        )
        author.pack(side="right", padx=20)

        toolbar = tk.Frame(self.root, bg="#f8fafc")
        toolbar.pack(fill="x", padx=15, pady=10)

        tk.Button(
            toolbar,
            text="📁 Select Folder",
            command=self.select_folder,
            bg="#2563eb",
            fg="white",
            relief="flat",
            font=("Segoe UI", 10, "bold"),
            padx=12,
            pady=8
        ).pack(side="left", padx=5)

        tk.Button(
            toolbar,
            text="❌ Exit",
            command=self.root.quit,
            bg="#ef4444",
            fg="white",
            relief="flat",
            font=("Segoe UI", 10, "bold"),
            padx=12,
            pady=8
        ).pack(side="right", padx=5)

        self.folder_label = tk.Label(
            self.root,
            text="No folder selected",
            bg="#f8fafc",
            fg="#475569",
            font=("Segoe UI", 11, "bold")
        )
        self.folder_label.pack(anchor="w", padx=20)

        self.instructions = tk.Label(
            self.root,
            text="Instructions: Click 'Select Folder' → choose a folder → select a file → right-click to show options.",
            bg="#f8fafc",
            fg="#64748b",
            font=("Segoe UI", 10)
        )
        self.instructions.pack(anchor="w", padx=20, pady=(0, 8))

        table_frame = tk.Frame(self.root, bg="#f8fafc")
        table_frame.pack(fill="both", expand=True, padx=15, pady=10)

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", rowheight=34, font=("Segoe UI", 10))
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))

        self.tree = ttk.Treeview(
            table_frame,
            columns=("name", "info"),
            show="headings"
        )

        self.tree.heading("name", text="File Name")
        self.tree.heading("info", text="Info")

        self.tree.column("name", width=760)
        self.tree.column("info", width=220, anchor="center")

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.tree.yview
        )

        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.tree.bind("<Button-3>", self.show_context_menu)
        self.tree.bind("<Double-1>", self.open_file)

        self.status = tk.Label(
            self.root,
            text="Ready | Made by Sultan Aljidani",
            bg="#e2e8f0",
            fg="#334155",
            anchor="w",
            padx=10,
            pady=8,
            font=("Segoe UI", 10, "bold")
        )
        self.status.pack(fill="x", side="bottom")

    # ---------------- Helpers ---------------- #

    def set_status(self, text):
        self.root.after(0, lambda: self.status.config(text=text))

    def clear_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.path_map = {}

    def get_selected_path(self):
        selected = self.tree.selection()
        if not selected:
            self.set_status("Please select a file first.")
            return None

        values = self.tree.item(selected[0], "values")
        return self.path_map.get(values[0])

    def run_in_thread(self, func):
        threading.Thread(target=func, daemon=True).start()

    # ---------------- Folder ---------------- #

    def select_folder(self):
        folder = filedialog.askdirectory()

        if folder:
            self.current_folder = folder
            self.file_manager = FileManager(folder)
            self.folder_label.config(
                text=f"Selected Folder: {os.path.basename(folder)}"
            )
            self.set_status("Folder selected successfully.")
            self.load_files()
        else:
            self.set_status("Folder selection canceled.")

    def load_files(self):
        def task():
            self.set_status("Loading files...")

            files = self.file_manager.get_all_files()
            self.root.after(0, self.clear_table)

            count = 0
            for file in files:
                try:
                    size = os.path.getsize(file)
                    name = os.path.basename(file)
                    size_mb = round(size / (1024 * 1024), 2)

                    self.path_map[name] = file
                    count += 1

                    self.root.after(
                        0,
                        lambda n=name, s=size_mb:
                        self.tree.insert("", "end", values=(n, f"{s} MB"))
                    )
                except:
                    pass

            self.set_status(f"{count} files loaded successfully.")

        self.run_in_thread(task)

    # ---------------- Menu ---------------- #

    def show_context_menu(self, event):
        item = self.tree.identify_row(event.y)

        if item:
            self.tree.selection_set(item)

        menu = tk.Menu(self.root, tearoff=0)

        menu.add_command(label="📊 Show Largest Files", command=self.show_largest)
        menu.add_command(label="🧬 Show Duplicate Files", command=self.show_duplicates)
        menu.add_separator()
        menu.add_command(label="☁ Upload to Cloud", command=self.upload_selected)
        menu.add_command(label="🗑 Delete File", command=self.delete_selected)
        menu.add_command(label="📋 Copy Path", command=self.copy_path)
        menu.add_command(label="📂 Open File", command=self.open_selected)

        menu.post(event.x_root, event.y_root)

    # ---------------- Actions ---------------- #

    def show_largest(self):
        if not self.file_manager:
            self.set_status("Please select a folder first.")
            return

        def task():
            self.set_status("Finding largest files...")

            files = self.file_manager.get_all_files()
            data = []

            for file in files:
                try:
                    size = os.path.getsize(file)
                    data.append((file, size))
                except:
                    pass

            data.sort(key=lambda x: x[1], reverse=True)

            self.root.after(0, self.clear_table)

            for file, size in data[:100]:
                name = os.path.basename(file)
                size_mb = round(size / (1024 * 1024), 2)
                self.path_map[name] = file

                self.root.after(
                    0,
                    lambda n=name, s=size_mb:
                    self.tree.insert("", "end", values=(n, f"{s} MB"))
                )

            self.set_status("Largest files displayed successfully.")

        self.run_in_thread(task)

    def show_duplicates(self):
        if not self.file_manager:
            self.set_status("Please select a folder first.")
            return

        def task():
            self.set_status("Scanning duplicates...")

            files = self.file_manager.get_all_files()
            hashes = {}
            found = 0

            self.root.after(0, self.clear_table)

            for file in files:
                file_hash = self.file_manager.get_file_hash(file)

                if not file_hash:
                    continue

                if file_hash in hashes:
                    name = os.path.basename(file)
                    self.path_map[name] = file
                    found += 1

                    self.root.after(
                        0,
                        lambda n=name:
                        self.tree.insert("", "end", values=(n, "Duplicate"))
                    )
                else:
                    hashes[file_hash] = file

            self.set_status(f"Duplicate scan completed. {found} duplicates found.")

        self.run_in_thread(task)

    def delete_selected(self):
        path = self.get_selected_path()
        if not path:
            return

        confirm = messagebox.askyesno("Delete File", "Are you sure you want to delete this file?")

        if confirm:
            try:
                os.remove(path)
                self.set_status("File deleted successfully.")
                self.load_files()
            except Exception as e:
                self.set_status(f"Delete failed: {e}")
        else:
            self.set_status("Delete canceled.")

    def upload_selected(self):
        path = self.get_selected_path()
        if not path:
            return

        def task():
            self.set_status("Uploading file to cloud...")

            try:
                self.cloud_manager.upload_and_delete(path)
                self.set_status("File uploaded successfully and deleted locally.")
                self.load_files()
            except Exception as e:
                self.set_status(f"Upload failed: {e}")

        self.run_in_thread(task)

    def copy_path(self):
        path = self.get_selected_path()
        if not path:
            return

        self.root.clipboard_clear()
        self.root.clipboard_append(path)
        self.set_status("Path copied successfully.")

    def open_selected(self):
        path = self.get_selected_path()
        if not path:
            return

        try:
            os.startfile(path)
            self.set_status("File opened successfully.")
        except Exception as e:
            self.set_status(f"Open failed: {e}")

    def open_file(self, event):
        self.open_selected()


if __name__ == "__main__":
    root = tk.Tk()
    app = SmartDiskCleanerGUI(root)
    root.mainloop()