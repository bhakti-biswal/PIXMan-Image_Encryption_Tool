# PRODIGY_CS_02
# 🖼️ PIXMan — Image Encryption & Decryption Tool

A Python-based image encryption and decryption tool using pixel-level transformations. PIXMan is built using NumPy and PIL, and is perfect for experimenting with lightweight image-level cryptographic techniques.

---

## 🚀 Features

- 🔐 Encrypts images with a custom key
- 🔓 Decrypts images back to original using the same key
- 🧪 Simple CLI-based interface for quick use
- 📷 Supports RGB image formats (like PNG, JPEG, etc.)

---

## 🛠️ Requirements

- Python 3.x
- `numpy`
- `Pillow`

Install dependencies:
```bash
pip install numpy
pip install pillow
```

##🧠 Usage
🔹 Encrypt an image
```bash
python pixman.py encrypt input.png encrypted.png <key>
```
🔹 Decrypt the image
```bash
python pixman.py decrypt encrypted.png decrypted.png <key>
```
⚠️ Use the same key for encryption and decryption, or the output will be unreadable.

##🖥️ Example Output

```bash
██████╗ ██╗██╗   ██╗███╗   ███╗  █████╗ ███╗   ██╗
██╔══██╗██║ ██║ ██╔╝████╗ ████║ ██╔══██╗████╗  ██║
██████╔╝██║  ████╔╝ ██╔████╔██║ ███████║██╔██╗ ██║
██╔═══╝ ██║ ██  ██╗ ██║╚██╔╝██║ ██╔══██║██║╚██╗██║
██║     ██║██║   ██╗██║ ╚═╝ ██║ ██║  ██║██║ ╚████║
╚═╝     ╚═╝╚═╝   ╚═╝╚═╝     ╚═╝ ╚═╝  ╚═╝╚═╝   ╚══╝  

PIXMan — Image Encryptor and Decryptor tool
```

##📂 Directory Structure

```bash
├── pixman.py
├── input.png
├── encrypted.png
├── decrypted.png
└── README.md
```

##📄 License

This project is open-source under the MIT License.

##🤝 Contributing

Feel free to fork the repository, suggest improvements, or submit pull requests. Bug fixes and feature ideas are welcome!


