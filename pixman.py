import numpy as np
from PIL import Image
import argparse
import os

def rotate_left(x, n):
    return ((x << n) | (x >> (8 - n))) & 0xFF

def rotate_right(x, n):
    return ((x >> n) | (x << (8 - n))) & 0xFF

def encrypt(image_path,key,output_path):
    photo=Image.open(image_path).convert("RGB")
    image_array=np.array(photo).astype(np.int32)

    vectorized_rotate_left = np.vectorize(rotate_left)
    image_array = vectorized_rotate_left(image_array, 2)

    key = key % 256
    image_array=image_array ^ key
    image_array=(image_array * 2)%256
    
    image_array = (image_array + key) % 256
    image_array = image_array ^ ((key << 5) & 0xFF)
  
    
    image_array = np.clip(image_array, 0, 255).astype(np.uint8)    
    encrypt_image=Image.fromarray(image_array)
    encrypt_image.save(output_path,format="PNG")
    encrypt_image.show()

def decrypt(image_path,key,output_path):
    photo=Image.open(image_path).convert("RGB")
    image_array=np.array(photo).astype(np.int32)
    
    key=key % 256
    image_array = image_array ^ ((key << 5) & 0xFF)
    image_array = (image_array - key) % 256
    image_array = (image_array // 2 )%256
    image_array=image_array ^ key

    vectorized_rotate_right = np.vectorize(rotate_right)
    image_array = vectorized_rotate_right(image_array, 2)
    
    image_array = np.clip(image_array, 0, 255).astype(np.uint8)
    decrypt_image=Image.fromarray(image_array)
    decrypt_image.save(output_path,format="PNG")
    decrypt_image.show()

def print_banner():
    print(r"""
██████╗ ██╗██╗   ██╗███╗   ███╗  █████╗ ███╗   ██╗
██╔══██╗██║ ██║ ██╔╝████╗ ████║ ██╔══██╗████╗  ██║
██████╔╝██║  ████╔╝ ██╔████╔██║ ███████║██╔██╗ ██║
██╔═══╝ ██║ ██  ██╗ ██║╚██╔╝██║ ██╔══██║██║╚██╗██║
██║     ██║██║   ██╗██║ ╚═╝ ██║ ██║  ██║██║ ╚████║
╚═╝     ╚═╝╚═╝   ╚═╝╚═╝     ╚═╝ ╚═╝  ╚═╝╚═╝   ╚══╝  

              PIXMan — Image Encryptor and Decryptor tool 
              """)


def main():
    print_banner()
    parser = argparse.ArgumentParser(description="PIXMan: Image Encryption/Decryption Tool")
    parser.add_argument("operation",choices=["encrypt","decrypt"],help="choose the operation: encrypt or decrypt")
    parser.add_argument("input",help="Input image file path")
    parser.add_argument("output",help="Output image file path")
    parser.add_argument("key",type=int,help="Encryption/Decryption key (integer value)")
    args = parser.parse_args()

    if not os.path.exists(args.input):
        raise FileNotFoundError(f"Error: File {args.input} does not exist.")
    if os.path.exists(args.output):
        print(f"Warning: {args.output} already exists.")
        exit(1)
    if args.key < 0:
        raise ValueError("Error: Key must be a non-negative integer.")
    if args.operation=="encrypt":
        encrypt(args.input,args.key,args.output)
    elif args.operation=="decrypt":
        decrypt(args.input,args.key,args.output)

if __name__=="__main__":
    main()
