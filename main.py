import easyocr
import cv2
import json

# Inisialisasi EasyOCR Reader (untuk Bahasa Inggris & Indonesia)
reader = easyocr.Reader(['en', 'id'])  # bisa tambah 'id' jika ingin support Indonesia

# Buka kamera (webcam)
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # OCR pada frame
    results = reader.readtext(frame)

    # Tampilkan hasil ke frame
    for (bbox, text, prob) in results:
        (tl, tr, br, bl) = bbox
        tl = tuple(map(int, tl))
        br = tuple(map(int, br))

        # Gambar kotak & teks
        cv2.rectangle(frame, tl, br, (0, 255, 0), 2)
        cv2.putText(frame, text, (tl[0], tl[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

    # Tampilkan frame
    cv2.imshow("Real-time OCR", frame)

    # Tekan 'q' untuk keluar
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

#json
def categorize_book(text, categories_file="book_categories.json"):
    """Menganalisis teks dan menentukan kategori buku berdasarkan file JSON."""
    text_lower = text.lower()
    if not text_lower.strip():
        return "Kategori Tidak Dapat Ditentukan (Tidak ada teks)"

    try:
        with open(categories_file, 'r', encoding='utf-8') as f:
            categories_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: File kategori '{categories_file}' tidak ditemukan.")
        return "Error: File Kategori Hilang"
    except json.JSONDecodeError:
        print(f"Error: Format JSON salah pada file '{categories_file}'.")
        return "Error: Format Kategori Salah"

    best_match_category = "Kategori Tidak Diketahui"
    max_score = 0

    for category_info in categories_data:
        current_score = 0
        for keyword in category_info.get("keywords", []):
            if keyword.lower() in text_lower:
                current_score += 1
        
        if current_score > max_score:
            max_score = current_score
            best_match_category = category_info.get("category_name", "Nama Kategori Hilang")

    if max_score > 0:
        return best_match_category
    else:
        return "Kategori Tidak Diketahui (Tidak ada kata kunci cocok)"
cap.release()
cv2.destroyAllWindows()