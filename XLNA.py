import streamlit as st
from PIL import Image
import io

# 1. Cấu hình trang (Đổi icon bằng URL hoặc Emoji)
st.set_page_config(
    page_title="Nén Ảnh Pro",
    page_icon="📸", # Bạn có thể thay bằng link ảnh .png vào đây
    layout="wide"
)

# 2. CSS để giao diện trông "xịn" hơn
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background-color: #007BFF;
        color: white;
    }
    div[data-testid="stMetricValue"] { font-size: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.title("📸 Nén Ảnh ")

# --- SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Cài đặt")
    quality = st.slider("Chất lượng (Quality)", 10, 100, 70)
    width_custom = st.number_input("Chiều rộng mới (0 = giữ nguyên)", value=0)
    st.divider()


# --- GIAO DIỆN CHÍNH ---
uploaded_file = st.file_uploader("Kéo thả ảnh vào đây", type=["jpg", "png", "jpeg"])

if uploaded_file:
    img = Image.open(uploaded_file)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Ảnh gốc")
        st.image(img, use_container_width=True)
        st.caption(f"Dung lượng: {uploaded_file.size/1024:.1f} KB")

    # Xử lý nén
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")
    
    if width_custom > 0:
        ratio = width_custom / float(img.size[0])
        new_h = int(float(img.size[1]) * ratio)
        img = img.resize((width_custom, new_h), Image.Resampling.LANCZOS)

    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=quality, optimize=True)
    byte_im = buf.getvalue()

    with col2:
        st.subheader("Ảnh đã nén")
        st.image(byte_im, use_container_width=True)
        st.success(f"Dung lượng mới: {len(byte_im)/1024:.1f} KB")

    st.download_button(
        label="📥 Tải ảnh đã nén",
        data=byte_im,
        file_name="nen_anh_pro.jpg",
        mime="image/jpeg"
    )
    # Ẩn các thành phần giao diện mặc định của Streamlit
hide_st_style = """
            <style>
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .stDeployButton {display:none;}
            #stDecoration {display:none;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
