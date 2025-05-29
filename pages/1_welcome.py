import streamlit as st

st.set_page_config(page_title="Panduan Penggunaan", page_icon="📖")

st.title("📖 Panduan Penggunaan Aplikasi")

st.markdown("""
Selamat datang di aplikasi **Pengenalan Cover Buku Otomatis**! 🎉

### Cara Menggunakan:
1. Buka halaman **`app`** di sidebar.
2. Tekan tombol **Aktifkan Kamera** untuk memulai kamera.
3. Arahkan cover buku ke kamera.
4. Tekan tombol **Scan** untuk melakukan deteksi OCR.
5. Aplikasi akan menampilkan hasil teks dari cover buku.
6. Sistem akan mencocokkan teks dengan kategori dari file `book_categories.json`.

---

### Catatan Tambahan:
- OCR hanya dilakukan saat tombol **Scan** ditekan agar performa lebih ringan.
- Pastikan pencahayaan cukup agar teks dapat terbaca dengan baik.

Selamat mencoba! 🚀
""")

