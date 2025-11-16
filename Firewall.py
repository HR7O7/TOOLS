import tkinter as tk
from tkinter import messagebox
import subprocess

def block_port():
    port = port_entry.get()
    if port.isdigit():
        cmd = ["sudo", "ufw", "deny", f"{port}/tcp"]
        run_cmd(cmd, f"Blocked TCP port {port}")
    else:
        messagebox.showerror("Error", "Please enter a valid port number.")

def unblock_port():
    port = port_entry.get()
    if port.isdigit():
        cmd = ["sudo", "ufw", "delete", "deny", f"{port}/tcp"]
        run_cmd(cmd, f"Unblocked TCP port {port}")
    else:
        messagebox.showerror("Error", "Please enter a valid port number.")

def show_rules():
    try:
        output = subprocess.check_output(["sudo", "ufw", "status"], universal_newlines=True)
        rules_text.delete("1.0", tk.END)
        rules_text.insert(tk.END, output)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to get firewall status.\n{e}")

def run_cmd(cmd, success_msg):
    try:
        subprocess.run(cmd, check=True)
        messagebox.showinfo("Success", success_msg)
        show_rules()
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Command failed:\n{e}")

# --- GUI Setup ---
root = tk.Tk()
root.title("Simple Firewall GUI")

tk.Label(root, text="Enter TCP Port:").pack(pady=5)
port_entry = tk.Entry(root)
port_entry.pack(pady=5)

tk.Button(root, text="Block Port", command=block_port).pack(pady=5)
tk.Button(root, text="Unblock Port", command=unblock_port).pack(pady=5)
tk.Button(root, text="Show Current Rules", command=show_rules).pack(pady=5)

rules_text = tk.Text(root, height=10, width=50)
rules_text.pack(pady=10)

root.mainloop()

