import random
import tkinter as tk
from tkinter import messagebox, scrolledtext

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def xgcd(a, b):
    x, old_x = 0, 1
    y, old_y = 1, 0
    while b != 0:
        quotient = a // b
        a, b = b, a - quotient * b
        old_x, x = x, old_x - quotient * x
        old_y, y = y, old_y - quotient * y
    return a, old_x, old_y

def mod_pow(base, exponent, mod):
    result = 1
    base %= mod
    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % mod
        exponent //= 2
        base = (base * base) % mod
    return result

def choose_keys():
    with open('primes-to-100k.txt', 'r') as f:
        primes = list(map(int, f.read().splitlines()))
    filtered_primes = [p for p in primes if p >= 17]
    while True:
        p = random.choice(filtered_primes)
        q = random.choice(filtered_primes)
        if p != q:
            n = p * q
            if n >= 256:
                break
    phi = (p - 1) * (q - 1)
    while True:
        e = random.randrange(2, phi)
        if gcd(e, phi) == 1:
            break
    _, d, _ = xgcd(e, phi)
    if d < 0:
        d += phi
    return p, q, n, phi, e, d

def encrypt_char(char, e, n):
    return mod_pow(ord(char), e, n)

def decrypt_char(cipher, d, n):
    return chr(mod_pow(cipher, d, n))

class RSAApp:
    def __init__(self, root):
        self.root = root
        self.root.title("RSA Encrypt/Decrypt")
        self.p, self.q, self.n, self.phi, self.e, self.d = choose_keys()

        # Title
        tk.Label(root, text="RSA Encryption and Decryption", font=('Arial', 14, 'bold')).pack(pady=10)
	
	# Show key info
        tk.Button(root, text="Show Key Details", command=self.show_keys).pack()

        # Input message
        tk.Label(root, text="Enter message to encrypt:").pack()
        self.message_entry = tk.Entry(root, width=50)
        self.message_entry.pack(pady=5)

        # Encrypt button
        tk.Button(root, text="Encrypt", command=self.encrypt_message).pack(pady=5)

        # Encrypted output
        tk.Label(root, text="Encrypted message (as list of integers):").pack()
        self.encrypted_box = scrolledtext.ScrolledText(root, height=4, width=60)
        self.encrypted_box.pack(pady=5)

        # Decrypt button
        tk.Button(root, text="Decrypt", command=self.decrypt_message).pack(pady=5)

        # Decrypted output
        tk.Label(root, text="Decrypted message:").pack()
        self.decrypted_label = tk.Label(root, text="", font=('Arial', 12, 'bold'))
        self.decrypted_label.pack(pady=10)

        

    def encrypt_message(self):
        msg = self.message_entry.get()
        if not msg:
            messagebox.showwarning("Input Error", "Please enter a message to encrypt.")
            return
        self.encrypted = [encrypt_char(c, self.e, self.n) for c in msg]
        self.encrypted_box.delete("1.0", tk.END)
        self.encrypted_box.insert(tk.END, str(self.encrypted))

    def decrypt_message(self):
        if not hasattr(self, 'encrypted') or not self.encrypted:
            messagebox.showerror("Decryption Error", "No encrypted message found.")
            return
        decrypted = ''.join([decrypt_char(val, self.d, self.n) for val in self.encrypted])
        self.decrypted_label.config(text=decrypted)

    def show_keys(self):
        key_info = (
            f"p = {self.p}\n"
            f"q = {self.q}\n"
            f"n = {self.n}\n"
            f"phi = {self.phi}\n"
            f"e = {self.e}\n"
            f"d = {self.d}"
        )
        messagebox.showinfo("RSA Key Details", key_info)

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = RSAApp(root)
    root.mainloop()

