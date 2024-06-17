from flask import Flask, request, send_from_directory, jsonify, render_template
import os
import subprocess
import glob

app = Flask(__name__, static_folder='frontend/static', template_folder='frontend/templates')
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'img')
OUTPUT_FOLDER = os.path.join(BASE_DIR, 'output')
MODEL_DIR = os.path.join(BASE_DIR, 'yolov3_mobilenet_v3_large_voc')

def get_next_filename(folder, prefix, ext):
    files = glob.glob(os.path.join(folder, f"{prefix}*.{ext}"))
    indices = [int(os.path.basename(f)[len(prefix):-len(ext)-1]) for f in files]
    next_index = max(indices, default=0) + 1
    return f"{prefix}{next_index}.{ext}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"})
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"})
    if file:
        filename = get_next_filename(UPLOAD_FOLDER, 'test', 'jpg')
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        # 调用detection.py
        command = f'python {BASE_DIR}/detection.py --image_path={filepath} --dir_save_path={OUTPUT_FOLDER}'
        subprocess.run(command, shell=True, check=True)
        
        # 返回图片路径
        output_filename = filename.replace('.jpg', '.png')  # Ensure output filename is a PNG
        return jsonify({"uploaded_image": filename, "output_image": output_filename})

@app.route('/img/<filename>')
def get_uploaded_image(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/output/<filename>')
def get_output_image(filename):
    return send_from_directory(OUTPUT_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)