import streamlit as st
from dashboard import show_dashboard
from data_loader import load_data
from PIL import Image

st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">', unsafe_allow_html=True)

try:
    logo = Image.open("src/logo_AI.png")
    st.set_page_config(
        page_title="AiMara Dashboard",
        page_icon=logo,
        layout="wide",
        initial_sidebar_state="collapsed"
    )
except FileNotFoundError:
    st.set_page_config(
        page_title="AiMara Dashboard",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    st.warning("Advertencia: No se pudo encontrar 'src/logo_AI.png'. Usando ícono por defecto.")

GIDS = {
    "Historia y Literatura": 888266253,
    "Noticias": 2068753571,
    "Educación": 517062553,
    "Poder Judicial": 1937765031,
    "Poder Legislativo": 1185292120,
    "Medicina": 1970051983,
    "Gatronomía": 538377057,
    "Turismo y Hotelería": 1885603225,
    "Empleo": 1224871178
}

AUTORES = {
    "Historia y Literatura": "Allison Reynoso",
    "Noticias": "Sofia Quispe",
    "Educación": "Miriam Cayo",
    "Poder Judicial": "Elmer Collanqui",
    "Poder Legislativo": "Jamir Balcona",
    "Medicina": "Jesus Rocca",
    "Gatronomía": "Seline Maquera",
    "Turismo y Hotelería": "Hans Amesquita",
    "Empleo": "Seline Maquera"
}

def main():
    st.sidebar.title("Menú")
    
    # Detecta si el tema es oscuro
    is_dark_mode = st.get_option("theme.base") == "dark"
    
    # Define los colores según el modo de tema
    if is_dark_mode:
        button_color = "#E0E0E0"  # Blanco-gris claro para texto normal en modo oscuro
        hover_bg_color = "#2F313E" # Gris oscuro para hover en modo oscuro
        active_bg_color = "#3A3A3A" # Gris más oscuro para el botón activo
        active_text_color = "#01c2cb" # Color principal para el texto activo
    else:
        button_color = "#4a4a4a"   # Gris oscuro para texto normal en modo claro
        hover_bg_color = "#f0f2f6" # Gris muy claro para hover en modo claro
        active_bg_color = "#e6e8eb" # Gris un poco más oscuro para el botón activo
        active_text_color = "#01c2cb"

    st.sidebar.markdown(f"""
    <style>
    .stButton>button {{
        width: 100%;
        text-align: left;
        background-color: transparent !important;
        border: none !important;
        color: {button_color} !important;
        font-size: 16px;
        font-weight: bold;
        padding: 10px 15px !important;
        margin: 5px 0;
        transition: background-color 0.2s;
    }}
    .stButton>button:hover {{
        background-color: {hover_bg_color} !important;
        border-radius: 5px;
    }}
    .stButton>button:active {{
        background-color: {active_bg_color} !important;
    }}
    </style>
    """, unsafe_allow_html=True)

    if 'page' not in st.session_state:
        st.session_state.page = list(GIDS.keys())[0]

    for page_name in GIDS.keys():
        if st.sidebar.button(page_name, key=page_name):
            st.session_state.page = page_name

    current_page = st.session_state.page
    
    st.sidebar.markdown(
        f"""
        <script>
        const buttons = window.parent.document.querySelectorAll('.stButton>button');
        buttons.forEach(btn => {{
            if (btn.innerText.includes("{current_page}")) {{
                btn.style.backgroundColor = '{hover_bg_color}';
                btn.style.color = '{active_text_color}';
                btn.style.borderRadius = '5px';
            }}
        }});
        </script>
        """,
        unsafe_allow_html=True
    )
    
    if GIDS[current_page] != 0:
        show_dashboard(current_page, GIDS[current_page], AUTORES[current_page])
    else:
        st.header(f"Bienvenido al Dashboard de {current_page}")
        st.write("Selecciona una de las opciones en el menú lateral para ver el contenido.")
        
if __name__ == "__main__":
    main()