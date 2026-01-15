from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import threading
import webbrowser
import time

app = Flask(__name__, template_folder='.', static_folder='.')
CORS(app)

# Store destination path
destination_folder = None

@app.route('/')
def index():
    return render_template('Home.html')

# Serve static files explicitly
@app.route('/Home.js')
def serve_js():
    return send_from_directory('.', 'Home.js')

@app.route('/Home.css')
def serve_css():
    return send_from_directory('.', 'Home.css')

@app.route('/api/select-destination', methods=['POST'])
def select_destination():
    global destination_folder
    data = request.json
    folder_path = data.get('path')
    
    if not folder_path or not os.path.isdir(folder_path):
        return jsonify({'error': 'Invalid folder path'}), 400
    
    destination_folder = folder_path
    return jsonify({
        'success': True,
        'path': folder_path,
        'name': os.path.basename(folder_path)
    })

@app.route('/api/transfer-files', methods=['POST'])
def transfer_files():
    global destination_folder
    
    if not destination_folder:
        return jsonify({'error': 'Destination not selected'}), 400
    
    try:
        files = request.files.getlist('files')
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

if __name__ == '__main__':
    def open_browser():
        time.sleep(1)
        webbrowser.open('http://localhost:8080')
    
    thread = threading.Thread(target=open_browser, daemon=True)
    thread.start()
    
    app.run(debug=False, host='127.0.0.1', port=8080)
