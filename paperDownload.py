import arxiv
import requests
import os

# Arxiv API'sini kullanarak makaleleri arayın
client = arxiv.Client()
query = "machine learning"
search = arxiv.Search(
    query=query,
    max_results=100,  # 100 makale indir
    sort_by=arxiv.SortCriterion.Relevance
)

# Dosyaların kaydedileceği klasör
output_dir = "paper"
os.makedirs(output_dir, exist_ok=True)  # paper klasörü yoksa oluştur

# Makaleleri indir ve kaydet
for result in client.results(search):
    print(f"Downloading: {result.title}")
    try:
        pdf_response = requests.get(result.pdf_url)
        # Dosya adını temizle (geçersiz karakterleri kaldır)
        filename = "".join(c if c.isalnum() else "_" for c in result.title) + ".pdf"
        filepath = os.path.join(output_dir, filename)
        
        # PDF dosyasını kaydet
        with open(filepath, "wb") as file:
            file.write(pdf_response.content)
        print(f"Downloaded: {filepath}")
    except Exception as e:
        print(f"Error downloading {result.title}: {e}")

