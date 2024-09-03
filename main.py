import tkinter as tk
from tkinter import messagebox, filedialog
import qrcode
from io import BytesIO
from PIL import Image, ImageTk
import sys


class QRCodeGeneratorApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("QR Code Generator")
        self.setup_ui()

    def setup_ui(self):
        self.center_window(400, 450)

        tk.Label(self.root, text="Enter the text").pack(pady=5)
        self.text_entry = tk.Entry(self.root, justify='center', width=30)
        self.text_entry.pack(pady=5, padx=10)

        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=5)

        tk.Button(button_frame, text="Generate", command=self.generate_qr_code).grid(
            row=0, column=0, padx=10)
        self.save_button = tk.Button(
            button_frame, text="Save", command=self.save_image, state=tk.DISABLED)
        self.save_button.grid(row=0, column=1, padx=10)

        self.image_place = tk.Label(self.root)
        self.image_place.pack(pady=5)

    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        self.root.update_idletasks()

    def generate_qr_code(self):
        txt = self.text_entry.get().strip()
        if not txt:
            messagebox.showwarning(
                "Input Error", "Please enter text to generate a QR code.")
            return

        try:
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(txt)
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white")
            img = img.resize((300, 300), Image.LANCZOS)

            self.qr_image = ImageTk.PhotoImage(img)
            self.image_place.config(image=self.qr_image)
            self.save_button.config(state=tk.NORMAL)
        except Exception as e:
            messagebox.showerror(
                "Error", f"Failed to generate QR code: {str(e)}")

    def save_image(self):
        file_types = [("PNG files", "*.png")]
        default_extension = ".png"

        # Add Mac-specific file type if running on macOS
        if sys.platform == "darwin":
            file_types.append(("macOS Icon", "*.icns"))

        file_path = filedialog.asksaveasfilename(
            defaultextension=default_extension,
            filetypes=file_types
        )

        if file_path:
            try:
                img = ImageTk.getimage(self.qr_image)

                # Handle macOS icon format
                if file_path.lower().endswith('.icns') and sys.platform == "darwin":
                    self.save_as_icns(img, file_path)
                else:
                    img.save(file_path)

                messagebox.showinfo("Success", "QR code saved successfully!")
            except Exception as e:
                messagebox.showerror(
                    "Error", f"Failed to save QR code: {str(e)}")

    def save_as_icns(self, image, file_path):
        # This is a placeholder for ICNS conversion
        # In a real implementation, you'd use a library like iconforge or a custom ICNS creation method
        messagebox.showinfo(
            "Info", "ICNS conversion is not implemented in this demo. Saving as PNG instead.")
        image.save(file_path.rsplit('.', 1)[0] + '.png')


if __name__ == "__main__":
    root = tk.Tk()
    app = QRCodeGeneratorApp(root)
    root.mainloop()
