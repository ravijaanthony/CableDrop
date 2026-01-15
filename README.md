# CableDrop - iOS to Windows Photo Transfer

A simple, offline web-based tool to transfer photos from an iOS device to a Windows PC via USB connection.

## Features

✅ **Entirely Offline** - USB transfers only, no internet required  
✅ **No Installation** - Single `.exe` file (Windows) or standalone app (Mac), just click and run  
✅ **Web-Based UI** - Runs on localhost inside the app  
✅ **Simple & Fast** - Designed for non-technical users

## Project Structure

```
FileTransfer/
├── app.py                 # Flask backend server
├── Home.html             # Web UI
├── Home.js               # Frontend logic (API calls)
├── Home.css              # Styling
├── requirements.txt      # Python dependencies
├── build.sh              # Build script for .exe/.app
└── README.md            # This file
```

## Development Setup

### Prerequisites

#### On Windows:
- Python 3.8+ (download from [python.org](https://python.org))
- pip (comes with Python)

#### On Mac:
- Python 3.8+ (install via Homebrew or [python.org](https://python.org))
  ```bash
  # Using Homebrew (recommended)
  brew install python3
  
  # Or download from python.org
  ```
- pip (comes with Python)

#### On Linux:
- Python 3.8+
- pip

### Installation

#### Step 1: Install Python (Mac only if not installed)
```bash
# Check if Python 3 is installed
python3 --version

# If not, install via Homebrew
brew install python3
```

#### Step 2: Install Dependencies
```bash
# Windows, Mac, or Linux - same command
pip3 install -r requirements.txt
```

**Note:** On Mac, you might need to use `pip3` instead of `pip` depending on your Python installation.

#### Step 3: Run locally for testing
```bash
python3 app.py
```

This will:
- Start Flask server on `http://localhost:5000`
- Open your browser automatically
- Show the CableDrop UI

## How It Works

### Step 1: Select Destination
- Click "📂 Select PC Backup Folder"
- Enter a folder path on your Windows PC (e.g., `C:\Users\YourName\Pictures`)
- Folder will be validated and set as destination

### Step 2: Transfer Photos
- Plug your iPhone into Windows via USB
- In file explorer, navigate to: `This PC > Apple iPhone > Internal Storage > DCIM`
- Click "📸 Select Photos" in CableDrop
- Select photos you want to transfer
- Transfer begins automatically

## Building Standalone Apps

### On Windows (creates .exe)
```bash
# Install PyInstaller first (if not done)
pip install pyinstaller==6.18.0

# Build executable
pyinstaller --onefile --windowed ^
  --add-data "Home.html;." ^
  --add-data "Home.js;." ^
  --add-data "Home.css;." ^
  --name CableDrop ^
  app.py
```

The `.exe` will be in the `dist/` folder.

### On Mac (creates .app)
```bash
# Install PyInstaller first (if not done)
pip3 install pyinstaller==6.18.0

# Build macOS app
pyinstaller --onefile --windowed \
  --add-data "Home.html:." \
  --add-data "Home.js:." \
  --add-data "Home.css:." \
  --name CableDrop \
  app.py
```

The `.app` will be in the `dist/` folder. You can:
- Double-click to run
- Move to Applications folder
- Create an alias on your desktop

### On Linux/Mac (using build script)
```bash
# Make script executable (first time only)
chmod +x build.sh

# Run build script
./build.sh
```

## Distribution

### Windows Users:
1. Share `dist/CableDrop.exe`
2. They can download and run it directly - no installation needed
3. No Python required on their machine

### Mac Users:
1. Share `dist/CableDrop.app`
2. They can download and double-click to run
3. No Python required on their machine
4. May need to allow execution: Right-click → Open (first time)

## API Endpoints

- **POST `/api/select-destination`** - Set the backup folder path
- **POST `/api/transfer-files`** - Transfer selected photos
- **GET `/`** - Serve the web UI

## Troubleshooting

### Flask server won't start
**Windows:**
```bash
# Check what's using port 5000
netstat -ano | findstr :5000

# Kill the process
taskkill /PID <PID> /F
```

**Mac/Linux:**
```bash
# Check what's using port 5000
lsof -i :5000

# Kill the process
kill -9 <PID>
```

### Python/pip not found on Mac
```bash
# Check your Python version
python3 --version

# Reinstall Python
brew reinstall python3

# Verify pip
pip3 --version
```

### Build fails with "file not found"
- Make sure you're in the `FileTransfer/` directory
- Check that `Home.html`, `Home.js`, `Home.css` exist
- Use `ls` (Mac/Linux) or `dir` (Windows) to verify

### iPhone not showing in File Explorer
- Try a different USB cable
- Make sure "Trust This Computer" is selected on iPhone
- Restart File Explorer: Press Win+I, Settings > Files > Show recently used files

## Future Improvements

- [ ] Better folder selection UI (native file dialog)
- [ ] iOS device auto-detection via libmtp
- [ ] Progress bar for large transfers
- [ ] Batch operations (duplicate handling)
- [ ] Dark mode theme
- [ ] Support for macOS native file dialog

## License

Personal project - Free to use

## Support

For issues, check:
1. Flask is running: `python3 app.py`
2. Browser can reach: `http://localhost:5000`
3. iPhone is connected and trusted
4. Destination folder path is correct
5. Python version is 3.8+: `python3 --version`
