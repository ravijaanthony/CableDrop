# CableDrop - iOS to Windows Photo Transfer

A simple, offline web-based tool to transfer photos from an iOS device to a Windows PC via USB connection.

## Features

✅ **Entirely Offline** - USB transfers only, no internet required  
✅ **No Installation** - Single `.exe` file, just click and run  
✅ **Web-Based UI** - Runs on localhost inside the `.exe`  
✅ **Simple & Fast** - Designed for non-technical users

## Project Structure

```
FileTransfer/
├── app.py                 # Flask backend server
├── Home.html             # Web UI
├── Home.js               # Frontend logic (API calls)
├── Home.css              # Styling
├── requirements.txt      # Python dependencies
├── build.sh              # Build script for .exe
└── README.md            # This file
```

## Development Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Installation

1. **Install dependencies:**
   ```bash
   pip3 install -r requirements.txt
   ```

2. **Run locally for testing:**
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

## Building the .exe

### On Windows:
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

### On Linux/Mac:
```bash
# Use the provided build script
./build.sh
```

The `.exe` will be in the `dist/` folder.

## Distribution

Once built:
1. Share `dist/CableDrop.exe` with users
2. They can download and run it directly - no installation needed
3. No Python required on their machine

## API Endpoints

- **POST `/api/select-destination`** - Set the backup folder path
- **POST `/api/transfer-files`** - Transfer selected photos
- **GET `/`** - Serve the web UI

## Troubleshooting

### Flask server won't start
- Make sure port 5000 is not in use: `lsof -i :5000`
- Kill the process if needed: `kill -9 <PID>`

### Build fails with file not found
- Make sure you're in the `FileTransfer/` directory
- Check that `Home.html`, `Home.js`, `Home.css` exist

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

## License

Personal project - Free to use

## Support

For issues, check:
1. Flask is running: `python3 app.py`
2. Browser can reach: `http://localhost:5000`
3. iPhone is connected and trusted
4. Destination folder path is correct
