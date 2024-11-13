import os
import subprocess
from pdf2image import convert_from_path
from tqdm import tqdm

def get_pdf_page_count(pdf_path):
    """pdfinfo kullanarak PDF'in sayfa sayısını alır."""
    try:
        output = subprocess.check_output(['pdfinfo', pdf_path], stderr=subprocess.STDOUT, text=True)
        for line in output.splitlines():
            if "Pages:" in line:
                return int(line.split(":")[1].strip())
    except subprocess.CalledProcessError as e:
        print(f"Hata: {pdf_path} sayfa sayısı alınamadı (pdfinfo hatası): {e.output}")
    except Exception as e:
        print(f"Hata: {pdf_path} sayfa sayısı alınamadı: {e}")
    return None

# paper ve paperPhoto klasörlerinin yollarını belirle
paper_folder = "./paper"
photo_folder = "./paperPhoto"

# paperPhoto klasörünü oluştur, eğer yoksa
os.makedirs(photo_folder, exist_ok=True)

# Tüm PDF dosyalarının listesini al
pdf_files = [f for f in os.listdir(paper_folder) if f.lower().endswith(".pdf")]
total_files = len(pdf_files)

# Tüm PDF'lerin toplam sayfa sayısını hesapla
total_pages = 0
valid_pdf_files = []
for filename in pdf_files:
    pdf_path = os.path.join(paper_folder, filename)
    page_count = get_pdf_page_count(pdf_path)
    if page_count is not None:
        total_pages += page_count
        valid_pdf_files.append(filename)
    else:
        print(f"Atlanıyor: {filename} dosyası okunamadı.")

# Tek bir ilerleme çubuğu ile tüm işlemi göster
with tqdm(total=total_pages, desc="PDF'ler işleniyor", unit="sayfa", ncols=80) as pbar:
    for filename in valid_pdf_files:
        pdf_path = os.path.join(paper_folder, filename)
        try:
            # DPI değerini 100'e indirerek bellek kullanımını azaltıyoruz
            pages = convert_from_path(pdf_path, dpi=100)
            for i, page in enumerate(pages):
                # PNG dosyasını kaydet
                output_filename = f"{os.path.splitext(filename)[0]}_page_{i + 1}.png"
                output_path = os.path.join(photo_folder, output_filename)
                page.save(output_path, "PNG")

                # İlerleme çubuğunu her sayfa kaydedildiğinde güncelle
                pbar.update(1)
        except Exception as e:
            print(f"{filename} dönüştürülürken hata oluştu: {e}")

print("\nTüm PDF dosyaları başarıyla dönüştürüldü!")

