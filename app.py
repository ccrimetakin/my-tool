import streamlit as st
from rembg import remove
from PIL import Image
import io
import requests

# Page setup
st.set_page_config(page_title="Ultimate AI Photo Editor", layout="wide")

st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 10px; background-color: #007bff; color: white; font-weight: bold; }
    .stDownloadButton>button { width: 100%; border-radius: 10px; background-color: #28a745; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("📸 Pro AI Background Editor")
st.write("Background hatayein aur apni pasand ka naya look dein!")

# --- Sidebar Settings ---
st.sidebar.header("⚙️ Background Options")
mode = st.sidebar.selectbox("Kya lagana chahte hain?", ["Transparent (Blank)", "Solid Color", "Stock Image"])

bg_image_final = None

if mode == "Solid Color":
    chosen_color = st.sidebar.color_picker("Color Chuniye", "#FFFFFF")
elif mode == "Stock Image":
    stock_options = {
        "Office": "https://images.unsplash.com/photo-1497366216548-37526070297c?w=800",
        "Nature": "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=800",
        "Studio Gray": "https://images.unsplash.com/photo-1557683316-973673baf926?w=800",
        "Abstract Blue": "https://images.unsplash.com/photo-1554034483-04fda0d3507b?w=800"
    }
    selection = st.sidebar.selectbox("Stock Background Chuniye:", list(stock_options.keys()))
    bg_url = stock_options[selection]
    bg_image_final = Image.open(requests.get(bg_url, stream=True).raw).convert("RGBA")

# --- Main Interface ---
upload = st.file_uploader("Photo Upload Karein", type=["jpg", "png", "jpeg"])

if upload:
    c1, c2 = st.columns(2)
    input_img = Image.open(upload)
    with c1:
        st.image(input_img, caption="Original Photo", use_container_width=True)

    if st.button("Magic Edit Shuru Karein ✨"):
        with st.spinner("AI Background Hatane Mein Busy Hai..."):
            # 1. Background Remove
            img_bytes = upload.getvalue()
            subject_bytes = remove(img_bytes)
            subject = Image.open(io.BytesIO(subject_bytes)).convert("RGBA")
            
            # 2. New Background Preparation
            if mode == "Transparent (Blank)":
                final_img = subject
            elif mode == "Solid Color":
                # Hex to RGB
                h = chosen_color.lstrip('#')
                rgb = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
                new_bg = Image.new("RGBA", subject.size, rgb + (255,))
                final_img = Image.alpha_composite(new_bg, subject)
            elif mode == "Stock Image":
                # Resize stock image to match subject size
                bg_resized = bg_image_final.resize(subject.size, Image.Resampling.LANCZOS)
                final_img = Image.alpha_composite(bg_resized, subject)

            with c2:
                st.image(final_img, caption="New Result", use_container_width=True)
            
            # 3. Download Logic
            buf = io.BytesIO()
            if mode == "Transparent (Blank)":
                final_img.save(buf, format="PNG")
                st.download_button("📥 Download PNG", buf.getvalue(), "transparent.png", "image/png")
            else:
                final_img.convert("RGB").save(buf, format="JPEG")
                st.download_button("📥 Download JPG", buf.getvalue(), "edited_photo.jpg", "image/jpeg")
