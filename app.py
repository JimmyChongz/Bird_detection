from flask import Flask, request, send_file, jsonify, render_template
import os
import subprocess
import uuid
import glob

app = Flask(__name__)

UPLOAD_FOLDER = './uploads'
RESULT_FOLDER = './runs/detect'  # YOLOv7 輸出目錄
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # 檢查檔案類型
    file_ext = file.filename.rsplit('.', 1)[-1].lower()
    if file_ext not in ['jpg', 'jpeg', 'png', 'mp4', 'mov']:
        return jsonify({'error': 'Unsupported file type'}), 400

    # 儲存上傳的檔案
    file_name = f"{uuid.uuid4().hex}.{file_ext}"
    file_path = os.path.join(UPLOAD_FOLDER, file_name)
    file.save(file_path)

    # YOLOv7 偵測命令
    detect_script = './yolov7/detect.py'
    weights_path = './yolov7/weights/best.pt'

    try:
        subprocess.run(
            [
                'python3', detect_script,
                '--weights', weights_path,
                '--source', file_path
            ],
            check=True
        )
    except subprocess.CalledProcessError as e:
        return jsonify({'error': f'Detection failed: {e.stderr.decode()}'}), 500

    # 獲取最新結果目錄
    exp_folders = glob.glob(f"{RESULT_FOLDER}/exp*")
    if not exp_folders:
        return jsonify({'error': 'Result folder not found'}), 500
    latest_result_folder = max(exp_folders, key=os.path.getmtime)
    result_file_path = os.path.join(latest_result_folder, os.path.basename(file_path))

    if not os.path.exists(result_file_path):
        return jsonify({'error': 'Result file not found'}), 500

    # 判斷回傳內容（圖片或影片）
    if file_ext == 'mp4':
        return send_file(result_file_path, mimetype='video/mp4', as_attachment=False)
    elif file_ext == 'mov':
        return send_file(result_file_path, mimetype='video/mov', as_attachment=False)
    else:
        return send_file(result_file_path, mimetype='image/jpeg', as_attachment=False)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
