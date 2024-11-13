import os
import zipfile
import uuid
from flask import Flask, request, jsonify, render_template, send_file, url_for, redirect
from inference_sdk import InferenceHTTPClient
from pdf2image import convert_from_path
from PIL import Image

# Flask uygulaması oluştur
app = Flask(__name__)

# RoboFlow API istemcisini başlat
CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key="tatWHpKD8MWgIalToK9o"
)

# Yüklemeler ve crop edilen görüntüler için klasörler oluştur
UPLOAD_FOLDER = 'uploads'
CROPPED_FOLDER = 'static/cropped'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CROPPED_FOLDER, exist_ok=True)

# Ana sayfa - PDF yükleme formu
@app.route('/')
def index():
    return render_template('index.html')

# PDF dosyasını yükleyip işleme alacak endpoint
@app.route('/upload', methods=['POST'])
def upload_pdf():
    if 'pdf' not in request.files:
        return jsonify({'error': 'Lütfen bir PDF dosyası yükleyin.'}), 400

    pdf_file = request.files['pdf']
    pdf_path = os.path.join(UPLOAD_FOLDER, f"{uuid.uuid4()}.pdf")
    pdf_file.save(pdf_path)

    # PDF'i görüntülere çevir
    images = convert_pdf_to_images(pdf_path)
    
    # Görüntüler üzerinde çıkarım yap ve crop et
    cropped_image_paths = []
    for idx, image in enumerate(images):
        result = CLIENT.infer(image, model_id="pageowl-wzh3i/1")
        cropped_images = crop_bounding_boxes(image, result)
        cropped_image_paths.extend(save_cropped_images(cropped_images, idx))

    # İşlenen görüntü yollarını döndür
    relative_paths = [os.path.relpath(path, 'static') for path in cropped_image_paths]
    return render_template('index.html', images=relative_paths)

# PDF'i görüntülere dönüştürme
def convert_pdf_to_images(pdf_path):
    return convert_from_path(pdf_path, dpi=300)

# Bounding box'ları kullanarak crop yapma
def crop_bounding_boxes(image, result):
    cropped_images = []
    for item in result['predictions']:
        x, y, w, h = item['x'], item['y'], item['width'], item['height']
        left = int(x - w / 2)
        top = int(y - h / 2)
        right = int(x + w / 2)
        bottom = int(y + h / 2)
        cropped_img = image.crop((left, top, right, bottom))
        cropped_images.append(cropped_img)
    return cropped_images

# Crop edilen görüntüleri kaydetme
def save_cropped_images(cropped_images, page_idx):
    paths = []
    for idx, cropped_img in enumerate(cropped_images):
        image_path = os.path.join(CROPPED_FOLDER, f"page{page_idx}_crop{idx}.png")
        cropped_img.save(image_path)
        paths.append(image_path)
    return paths

# Uygulamayı başlat
if __name__ == '__main__':
    app.run(debug=True, port=5000)
