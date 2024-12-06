import pyzipper 
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
import sys
import time
import threading

# Static ASCII banner for "ZIP RIP"
ascii_banner = r"""
   ___________________    _____  ____  _____________._____________ 
  \_   ___ \______   \  /  _  \ \   \/  /\____    /|   \______   \
  /    \  \/|       _/ /  /_\  \ \     /   /     / |   ||     ___/
  \     \___|    |   \/    |    \/     \  /     /_ |   ||    |    
   \______  /____|_  /\____|__  /___/\  \/_______ \|___||____|    
          \/       \/         \/      \_/        \/           

                          A GRP UTILITY
"""

# Global counter for passwords attempted
password_attempts = 0
found_password = False
password_lock = threading.Lock()

# Function to display the banner
def display_banner():
    os.system("cls" if os.name == "nt" else "clear")  # Clear the terminal
    print(ascii_banner)

# Function to extract files from a PKZIP-encrypted file
def extract_file(zname, password):
    global password_attempts, found_password

    # Exit early if the password is already found
    if found_password:
        return

    try:
        # Attempt to extract using the given password
        with pyzipper.AESZipFile(zname) as zip_file:
            zip_file.pwd = password.encode('utf-8')
            zip_file.extractall()
        with password_lock:
            if not found_password:
                found_password = True
                print(f'\n[+] Found password: {password}\n')
                os._exit(0)  # Exit immediately once the password is found
    except (RuntimeError, pyzipper.BadZipFile):
        with password_lock:
            password_attempts += 1

# Function to display progress updates
def display_progress(total_passwords):
    global password_attempts, found_password
    while not found_password:
        with password_lock:
            progress = (password_attempts / total_passwords) * 100
        sys.stdout.write(f"\r[INFO] Progress: {password_attempts}/{total_passwords} passwords tried ({progress:.2f}%)")
        sys.stdout.flush()
        time.sleep(0.5)  # Update every 0.5 seconds

def main(zname, dname, max_threads=10):
    global password_attempts, found_password

    # Display the banner
    display_banner()

    # Read dictionary file efficiently
    try:
        with open(dname, 'r', encoding='utf-8', errors='ignore') as pass_file:
            passwords = [line.strip() for line in pass_file]
    except FileNotFoundError:
        print(f"[-] Dictionary file '{dname}' not found.")
        return

    total_passwords = len(passwords)
    print(f"[+] Loaded {total_passwords} passwords from dictionary file.")

    # Start a thread to display the progress bar
    progress_thread = threading.Thread(target=display_progress, args=(total_passwords,), daemon=True)
    progress_thread.start()

    # Use ThreadPoolExecutor for managing threads
    with ThreadPoolExecutor(max_threads) as executor:
        futures = [executor.submit(extract_file, zname, password) for password in passwords]

        # Wait for the threads to complete or for the password to be found
        for future in as_completed(futures):
            if found_password:
                break

    if not found_password:
        print("\n[-] Password not found. Try another dictionary.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(usage='zip_crack.py ZIPFILE DICTFILE')
    parser.add_argument('zipfile', type=str, metavar='ZIPFILE',
                        help='Specify the ZIP file to crack.')
    parser.add_argument('dictfile', type=str, metavar='DICTFILE',
                        help='Specify the dictionary file.')
    parser.add_argument('--threads', type=int, default=10,
                        help='Specify the maximum number of threads (default: 10).')
    args = parser.parse_args()
    main(args.zipfile, args.dictfile, args.threads)
