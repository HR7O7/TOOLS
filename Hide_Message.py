import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

def encode_message(img, msg):
    binary_msg = ''.join(format(ord(c), '08b') for c in msg) + '1111111111111110'
    img = img.convert('RGB')
    pixels = img.load()
    i = 0
    for y in range(img.height):
        for x in range(img.width):
            if i < len(binary_msg):
                r, g, b = pixels[x, y]
                r = (r & ~1) | int(binary_msg[i])
                i += 1
                if i < len(binary_msg):
                    g = (g & ~1) | int(binary_msg[i])
                    i += 1
                if i < len(binary_msg):
                    b = (b & ~1) | int(binary_msg[i])
                    i += 1
                pixels[x, y] = (r, g, b)
            else:
                return img
    return img

def decode_message(img):
    img = img.convert('RGB')
    pixels = img.load()
    binary_msg = ""
    for y in range(img.height):
        for x in range(img.width):
            for color in pixels[x, y]:
                binary_msg += str(color & 1)
    bytes_list = [binary_msg[i:i+8] for i in range(0, len(binary_msg), 8)]
    msg = ""
    for byte in bytes_list:
        if byte == '11111110':
            break
        msg += chr(int(byte, 2))
    return msg

class StegApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Steganography")
        self.root.geometry("500x500")

        self.image = None

        self.load_btn = tk.Button(root, text="Load Image", command=self.load_image)
        self.load_btn.pack(pady=10)

        self.encode_text = tk.Text(root, height=5, width=50)
        self.encode_text.pack()

        self.encode_btn = tk.Button(root, text="Encode & Save", command=self.encode_and_save)
        self.encode_btn.pack(pady=5)

        self.decode_btn = tk.Button(root, text="Decode Message", command=self.decode)
        self.decode_btn.pack(pady=5)

        self.output_label = tk.Label(root, text="", wraplength=400)
        self.output_label.pack(pady=10)

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("PNG Images", "*.png")])
        if file_path:
            self.image = Image.open(file_path)
            messagebox.showinfo("Image Loaded", f"Loaded image: {file_path}")

    def encode_and_save(self):
        if self.image is None:
            messagebox.showerror("Error", "Please load an image first.")
            return
        msg = self.encode_text.get("1.0", tk.END).strip()
        if not msg:
            messagebox.showerror("Error", "Please enter a message to encode.")
            return
        encoded_img = encode_message(self.image.copy(), msg)
        save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png")])
        if save_path:
            encoded_img.save(save_path)
            messagebox.showinfo("Success", f"Image saved with hidden message at:\n{save_path}")

    def decode(self):
        if self.image is None:
            messagebox.showerror("Error", "Please load an image first.")
            return
        decoded_msg = decode_message(self.image)
        self.output_label.config(text="Hidden message:\n" + decoded_msg)

if __name__ == "__main__":
    root = tk.Tk()
    app = StegApp(root)
    root.mainloop()