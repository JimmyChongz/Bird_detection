from flask import Flask, request, send_file, jsonify, render_template_string
import os
import subprocess

app = Flask(__name__)

UPLOAD_FOLDER = './uploads'
RESULT_FOLDER = './runs/detect/exp'  # YOLOv7 預設輸出目錄
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return '''
        <h1>YOLOv7 Object Detection</h1>
        <form action="/predict" method="post" enctype="multipart/form-data">
            <input type="file" name="file" accept="image/*,video/mp4" />
            <input type="submit" value="Upload and Predict" />
        </form>
    '''

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # 儲存上傳的檔案
    file_ext = file.filename.rsplit('.', 1)[-1].lower()
    if file_ext not in ['jpg', 'jpeg', 'png', 'mp4']:
        return jsonify({'error': 'Unsupported file type'}), 400

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    # YOLOv7 偵測命令
    detect_script = './yolov7/detect.py'
    weights_path = './yolov7/weights/best.pt'
    
    if file_ext == 'mp4':
        result_source = file_path  # 直接使用視頻檔案進行偵測
    else:
        result_source = file_path  # 圖片檔案

    try:
        subprocess.run(
            [
                'python3', detect_script,
                '--weights', weights_path,
                '--source', result_source
            ],
            check=True
        )
    except subprocess.CalledProcessError as e:
        return jsonify({'error': f'Detection failed: {e}'}), 500

    result_file_path = os.path.join(RESULT_FOLDER, file.filename)
    if not os.path.exists(result_file_path):
        return jsonify({'error': 'Result file not found'}), 500

    # 如果是視頻，返回視頻文件並提供下載
    if file_ext == 'mp4':
        video_url = f'/download/{file.filename}'
        return render_template_string('''
            <h2>Processed Video:</h2>
            <video controls style="max-width: 100%;">
                <source src="{{ video_url }}" type="video/mp4" />
                Your browser does not support the video tag.
            </video>
            <br>
            <a href="{{ video_url }}" download>Download Processed Video</a>
        ''', video_url=video_url)
    
    # 如果是圖片，直接顯示圖片
    else:
        image_url = f'/image/{file.filename}'
        return render_template_string('''
            <h2>Processed Image:</h2>
            <img src="{{ image_url }}" style="max-width: 100%;" />
        ''', image_url=image_url)


@app.route('/image/<filename>')
def get_image(filename):
    result_file_path = os.path.join(RESULT_FOLDER, filename)
    if os.path.exists(result_file_path):
        return send_file(result_file_path, mimetype='image/jpeg')
    return jsonify({'error': 'Image not found'}), 404

@app.route('/download/<filename>')
def download_video(filename):
    result_file_path = os.path.join(RESULT_FOLDER, filename)
    if os.path.exists(result_file_path):
        return send_file(result_file_path, mimetype='video/mp4', as_attachment=True, download_name=filename)
    return jsonify({'error': 'Video not found'}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
