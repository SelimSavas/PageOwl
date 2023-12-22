import os
from pdf2image import convert_from_path

# Klasördeki tüm PDF dosyalarını al
pdf_folder = '/home/slm/Desktop/PageOwl/paper/'
output_folder = '/home/slm/Desktop/PageOwl/image/'

# PDF dosyalarının bulunduğu klasörde dolaş
for pdf_file in os.listdir(pdf_folder):
    if pdf_file.endswith('.pdf'):
        pdf_path = os.path.join(pdf_folder, pdf_file)

        # PDF'yi resimlere dönüştür
        images = convert_from_path(pdf_path)

        # Her bir sayfayı ayrı ayrı kaydet
        for i in range(len(images)):
            image_path = os.path.join(output_folder, f'{pdf_file}_page{i + 1}.jpg')
            images[i].save(image_path, 'JPEG')

print("Dönüştürme işlemi tamamlandı.")

