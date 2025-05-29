import streamlit as st
import cv2
import easyocr
import json
import tempfile
from PIL import Image


# Inisialisasi OCR
reader = easyocr.Reader(['en', 'id'])

# Fungsi kategori
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

# Inisialisasi session state
if 'camera_on' not in st.session_state:
    st.session_state.camera_on = False
if 'captured_frame' not in st.session_state:
    st.session_state.captured_frame = None

# UI Awal
st.title("🚀 Ayo Mulai Scan Bukumu")
st.write('Untuk memulainya, tekan tombol **"Aktifkan Kamera"** di bawah! 📸')

# Tombol Aktifkan Kamera
# if not st.session_state.camera_on:
#     if st.button("Aktifkan Kamera"):
#         st.session_state.camera_on = True
#         st.experimental_rerun()
if not st.session_state.camera_on:
    if st.button("Aktifkan Kamera"):
        st.session_state.camera_on = True

else:
    # Kamera Aktif
    st.subheader("📷 Kamera Aktif - Siapkan Buku Anda")
    frame_placeholder = st.empty()
    scan_button = st.button("📸 Scan Cover Buku")

    # Mulai kamera
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    if not ret:
        st.error("Tidak dapat mengakses kamera.")
    else:
        # Tampilkan frame
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # frame_placeholder.image(frame_rgb, channels="RGB", use_column_width=True)
        frame_placeholder.image(frame_rgb, channels="RGB", use_container_width=True)


        # Simpan frame untuk scanning
        if scan_button:
            st.session_state.captured_frame = frame
            st.success("Gambar berhasil diambil! Lanjut ke proses OCR...")

    cap.release()

# Jika sudah ada hasil gambar yang di-scan
if st.session_state.captured_frame is not None:
    st.subheader("📄 Hasil Scan")
    # st.image(st.session_state.captured_frame, channels="BGR", use_column_width=True)
    st.image(st.session_state.captured_frame, channels="BGR", use_container_width=True)


    with st.spinner("🔍 Membaca teks..."):
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
        cv2.imwrite(temp_file.name, st.session_state.captured_frame)

        results = reader.readtext(temp_file.name)
        extracted_text = " ".join([text for (_, text, _) in results])
        kategori = categorize_book(extracted_text)

        st.markdown("### 📝 Teks Terbaca")
        st.write(extracted_text if extracted_text else "Tidak ada teks terbaca.")

        st.markdown("### 🏷️ Kategori Buku")
        st.success(kategori)
