```
   ___________________    _____  ____  _____________._____________
  \_   ___ \______   \  /  _  \ \   \/  /\____    /|   \______   \
  /    \  \/|       _/ /  /_\  \ \     /   /     / |   ||     ___/
  \     \___|    |   \/    |    \/     \  /     /_ |   ||    |    
   \______  /____|_  /\____|__  /___/\  \/_______ \|___||____|    
          \/       \/         \/      \_/        \/            

                          A GRP UTILITY
```

# CRAXZIP (V1)
#### WORK IN PROGRESS

A Python-based brute-force tool for ZIP file password cracking. This utility supports both PKZIP and AES-encrypted ZIP files.

## Features

- Supports PKZIP and AES-encryption.
- Multi-threaded.
- (Ctrl+C) to exit. 

### Basic Usage

```bash
python grpcrack.py <ZIP_FILE> <DICTIONARY_FILE>
```

## Usage

1. **Basic Command**:
   ```bash
   python grpcrack.py example.zip passwords.txt
   ```

2. **Custom Threads**:
   Specify the number of threads for multi-threaded processing:
   ```bash
   python grpcrack.py example.zip /password/list/path --threads 8
   ```

3. **Interrupt the Process**:
   - Press `Ctrl+C` to stop the script gracefully.
   - The script will display the number of passwords attempted before stopping.

## Requirements

- Python 3.6+
- `pyzipper` 

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Disclaimer

This tool is intended for educational purposes and legitimate use only. The author is not responsible for any misuse of this tool.

