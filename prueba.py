import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
import plotly.graph_objects as go

st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">', unsafe_allow_html=True)

#------------ Configuración web ------------
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

# Función para cargar datos con caché
@st.cache_data(ttl=600)
def load_data(gid):
    base_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTgIAHF5Rdo7EzkMz6ymYeBoDWQ4BDb6j0OzZNFa3OuHiEq3HS3t0BCQt7bof3MHk3NXQRp-3rZzz5l/pub?output=csv&gid="
    gid_fechas = 1002468456

    try:
        df_historia = pd.read_csv(f"{base_url}{gid}")
        df_fechas = pd.read_csv(f"{base_url}{gid_fechas}")
        df_historia = df_historia.merge(df_fechas, on="ID_corte", how="left")
        
        fechas_unicas = df_historia[['ID_corte', 'fecha_corte']].drop_duplicates()
        fechas_unicas = fechas_unicas.sort_values(by="ID_corte", ascending=True)
        
        fecha_dict = {row['fecha_corte']: row['ID_corte'] for _, row in fechas_unicas.iterrows()}
        
        return df_historia, fecha_dict
    except Exception as e:
        st.error(f"Error al cargar los datos: {e}")
        return pd.DataFrame(), {}

# Nuevo Dashboard
def show_dashboard(page_title, gid):
    df_historia, fecha_dict = load_data(gid)

    col_title = st.columns(1)[0]
    with col_title:
        st.markdown(f"### {page_title}")

    col_encargado, col_tarjetas = st.columns((1, 3))
    
    with col_encargado:
        st.markdown(
            """
            <div style="font-size: 16px; font-weight: bold;">Allison I. Reynoso</div>
            """,
            unsafe_allow_html=True
        )
        
        if fecha_dict:
            fechas_ordenadas_por_id = sorted(fecha_dict, key=fecha_dict.get)
            fecha_sel = st.selectbox("Fecha de corte:", fechas_ordenadas_por_id)
            id_sel = fecha_dict[fecha_sel]
            df_filtrado = df_historia[df_historia["ID_corte"] == id_sel]
        else:
            st.warning("No se encontraron datos para mostrar.")
            df_filtrado = pd.DataFrame(columns=["r_registros", "r_archivos", "r_almacenamiento", "sub_categoria"])

    total_registros = df_filtrado["r_registros"].sum()
    total_archivos = df_filtrado["r_archivos"].sum()
    total_almacenamiento = df_filtrado["r_almacenamiento"].sum()
    
    delta_registros_porcentual = 0
    fechas_unicas = sorted(list(fecha_dict.keys()), reverse=True)
    if len(fechas_unicas) > 1:
        indice_actual = fechas_unicas.index(fecha_sel)
        if indice_actual + 1 < len(fechas_unicas):
            fecha_anterior_sel = fechas_unicas[indice_actual + 1]
            df_anterior = df_historia[df_historia["fecha_corte"] == fecha_anterior_sel]
            total_registros_anterior = df_anterior["r_registros"].sum()
            if total_registros_anterior != 0:
                delta_registros_porcentual = ((total_registros - total_registros_anterior) / total_registros_anterior) * 100

    with col_tarjetas:
        col_reg, col_arch, col_alm = st.columns(3)
        with col_reg:
            with st.container(border=True):
                st.markdown(
                    f"""
                    <div style="display: flex; align-items: center; justify-content: space-between; padding-bottom: 20px;">
                        <div style="text-align: left; flex: 1;">
                            <div style="font-size: 32px; font-weight: bold;">{total_registros:,}</div>
                            <div style="font-size: 16px;">Registros</div>
                        </div>
                        <div style="text-align: right;">
                            <i class="fa-solid fa-file-lines" style="font-size: 40px; color: #01c2cb;"></i>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        with col_arch:
            with st.container(border=True):
                st.markdown(
                    f"""
                    <div style="display: flex; align-items: center; justify-content: space-between; padding-bottom: 20px;">
                        <div style="text-align: left; flex: 1;">
                            <div style="font-size: 32px; font-weight: bold;">{total_archivos:,}</div>
                            <div style="font-size: 16px;">Archivos</div>
                        </div>
                        <div style="text-align: right;">
                            <i class="fa-solid fa-folder" style="font-size: 40px; color: #01c2cb;"></i>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        with col_alm:
            with st.container(border=True):
                st.markdown(
                    f"""
                    <div style="display: flex; align-items: center; justify-content: space-between; padding-bottom: 20px;">
                        <div style="text-align: left; flex: 1;">
                            <div style="font-size: 32px; font-weight: bold;">{total_almacenamiento:,.1f} GB</div>
                            <div style="font-size: 16px;">Almacenamiento</div>
                        </div>
                        <div style="text-align: right;">
                            <i class="fa-solid fa-hard-drive" style="font-size: 40px; color: #01c2cb;"></i>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    col_resumen, col_rendimiento = st.columns((1, 3))
    
    with col_resumen:
        with st.container(border=True):
            st.markdown(
                """
                <div style="font-size: 20px; font-weight: bold; margin: 5;">Resumen por Sub Categorias</div>
                <div style="height: 20px;"></div>
                """,
                unsafe_allow_html=True
            )
            
            st.markdown(
                """
                <div style="
                    display: grid; 
                    grid-template-columns: 1fr 0.5fr 0.5fr 0.5fr; 
                    gap: 10px;
                    padding: 10px;
                    font-weight: bold;
                    background-color: #f0f2f6; 
                    border-radius: 10px;
                    margin-bottom: 5px;
                ">
                    <div>Subcategoría</div>
                    <div style="text-align: right;">Reg.</div>
                    <div style="text-align: right;">Arch.</div>
                    <div style="text-align: right;">Alm.</div>
                </div>
                """, 
                unsafe_allow_html=True
            )
            
            for index, row in df_filtrado.iterrows():
                st.markdown(
                    f"""
                    <div style="
                        display: grid; 
                        grid-template-columns: 1fr 0.5fr 0.5fr 0.5fr; 
                        gap: 10px;
                        padding: 10px;
                        background-color: white;
                        border-radius: 10px;
                        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
                        margin-bottom: 5px;
                        transition: all 0.2s ease-in-out;
                    ">
                        <div style="color: #01c2cb; font-weight: bold;">{row['sub_categoria']}</div>
                        <div style="text-align: right;">{row['r_registros']:,}</div>
                        <div style="text-align: right;">{row['r_archivos']:,}</div>
                        <div style="text-align: right;">{row['r_almacenamiento']:,.1f} GB</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            
        st.markdown("<br>", unsafe_allow_html=True) 
        st.markdown(
            f"""
            <div style="
                border: 1px solid #e0e0e0;
                border-radius: 0.5rem;
                padding: 0;
                overflow: hidden;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
            ">
                <div style="
                    background-color: #01c2cb;
                    padding: 20px;
                    height: 375px;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                    text-align: center;
                    color: white;
                    width: 100%;
                    margin: 0;
                ">
                    <h4 style="color: white; margin: 0 0 5px 0; padding: 0; font-size: 20px;">Crecimiento de Registros</h4>
                    <div style="font-size: 4em; font-weight: bold; margin: 5px 0;">{total_registros:,.0f}</div>
                    <div style="
                        font-size: 20px;
                        font-weight: bold;
                        display: flex;
                        align-items: center;
                        gap: 5px;
                    ">
                        <div style="color: white; font-size: 20px; padding: 0; font-weight: normal">Cambio vs. Periodo Anterior:</div>
                        <div style="
                            font-size: 20px; 
                            font-weight: bold; 
                            color: {'green' if delta_registros_porcentual >= 0 else 'red'} !important;
                        ">{delta_registros_porcentual:,.2f}%</div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col_rendimiento:
        with st.container(border=True):
            st.markdown(
                """
                <div style="font-size: 20px; font-weight: bold; margin: 5;">Evolución histórica de registros</div>
                """,
                unsafe_allow_html=True
            )
            
            df_linea = df_historia.groupby(['ID_corte', 'fecha_corte'])['r_registros'].sum().reset_index(name='Registros')
            df_linea = df_linea.sort_values(by="ID_corte", ascending=True)
            
            fig_linea = px.line(
                df_linea,
                x='fecha_corte',
                y='Registros',
                markers=True,
                line_shape='linear',
                title='',
                color_discrete_sequence=['#01c2cb']
            )
            
            fig_linea.update_traces(line=dict(width=4))
            fig_linea.update_traces(fill='tozeroy', fillcolor='rgba(1, 194, 203, 0.2)', mode='lines+markers')
            
            fig_linea.update_layout(
                height=400,
                xaxis_title="Fecha de Corte",
                yaxis_title="Cantidad de Registros",
                hovermode="x unified",
                plot_bgcolor='white',
                paper_bgcolor='white',
                font=dict(color='#4a4a4a')
            )
            
            st.plotly_chart(fig_linea, use_container_width=True)

        subcol1, subcol2 = st.columns((1.5, 1.5))
        with subcol1:
            with st.container(border=True):
                st.markdown(
                    """
                    <div style="font-size: 20px; font-weight: bold; margin: 5;">Distribución de registros por subcategoría</div>
                    """,
                    unsafe_allow_html=True
                )
                
                umbral = 0.05
                df_pie = df_filtrado[["sub_categoria", "r_registros"]].copy()
                df_pie.rename(columns={"sub_categoria": "Subcategoría", "r_registros": "Registros"}, inplace=True)

                total = df_pie["Registros"].sum()
                df_pie["Porcentaje"] = df_pie["Registros"] / total

                grandes = df_pie[df_pie["Porcentaje"] >= umbral]
                pequeñas = df_pie[df_pie["Porcentaje"] < umbral]

                if not pequeñas.empty:
                    otros = pd.DataFrame({
                        "Subcategoría": ["Otros"],
                        "Registros": [pequeñas["Registros"].sum()]
                    })
                    df_final_pie = pd.concat([grandes[["Subcategoría", "Registros"]], otros], ignore_index=True)
                else:
                    df_final_pie = grandes[["Subcategoría", "Registros"]]
                
                fig_pie = px.pie(
                    df_final_pie,
                    names="Subcategoría",
                    values="Registros",
                    hole=0.4,
                    color_discrete_sequence=[
                        "#016F75", "#5DF6FE", "#019AA2",
                        "#B8FBFF", "#004447", "#0BF3FE",
                    ]
                )
                st.plotly_chart(fig_pie, use_container_width=True)
        with subcol2:
            with st.container(border=True):
                st.markdown(
                    """
                    <div style="font-size: 20px; font-weight: bold; margin: 5;">Almacenamiento utilizado por subcategoría</div>
                    """,
                    unsafe_allow_html=True
                )
                
                fig_barras_2 = px.bar(
                    df_filtrado, 
                    x="sub_categoria", 
                    y="r_almacenamiento",
                    title="",
                    color_discrete_sequence=['#01c2cb']
                )
                
                fig_barras_2.update_layout(
                    height=400,
                    xaxis_title="Subcategoría",
                    yaxis_title="Almacenamiento (GB)",
                    plot_bgcolor='white', 
                    paper_bgcolor='white',
                    font=dict(color='#4a4a4a'),
                    title_font=dict(size=20),
                    hovermode="x unified"
                )
                
                st.plotly_chart(fig_barras_2, use_container_width=True)
                
### Main function
def main():
    st.sidebar.title("Menú")
    st.sidebar.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        text-align: left;
        background-color: transparent !important;
        border: none !important;
        color: #4a4a4a !important;
        font-size: 16px;
        font-weight: bold;
        padding: 10px 15px !important;
        margin: 5px 0;
        transition: background-color 0.2s;
    }
    .stButton>button:hover {
        background-color: #f0f2f6 !important;
        border-radius: 5px;
    }
    .stButton>button:active {
        background-color: #e6e8eb !important;
    }
    .stButton>button[style*="background-color: rgb(240, 242, 246)"] {
        color: #01c2cb !important;
        background-color: #f0f2f6 !important;
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

    if 'page' not in st.session_state:
        st.session_state.page = "Inicio"
    
    # Grid IDs para cada categoría
    GIDs = {
        "Inicio": 888266253,  # Historia y Literatura
        "Noticias": 0,       # Reemplazar con el GID correcto
        "Educación": 0,      # Reemplazar con el GID correcto
        "Poder Judicial": 0, # Reemplazar con el GID correcto
        "Poder Legislativo": 0, # Reemplazar con el GID correcto
        "Medicina": 0,       # Reemplazar con el GID correcto
        "Empleo": 0          # Reemplazar con el GID correcto
    }

    if st.sidebar.button("Historia y Literatura"):
        st.session_state.page = "Inicio"
    if st.sidebar.button("Noticias"):
        st.session_state.page = "Noticias"
    if st.sidebar.button("Educación"):
        st.session_state.page = "Educación"
    if st.sidebar.button("Poder Judicial"):
        st.session_state.page = "Poder Judicial"
    if st.sidebar.button("Poder Legislativo"):
        st.session_state.page = "Poder Legislativo"
    if st.sidebar.button("Medicina"):
        st.session_state.page = "Medicina"
    if st.sidebar.button("Empleo"):
        st.session_state.page = "Empleo"
    

    opcion = st.session_state.page

    st.sidebar.markdown(
        f"""
        <script>
        const buttons = window.parent.document.querySelectorAll('.stButton>button');
        buttons.forEach(btn => {{
            if (btn.innerText.includes("{opcion}")) {{
                btn.style.backgroundColor = '#f0f2f6';
                btn.style.color = '#01c2cb';
                btn.style.borderRadius = '5px';
            }}
        }});
        </script>
        """,
        unsafe_allow_html=True)
        
    if opcion in GIDs:
        show_dashboard(opcion, GIDs[opcion])
    else:
        st.header("Bienvenido al Dashboard Interactivo")
        st.write("Selecciona una de las opciones en el menú lateral para ver el contenido.")

if __name__ == "__main__":
    main()