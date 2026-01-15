from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import os
import threading
import webbrowser
import time
import io
import zipfile
from datetime import datetime

app = Flask(__name__, template_folder='.', static_folder='.')
CORS(app)

# Store destination path
destination_folder = None

@app.route('/')
def index():
    return render_template('Home.html')

@app.route('/api/get-home-path', methods=['GET'])
def get_home_path():
    """Get the user's home directory path"""
    return jsonify({'home': os.path.expanduser('~')})

@app.route('/api/get-common-folders', methods=['GET'])
def get_common_folders():
    """Get common backup folders on the system"""
    folders = []
    home = os.path.expanduser('~')

    # Common backup locations
    common_paths = [
        ('Pictures', os.path.join(home, 'Pictures')),
        ('Documents', os.path.join(home, 'Documents')),
        ('Desktop', os.path.join(home, 'Desktop')),
        ('Downloads', os.path.join(home, 'Downloads')),
    ]

    for name, path in common_paths:
        if os.path.isdir(path):
            folders.append({
                'name': name,
                'path': path
            })

    return jsonify({'folders': folders})

@app.route('/api/select-destination', methods=['POST'])
def select_destination():
    global destination_folder
    data = request.json
    folder_path = data.get('path', '').strip()

    # Expand ~ to home directory
    if folder_path.startswith('~'):
        folder_path = os.path.expanduser(folder_path)

    # Make absolute path
    folder_path = os.path.abspath(folder_path)

    # Validate folder exists
    if not os.path.isdir(folder_path):
        return jsonify({'error': f'Folder not found: {folder_path}'}), 400

    # Check if we have write access
    if not os.access(folder_path, os.W_OK):
        return jsonify({'error': f'No write permission for: {folder_path}'}), 400

    destination_folder = folder_path
    return jsonify({
        'success': True,
        'path': folder_path,
        'name': os.path.basename(folder_path) or folder_path
    })

@app.route('/api/transfer-files', methods=['POST'])
def transfer_files():
    global destination_folder

    if not destination_folder:
        return jsonify({'error': 'Destination not selected'}), 400

    try:
        files = request.files.getlist('files')
        if not files:
            return jsonify({'error': 'No files to transfer'}), 400

        results = {
            'success': [],
            'failed': []
        }

        for file in files:
            try:
                filepath = os.path.join(destination_folder, file.filename)
                file.save(filepath)
                results['success'].append(file.filename)
            except Exception as e:
                results['failed'].append({
                    'filename': file.filename,
                    'error': str(e)
                })

        return jsonify({
            'success': True,
            'transferred': len(results['success']),
            'failed': len(results['failed']),
            'results': results
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/download-zip', methods=['POST'])
def download_zip():
    try:
        files = request.files.getlist('files')
        if not files:
            return jsonify({'error': 'No files to transfer'}), 400

        # Build zip in memory
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file in files:
                # Use basename only to avoid paths
                filename = os.path.basename(file.filename)
                if not filename:
                    continue
                zipf.writestr(filename, file.read())

        zip_buffer.seek(0)
        ts = datetime.now().strftime('%Y%m%d_%H%M%S')
        zip_name = f'CableDrop_{ts}.zip'

        return send_file(
            zip_buffer,
            mimetype='application/zip',
            as_attachment=True,
            download_name=zip_name
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    def open_browser():
        time.sleep(1)
        webbrowser.open('http://localhost:5000')

    thread = threading.Thread(target=open_browser, daemon=True)
    thread.start()

    app.run(debug=False, host='127.0.0.1', port=5000)
