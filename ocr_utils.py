import easyocr
import cv2
import json
import tempfile

# Inisialisasi Reader hanya sekali
reader = easyocr.Reader(['en', 'id'])

def capture_frame():
    """Ambil satu frame dari kamera dan simpan sebagai file gambar sementara"""
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()

    if not ret:
        return None, "Gagal mengambil gambar dari kamera."

    # Simpan ke file temporer
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
    cv2.imwrite(temp_file.name, frame)

    return temp_file.name, None

def perform_ocr(image_path):
    """Melakukan OCR pada file gambar"""
    results = reader.readtext(image_path)
    extracted_text = " ".join([text for (_, text, _) in results])
    return extracted_text

def categorize_book(text, categories_file="book_categories.json"):
    text_lower = text.lower()
    if not text_lower.strip():
        return "Kategori Tidak Dapat Ditentukan (Tidak ada teks)"

    try:
        with open(categories_file, 'r', encoding='utf-8') as f:
            categories_data = json.load(f)
    except FileNotFoundError:
        return "Error: File Kategori Tidak Ditemukan"
    except json.JSONDecodeError:
        return "Error: Format File Kategori Salah"

    best_match_category = "Kategori Tidak Diketahui"
    max_score = 0

    for category_info in categories_data:
        current_score = sum(1 for keyword in category_info.get("keywords", []) if keyword.lower() in text_lower)
        if current_score > max_score:
            max_score = current_score
            best_match_category = category_info.get("category_name", "Nama Kategori Tidak Ada")

    return best_match_category if max_score > 0 else "Kategori Tidak Diketahui (Tidak ada kata kunci cocok)"
