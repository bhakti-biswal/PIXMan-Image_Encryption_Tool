import argparse
from PIL import Image
from cryptography.fernet import Fernet

# ---------------- AES Wrappers ----------------
def load_key(keyfile):
    with open(keyfile, "rb") as f:
        return f.read()

def save_key(keyfile):
    key = Fernet.generate_key()
    with open(keyfile, "wb") as f:
        f.write(key)
    print(f"[+] Key saved in {keyfile}")
    return key

def encrypt_data(data, key):
    return Fernet(key).encrypt(data)

def decrypt_data(data, key):
    return Fernet(key).decrypt(data)

# ---------------- Steganography ----------------
def encode_message(image_path, message_bytes, output_path):
    img = Image.open(image_path)
    encoded = img.copy()
    width, height = img.size
    index = 0

    bits = ''.join(format(byte, '08b') for byte in message_bytes) + "1111111111111110"

    for row in range(height):
        for col in range(width):
            pixel = list(img.getpixel((col, row)))
            for n in range(3):  # RGB
                if index < len(bits):
                    pixel[n] = pixel[n] & ~1 | int(bits[index])
                    index += 1
            encoded.putpixel((col, row), tuple(pixel))

    encoded.save(output_path)
    print(f"[+] Hidden message inside {output_path}")

def decode_message(image_path):
    img = Image.open(image_path)
    width, height = img.size
    bits = ""

    for row in range(height):
        for col in range(width):
            pixel = list(img.getpixel((col, row)))
            for n in range(3):
                bits += str(pixel[n] & 1)

    all_bytes = [bits[i:i+8] for i in range(0, len(bits), 8)]
    data = bytearray()
    for byte in all_bytes:
        if byte == "11111110":
            break
        data.append(int(byte, 2))

    return bytes(data)

# ---------------- Encrypt Flow ----------------
def encrypt_flow(text, input_img, output_file, keyfile):
    # Load/generate key
    try:
        key = load_key(keyfile)
    except FileNotFoundError:
        key = save_key(keyfile)

    # Step 1: Encrypt text
    encrypted_text = encrypt_data(text.encode(), key)

    # Step 2: Hide inside image
    encode_message(input_img, encrypted_text, "stego.png")

    # Step 3: Encrypt stego image
    with open("stego.png", "rb") as f:
        stego_bytes = f.read()
    encrypted_image = encrypt_data(stego_bytes, key)
    with open(output_file, "wb") as f:
        f.write(encrypted_image)

    print(f"[+] Final encrypted file saved as {output_file}")

# ---------------- Decrypt Flow ----------------
def decrypt_flow(input_file, output_text, keyfile):
    key = load_key(keyfile)

    # Step 1: Decrypt image
    with open(input_file, "rb") as f:
        encrypted_image = f.read()
    stego_bytes = decrypt_data(encrypted_image, key)
    with open("stego_decrypted.png", "wb") as f:
        f.write(stego_bytes)

    # Step 2: Extract hidden ciphertext
    hidden_data = decode_message("stego_decrypted.png")

    # Step 3: Decrypt hidden text
    decrypted_text = decrypt_data(hidden_data, key).decode()

    with open(output_text, "w") as f:
        f.write(decrypted_text)

    print(f"[+] Recovered secret text saved in {output_text}")

# ---------------- Main Parser ----------------
def main():
    print("""""
██████╗ ██╗██╗   ██╗███╗   ███╗  █████╗ ███╗   ██╗
██╔══██╗██║ ██║ ██╔╝████╗ ████║ ██╔══██╗████╗  ██║
██████╔╝██║  ████╔╝ ██╔████╔██║ ███████║██╔██╗ ██║
██╔═══╝ ██║ ██  ██╗ ██║╚██╔╝██║ ██╔══██║██║╚██╗██║
██║     ██║██║   ██╗██║ ╚═╝ ██║ ██║  ██║██║ ╚████║
╚═╝     ╚═╝╚═╝   ╚═╝╚═╝     ╚═╝ ╚═╝  ╚═╝╚═╝   ╚══╝  

              PIXMan — Image Encryptor and Decryptor tool 
              """)
    parser = argparse.ArgumentParser(description="AES + Stego Secure Tool")
    subparsers = parser.add_subparsers(dest="command")

    # Encrypt command
    enc_parser = subparsers.add_parser("encrypt", help="Encrypt text, hide in image, then encrypt image")
    enc_parser.add_argument("--text", required=True, help="Secret text to hide")
    enc_parser.add_argument("--input", required=True, help="Input image path")
    enc_parser.add_argument("--output", required=True, help="Final encrypted file path")
    enc_parser.add_argument("--key", required=True, help="Key file path")

    # Decrypt command
    dec_parser = subparsers.add_parser("decrypt", help="Decrypt image and extract hidden text")
    dec_parser.add_argument("--input", required=True, help="Final encrypted file path")
    dec_parser.add_argument("--output", required=True, help="Recovered text output file")
    dec_parser.add_argument("--key", required=True, help="Key file path")

    args = parser.parse_args()

    if args.command == "encrypt":
        encrypt_flow(args.text, args.input, args.output, args.key)
    elif args.command == "decrypt":
        decrypt_flow(args.input, args.output, args.key)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
