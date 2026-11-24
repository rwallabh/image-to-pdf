import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import os


def convert_images_to_pdf(image_paths, output_pdf_path):
    """Core function to convert images to PDF."""
    try:
        first_image = Image.open(image_paths[0]).convert('RGB')
        image_list = []
        for path in image_paths[1:]:
            img = Image.open(path).convert('RGB')
            image_list.append(img)
        first_image.save(output_pdf_path, save_all=True, append_images=image_list)
        return True, "PDF created successfully!"
    except Exception as e:
        return False, f"An error occurred: {str(e)}"


class ImageToPdfApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image to PDF Converter")
        # Slightly increased height to accommodate the new button
        self.root.geometry("550x450")
        self.root.eval('tk::PlaceWindow . center')

        self.selected_files = []

        # Instructions label
        self.label = tk.Label(root, text="1. Select, arrange, or remove images:")
        self.label.pack(pady=(15, 5))

        # Select button
        self.btn_select = tk.Button(root, text="Browse Images", command=self.select_images)
        self.btn_select.pack()

        # --- Listbox and Control Buttons Frame ---
        self.frame = tk.Frame(root)
        self.frame.pack(pady=15)

        # Listbox
        self.listbox = tk.Listbox(self.frame, width=50, height=12, selectmode=tk.SINGLE)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH)

        # Scrollbar for Listbox
        self.scrollbar = tk.Scrollbar(self.frame, orient="vertical")
        self.scrollbar.config(command=self.listbox.yview)
        self.scrollbar.pack(side=tk.LEFT, fill="y")
        self.listbox.config(yscrollcommand=self.scrollbar.set)

        # Control buttons frame
        self.btn_frame = tk.Frame(self.frame)
        self.btn_frame.pack(side=tk.LEFT, padx=10)

        self.btn_up = tk.Button(self.btn_frame, text="Move Up ▲", command=self.move_up, width=12)
        self.btn_up.pack(pady=5)

        self.btn_down = tk.Button(self.btn_frame, text="Move Down ▼", command=self.move_down, width=12)
        self.btn_down.pack(pady=5)

        # Remove button
        self.btn_remove = tk.Button(self.btn_frame, text="Remove ❌", command=self.remove_selected, width=12)
        self.btn_remove.pack(pady=(15, 5))

        # Clear All button
        self.btn_clear = tk.Button(self.btn_frame, text="Clear All 🗑️", command=self.clear_all, width=12, fg="red")
        self.btn_clear.pack(pady=5)

        # Convert button
        self.btn_convert = tk.Button(root, text="2. Save as PDF", command=self.convert_to_pdf, state=tk.DISABLED,
                                     bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
        self.btn_convert.pack(pady=10)

    def select_images(self):
        filetypes = (('Image files', '*.jpg *.jpeg *.png *.bmp *.tiff'), ('All files', '*.*'))
        filenames = filedialog.askopenfilenames(title='Select Images', filetypes=filetypes)

        if filenames:
            for f in filenames:
                self.selected_files.append(f)
                self.listbox.insert(tk.END, os.path.basename(f))
            self.btn_convert.config(state=tk.NORMAL)

    def move_up(self):
        selection = self.listbox.curselection()
        if not selection:
            return
        idx = selection[0]
        if idx > 0:
            self.selected_files[idx - 1], self.selected_files[idx] = self.selected_files[idx], self.selected_files[
                idx - 1]
            text = self.listbox.get(idx)
            self.listbox.delete(idx)
            self.listbox.insert(idx - 1, text)
            self.listbox.selection_set(idx - 1)

    def move_down(self):
        selection = self.listbox.curselection()
        if not selection:
            return
        idx = selection[0]
        if idx < self.listbox.size() - 1:
            self.selected_files[idx + 1], self.selected_files[idx] = self.selected_files[idx], self.selected_files[
                idx + 1]
            text = self.listbox.get(idx)
            self.listbox.delete(idx)
            self.listbox.insert(idx + 1, text)
            self.listbox.selection_set(idx + 1)

    def remove_selected(self):
        selection = self.listbox.curselection()
        if not selection:
            return
        idx = selection[0]

        self.listbox.delete(idx)
        self.selected_files.pop(idx)

        if not self.selected_files:
            self.btn_convert.config(state=tk.DISABLED)
        else:
            next_idx = min(idx, self.listbox.size() - 1)
            self.listbox.selection_set(next_idx)

    def clear_all(self):
        """Empties the listbox and backend array completely."""
        self.selected_files.clear()
        self.listbox.delete(0, tk.END)
        self.btn_convert.config(state=tk.DISABLED)

    def convert_to_pdf(self):
        if not self.selected_files:
            return

        output_file = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            title="Save PDF as..."
        )

        if output_file:
            success, message = convert_images_to_pdf(self.selected_files, output_file)
            if success:
                messagebox.showinfo("Success", message)
                self.clear_all()  # Reuse the clear_all function to reset the UI
            else:
                messagebox.showerror("Error", message)


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageToPdfApp(root)
    root.mainloop()