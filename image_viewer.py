import streamlit as st
import numpy as np
import cv2
from PIL import Image
import io

st.set_page_config(
    page_title="Image viewer",
    page_icon=":floppy_disk:",
    layout="wide",
)

# ========== Sidebar ==========
sidebar = st.sidebar.title("Ajustes da Imagem")

# ========== Upload ==========
upload = st.file_uploader("Carregar arquivo", type=["png", "jpg", "jpeg"])

# ========== Display Image ==========
if upload is not None:
    # Abre a imagem com PIL
    img = Image.open(upload).convert("RGB")

    # Converte para NumPy array (formato OpenCV)
    img_np = np.array(img)
    img_cv = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)

# ========== Filtros com OpenCV ==========
    
    sidebar = st.sidebar.title("Filtros")

    # ========== Inverter cor ==========
    inverter = st.sidebar.checkbox("Inverter Cor")
    if inverter:
        img_cv = cv2.bitwise_not(img_cv)

    # ========== Intensidade RGB ==========
    rgb = st.sidebar.checkbox("RGB")    
    
    if rgb:
        reset = st.sidebar.button("Resetar Intensidade")

        if reset:
            st.session_state.red_slider = 0
            st.session_state.green_slider = 0
            st.session_state.blue_slider = 0

        red = st.sidebar.slider("Intensidade do Vermelho", -255, 255, 0, key="red_slider")
        green = st.sidebar.slider("Intensidade do Verde", -255, 255, 0, key="green_slider")
        blue = st.sidebar.slider("Intensidade do Azul", -255, 255, 0, key="blue_slider")

        b, g, r = cv2.split(img_cv)

        if red:
            r = cv2.add(r, red)
        if green:
            g = cv2.add(g, green)
        if blue:
            b = cv2.add(b, blue)

        img_cv = cv2.merge((b, g, r))

    # ========== Contraste ==========
    contraste = st.sidebar.checkbox("Aumentar Contraste")
    if contraste:
        alpha = st.sidebar.slider("Contraste (α)", 1.0, 3.0, 1.5, step=0.1)  
        beta = st.sidebar.slider("Brilho (β)", 0, 100, 0, step=1)
        img_cv = cv2.convertScaleAbs(img_cv, alpha=alpha, beta=beta)

    # ========== Nitidez ==========
    nitidez = st.sidebar.checkbox("Aumentar Nitidez")
    if nitidez:
        kernel_nitidez = np.array([[0, -1, 0],
                                [-1, 5,-1],
                                [0, -1, 0]])
        img_cv = cv2.filter2D(img_cv, -1, kernel_nitidez) 
    # ========== Conversão para Cinza ==========
    
    cinza = st.sidebar.checkbox("Escala Cinza")

    if cinza:
        img_cv = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
        img_cv = cv2.cvtColor(img_cv, cv2.COLOR_GRAY2BGR)

    # ========== Blur ==========
    
    blur = st.sidebar.checkbox("Blur")
    
    if blur:
        img_cv = cv2.GaussianBlur(img_cv, (15, 15), 0)
    
    # ========== Detecção de Bordas ==========
    
    bordas = st.sidebar.checkbox("Detecção de Bordas")
    
    if bordas:
        img_cv = cv2.Canny(img_cv, 100, 200)
        img_cv = cv2.cvtColor(img_cv, cv2.COLOR_GRAY2BGR)
        
    sidebar = st.sidebar.title("Ajustes de sentido")

    # ========== Espelhamento ==========
    
    espelhamento = st.sidebar.checkbox("Espelhamento")
    if espelhamento:
            img_cv = cv2.flip(img_cv, 1)

    # ========== Rotação ========== 
    
    rotacao = st.sidebar.checkbox("Rotação")
    if rotacao:
        angulo = st.sidebar.slider("Ângulo de Rotação", 0, 360, 0)
        (h, w) = img_cv.shape[:2]
        centro = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(centro, angulo, 1.0)
        img_cv = cv2.warpAffine(img_cv, M, (w, h))
    
    # ========== Exibição ==========
    img_filtro = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
    img_filtro = Image.fromarray(img_filtro)
    
    col1, col2 = st.columns(2)

    with col1:
        st.image(img, caption="Imagem Original", use_container_width=True)

    with col2:
        st.image(img_filtro, caption="Imagem com Filtro", use_container_width=True)

    # ========== Download ==========
    st.sidebar.title("Download")
    formato = st.sidebar.selectbox("Formato", ["PNG", "JPEG", "PDF"], key="download_format")

    mime_types = {
        "PNG": "image/png",
        "JPEG": "image/jpeg",
        "PDF": "application/pdf"
    }

    buffer = io.BytesIO()
    img_filtro.save(buffer, format=formato)
    byte_im = buffer.getvalue()

    st.sidebar.download_button(
        label="Baixar imagem",
        data=byte_im,
        file_name=f"imagem_filtrada.{formato.lower()}",
        mime=mime_types[formato]
    )