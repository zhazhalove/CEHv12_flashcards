import json
import tkinter as tk
from tkinter import filedialog, messagebox

class FlashCardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Flashcard Viewer")

        self.flashcard_groups = {}
        self.current_group = None
        self.flashcards = []
        self.current_index = 0
        self.showing_back = False

        self.group_selector = tk.Listbox(self.root, height=5)
        self.group_selector.pack(fill="x", padx=10, pady=5)
        self.group_selector.bind("<<ListboxSelect>>", self.select_group)

        self.card_frame = tk.Frame(
            self.root, relief="raised", bd=4, bg="white"
        )
        self.card_frame.pack(expand=True, fill="both", padx=20, pady=20)

        self.card_label = tk.Label(
            self.card_frame, text="Load a JSON file to begin", font=("Arial", 20), wraplength=400, justify="center", bg="white"
        )
        self.card_label.pack(expand=True, fill="both", padx=10, pady=10)

        self.next_button = tk.Button(
            self.root, text="Next", command=self.next_card, state="disabled"
        )
        self.next_button.pack(side="right", padx=10, pady=10)

        self.prev_button = tk.Button(
            self.root, text="Previous", command=self.prev_card, state="disabled"
        )
        self.prev_button.pack(side="left", padx=10, pady=10)

        self.card_label.bind("<Button-1>", self.flip_card)

        menu_bar = tk.Menu(self.root)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Load JSON", command=self.load_json)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

        self.root.config(menu=menu_bar)

    def load_json(self):
        file_path = filedialog.askopenfilename(
            title="Select a Flashcard JSON File",
            filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")]
        )

        if not file_path:
            return

        try:
            with open(file_path, "r") as file:
                self.flashcard_groups = json.load(file)

            if not self.flashcard_groups:
                raise ValueError("The JSON file is empty or invalid.")

            self.group_selector.delete(0, tk.END)
            for group in self.flashcard_groups.keys():
                self.group_selector.insert(tk.END, group)

            self.flashcards = []
            self.current_group = None
            self.current_index = 0
            self.showing_back = False
            self.card_label.config(text="Select a group to begin")
            self.next_button["state"] = "disabled"
            self.prev_button["state"] = "disabled"

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load JSON file: {e}")

    def select_group(self, event):
        selection = self.group_selector.curselection()
        if selection:
            group_name = self.group_selector.get(selection[0])
            self.current_group = group_name
            self.flashcards = self.flashcard_groups[group_name]
            self.current_index = 0
            self.showing_back = False
            self.update_card()
            self.next_button["state"] = "normal"
            self.prev_button["state"] = "normal"

    def update_card(self):
        if self.flashcards:
            card = self.flashcards[self.current_index]
            if self.showing_back:
                self.card_label.config(text=card["Back"])
            else:
                self.card_label.config(text=card["Front"])

    def flip_card(self, event):
        if self.flashcards:
            self.showing_back = not self.showing_back
            self.update_card()

    def next_card(self):
        if self.flashcards:
            self.current_index = (self.current_index + 1) % len(self.flashcards)
            self.showing_back = False
            self.update_card()

    def prev_card(self):
        if self.flashcards:
            self.current_index = (self.current_index - 1) % len(self.flashcards)
            self.showing_back = False
            self.update_card()

if __name__ == "__main__":
    root = tk.Tk()
    app = FlashCardApp(root)
    root.mainloop()
