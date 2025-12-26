import streamlit as st
from rembg import remove
from PIL import Image
import io

# Page Configuration
st.set_page_config(page_title="AI Pro Background Remover", layout="centered")

# CSS Fix: unsafe_allow_html use hota hai
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 20px; background-color: #007bff; color: white; }
    .stDownloadButton>button { width: 100%; border-radius: 20px; background-color: #28a745; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("✨ AI Photo Professional")
st.write("Professional photos banayein sirf ek click mein!")

# Sidebar Settings
st.sidebar.header("🎨 Appearance")
choice = st.sidebar.radio("Background Style:", ["Solid Color", "Transparent"])

bg_color = "#FFFFFF"
if choice == "Solid Color":
    bg_color = st.sidebar.color_picker("Color Chuniye", "#0000FF")
    
    st.sidebar.write("Quick Colors:")
    if st.sidebar.button("Passport Blue"): bg_color = "#0000FF"
    if st.sidebar.button("Plain White"): bg_color = "#FFFFFF"

def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

# File Upload
upload = st.file_uploader("Apni Photo Yahan Daalein", type=["png", "jpg", "jpeg"])

if upload:
    col1, col2 = st.columns(2)
    img = Image.open(upload)
    with col1:
        st.image(img, caption="Original Image", use_container_width=True)
    
    if st.button("Magic Process Shuru Karein"):
        with st.spinner("Processing..."):
            img_bytes = upload.getvalue()
            res_bytes = remove(img_bytes)
            subject = Image.open(io.BytesIO(res_bytes)).convert("RGBA")
            
            if choice == "Solid Color":
                rgb = hex_to_rgb(bg_color)
                new_bg = Image.new("RGBA", subject.size, rgb + (255,))
                final = Image.alpha_composite(new_bg, subject).convert("RGB")
            else:
                final = subject

            with col2:
                st.image(final, caption="Result", use_container_width=True)
            
            buf = io.BytesIO()
            if choice == "Solid Color":
                final.save(buf, format="JPEG")
                mime_type = "image/jpeg"
                ext = "jpg"
            else:
                final.save(buf, format="PNG")
                mime_type = "image/png"
                ext = "png"
                
            st.download_button(f"📥 Download {ext.upper()}", buf.getvalue(), f"pro_photo.{ext}", mime_type)
