import streamlit as st
from rembg import remove
from PIL import Image
import io

st.set_page_config(page_title="AI Background Remover")
st.title("✂️ AI Background Remover")

# Color Picker
color = st.sidebar.color_picker("Background Color Chuney", "#FFFFFF")

def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

upload = st.file_uploader("Photo upload karein", type=["png", "jpg", "jpeg"])

if upload:
    img = Image.open(upload)
    st.image(img, caption="Original Photo", width=300)
    
    if st.button("Magic Shuru Karein"):
        with st.spinner("Kaam ho raha hai..."):
            # Background hatana
            img_bytes = upload.getvalue()
            res_bytes = remove(img_bytes)
            subject = Image.open(io.BytesIO(res_bytes)).convert("RGBA")
            
            # Naya Background lagana
            bg_rgb = hex_to_rgb(color)
            new_bg = Image.new("RGBA", subject.size, bg_rgb + (255,))
            final = Image.alpha_composite(new_bg, subject).convert("RGB")
            
            st.image(final, caption="Tayyar Photo", width=300)
            
            # Download Button
            buf = io.BytesIO()
            final.save(buf, format="JPEG")
            st.download_button("Download Karein", buf.getvalue(), "photo.jpg", "image/jpeg")
