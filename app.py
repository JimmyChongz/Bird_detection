import os
import subprocess  # 用於執行外部命令
from flask import Flask, request, send_file, jsonify

# 初始化 Flask 應用
app = Flask(__name__)

# 設定上傳檔案的路徑
UPLOAD_FOLDER = './uploads'
RESULT_FOLDER = './runs/detect/exp'  # YOLOv7 預設輸出目錄
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# 路由：首頁
@app.route('/')
def index():
    return '''
        <h1>YOLOv7 Object Detection</h1>
        <form action="/predict" method="post" enctype="multipart/form-data">
            <input type="file" name="file" accept="image/*" />
            <input type="submit" value="Upload and Predict" />
        </form>
    '''

# 路由：處理圖片並返回結果
@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # 儲存上傳的圖片
    img_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(img_path)

    # 構建 YOLOv7 命令並執行
    detect_script = './yolov7/detect.py'
    weights_path = './yolov7/weights/best.pt'
    result_source = img_path
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

    # YOLOv7 預設將結果保存至 runs/detect/exp 目錄
    result_img_path = os.path.join(RESULT_FOLDER, file.filename)
    if not os.path.exists(result_img_path):
        return jsonify({'error': 'Result image not found'}), 500

    # 返回處理後的圖片
    return send_file(result_img_path, mimetype='image/jpeg/mp4')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
