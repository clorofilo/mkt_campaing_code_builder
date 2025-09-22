# app_streamlit_promomodalidad.py
# ---------------------------------
# Interfaz visual (Streamlit) para construir la PROMOMODALIDAD
# a partir de los ficheros de equivalencias.
#
# Requisitos:
#   pip install streamlit pandas openpyxl numpy
# Ejecución:
#   streamlit run app_streamlit_promomodalidad.py
# Estructura esperada:
#   data/
#     └─ equivalencias_promo_modalidad.xlsx (hojas: promocion, modalidad, areas_paises)

import os
import numpy as np
import pandas as pd
import streamlit as st

# ==========================
# Configuración de la página
# ==========================
st.set_page_config(
    page_title="Promomodalidad Builder",
    page_icon="🎯",
    layout="wide",
)

# Estilos (tema suave, tarjetas, badges)
CUSTOM_CSS = """
<style>
/*********** Layout base ***********/
.block-container {padding-top: 2rem;}

/*********** Tarjeta principal ***********/
.card { 
  border-radius: 18px; 
  padding: 1.25rem 1.25rem; 
  border: 1px solid rgba(0,0,0,0.06);
  background: linear-gradient(180deg, rgba(255,255,255,0.9), rgba(249,250,251,0.9));
  box-shadow: 0 6px 24px rgba(0,0,0,0.06);
}
.card h3 {margin-top: 0.25rem; margin-bottom: 0.75rem;}

/*********** Badges ***********/
.badge {display:inline-block; padding: .25rem .6rem; border-radius: 999px; border: 1px solid rgba(0,0,0,.08); font-size: .85rem;}
.badge-soft {background: #f6f8fa;}
.badge-accent {background: #eef7ff; border-color: #b9e1ff;}

/*********** Code pill ***********/
.pill {font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace; padding: .25rem .5rem; border-radius: 8px; background: #0f172a; color: #e5e7eb;}

/*********** Resultado grande ***********/
.result {
  font-weight: 700; font-size: clamp(18px, 2.6vw, 36px); letter-spacing: .5px; 
  padding: .75rem 1rem; border-radius: 14px; background: #0F766E; color: white;
  display:inline-block;
}
.sub {font-size: .95rem; opacity: .85;}

/*********** Breadcrumb ***********/
.breadcrumb {display:flex; flex-wrap:wrap; gap:.35rem; align-items:center;}
.bc-item {padding:.25rem .5rem; background:#f3f4f6; border-radius:6px; font-size:.85rem;}
.bc-sep {opacity:.45;}

/*********** Footer note ***********/
.note {font-size: .85rem; color:#64748b}
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ==========================
# Carga de datos con cache
# ==========================
@st.cache_data(show_spinner=False)
def load_data(base_path: str = "data"):
    xlsx_path = os.path.join(base_path, "equivalencias_promo_modalidad.xlsx")
    if not os.path.exists(xlsx_path):
        st.error(
            f"No se encontró el fichero: {xlsx_path}.\n\n" \
            "Crea la carpeta 'data' y coloca el Excel 'equivalencias_promo_modalidad.xlsx' con las hojas 'promocion', 'modalidad', 'areas_paises'."
        )
        st.stop()
    df_promociones = pd.read_excel(xlsx_path, sheet_name="promocion")
    df_modalidades = pd.read_excel(xlsx_path, sheet_name="modalidad")
    df_area_paises = pd.read_excel(xlsx_path, sheet_name="areas_paises")
    return df_promociones, df_modalidades, df_area_paises


df_promociones, df_modalidades, df_area_paises = load_data()

# Helpers equivalentes a tus funciones

def filtrar_plataforma(df: pd.DataFrame, plataforma: str) -> pd.DataFrame:
    return df[df["Plataforma"] == plataforma]


def lista_plataformas(df: pd.DataFrame):
    plataformas = (
        pd.Series(df["Plataforma"]).dropna().astype(str).str.strip().unique().tolist()
    )
    return sorted(plataformas)


def seleccionar_area_paises(plataforma_select: str, pais_o_area: str):
    """Devuelve lista de regiones/áreas según plataforma y Pais/Area.
    Mantiene la misma lógica que tu script CLI.
    """
    if plataforma_select == "LinkedIn":
        d = filtrar_plataforma(df_modalidades, "LinkedIn")
        d = d[d["Area/programa"] == pais_o_area.lower()]
        opciones = sorted(list(d["particularidad"].dropna().astype(str).unique()))
        return opciones
    else:
        d = df_promociones[df_promociones["Plataforma"] == plataforma_select]
        d = d[d["Pais/Area"] == pais_o_area.lower()]
        opciones = sorted(list(d["Area/programa"].dropna().astype(str).unique()))
        return opciones


def seleccionar_particularidad(plataforma_select: str, region: str, pais_area: str):
    if plataforma_select == "LinkedIn":
        d = df_modalidades[
            (df_modalidades["Plataforma"] == "LinkedIn") \
            & (df_modalidades["particularidad"] == region)
        ]
        col1_vals = sorted(pd.Series(d["Columna1"]).dropna().astype(str).unique().tolist())
        return col1_vals

    elif plataforma_select == "Google":
        d = df_promociones[
            (df_promociones["Plataforma"] == "Google")
            & (df_promociones["Area/programa"] == region)
            & (df_promociones["Pais/Area"] == pais_area.lower())
        ]
        expats = sorted(pd.Series(d["Expats/No"]).dropna().astype(str).unique().tolist())
        return expats

    elif plataforma_select == "Meta":
        # Se maneja por pasos en el flujo de 'Meta'
        return []

    return []


def seleccionar_programa_meta():
    d = df_modalidades[df_modalidades["Plataforma"] == "Meta"].copy()

    area_programa_list = sorted(pd.Series(d["Area/programa"]).dropna().astype(str).unique().tolist())
    area = st.selectbox("Área/Programa (Meta)", options=area_programa_list, index=0, key="meta_area")

    dd = d[d["Area/programa"] == area]
    tipos_list = sorted(pd.Series(dd["particularidad"]).dropna().astype(str).unique().tolist())
    tipo = st.selectbox("Tipo de campaña", options=tipos_list, index=0, key="meta_tipo")

    dd = dd[dd["particularidad"] == tipo]
    zonas = sorted(pd.Series(dd["Zona Meta"]).dropna().astype(str).unique().tolist())
    zona = st.selectbox("Zona Meta", options=zonas, index=0, key="meta_zona")

    dd = dd[dd["Zona Meta"] == zona]
    areas_zona = sorted(pd.Series(dd["Columna1"]).dropna().astype(str).unique().tolist())
    area_zona = st.selectbox("Área de programas (según Zona)", options=areas_zona, index=0, key="meta_area_zona")

    modalidad = dd[dd["Columna1"] == area_zona]["Modalidad"].iloc[0]
    return area, tipo, zona, area_zona, modalidad


def seleccionar_programa_google():
    d = df_modalidades[df_modalidades["Plataforma"] == "Google"].copy()

    area_programa_list = sorted(pd.Series(d["Area/programa"]).dropna().astype(str).unique().tolist())
    area = st.selectbox("Área/Programa (Google)", options=area_programa_list, index=0, key="g_area")

    dd = d[d["Area/programa"] == area]
    particularidad_list = sorted(pd.Series(dd["particularidad"]).dropna().astype(str).unique().tolist())
    part = st.selectbox("Demand gen o no", options=particularidad_list, index=0, key="g_part")

    modalidad = dd[dd["particularidad"] == part]["Modalidad"].iloc[0]
    return area, part, modalidad


# ==========================
# UI – Controles
# ==========================
st.title("🎯 Promomodalidad Builder")

left, right = st.columns([1.5, 1])

with left:
    st.markdown("""
    <div class="card">
      <h3>Configuración</h3>
      <span class="badge badge-soft">Crea la combinación para tu campaña</span>
    </div>
    """, unsafe_allow_html=True)

    plataformas = lista_plataformas(df_promociones)
    plataforma = st.selectbox("Plataforma", options=plataformas, index=0)

    pais_area = st.segmented_control(
        "La campaña es para...",
        options=["Pais", "Area"],
        default="Pais",
        help="Selecciona si tu targeting es un único país o un área",
    )

    # Regiones disponibles dado plataforma + pais/area
    regiones = seleccionar_area_paises(plataforma, pais_area)
    if not regiones:
        st.warning("No hay regiones disponibles para la selección actual.")
        st.stop()

    region = st.selectbox(
        "Región (país/área)", options=regiones, index=0,
        help="Lista derivada de tus equivalencias"
    )

    # Particularidad (según plataforma)
    particularidades = seleccionar_particularidad(plataforma, region, pais_area)

    if plataforma == "LinkedIn":
        # 'particularidades' son valores de Columna1
        if not particularidades:
            st.warning("No hay modalidades disponibles para esta región en LinkedIn.")
            st.stop()
        particularidad = st.selectbox("Tipo de campaña (Columna1)", options=particularidades, index=0)

    elif plataforma == "Google":
        # 'particularidades' son Expats/No
        if not particularidades:
            st.warning("No hay opciones de Expats/No para esta región.")
            st.stop()
        particularidad = st.selectbox("Expats/No", options=particularidades, index=0)

    else:
        particularidad = ""

with right:
    st.markdown("""
    <div class="card">
      <h3>Progreso</h3>
      <div class="breadcrumb">
        <span class="bc-item">Plataforma: <b>{plataforma}</b></span>
        <span class="bc-sep">→</span>
        <span class="bc-item">Ámbito: <b>{ambito}</b></span>
        <span class="bc-sep">→</span>
        <span class="bc-item">Región: <b>{region}</b></span>
      </div>
    </div>
    """.format(plataforma=plataforma, ambito=pais_area, region=region), unsafe_allow_html=True)

# Ramas por plataforma para obtener MODALIDAD y PROMOCIÓN
modalidad = None
promo = None
extra_info = {}

if plataforma == "Meta":
    st.divider()
    st.subheader("Meta – Detalles de campaña")
    area, tipo, zona, area_zona, modalidad = seleccionar_programa_meta()

    # obtener PROMO desde df_promociones con (Plataforma, Pais/Area, Area/programa = region)
    try:
        promo = df_promociones[
            (df_promociones["Plataforma"] == "Meta")
            & (df_promociones["Pais/Area"] == pais_area.lower())
            & (df_promociones["Area/programa"] == region)
        ]["Promocion"].iloc[0]
    except IndexError:
        promo = None

    extra_info = {
        "Programa/Área": area,
        "Tipo de campaña": tipo,
        "Zona Meta": zona,
        "Área (según Zona)": area_zona,
    }

elif plataforma == "LinkedIn":
    # promoción (primera única disponible según tu script original)
    try:
        d = df_promociones[df_promociones["Plataforma"] == "LinkedIn"]
        promocion = sorted(pd.Series(d["Promocion"]).dropna().astype(str).unique().tolist())[0]
    except Exception:
        promocion = None

    promo = promocion

    # modalidad desde df_modalidades con filtros
    try:
        modalidad = df_modalidades[
            (df_modalidades["Plataforma"] == "LinkedIn")
            & (df_modalidades["Area/programa"] == pais_area.lower())
            & (df_modalidades["particularidad"] == region)
            & (df_modalidades["Columna1"] == particularidad)
        ]["Modalidad"].iloc[0]
    except IndexError:
        modalidad = None

elif plataforma == "Google":
    # selección adicional para Google
    st.divider()
    st.subheader("Google – Detalles de campaña")
    g_area, g_particularidad2, modalidad = seleccionar_programa_google()

    # promo basada en df_promo con filtros (como tu script)
    try:
        promo = df_promociones[
            (df_promociones["Plataforma"] == "Google")
            & (df_promociones["Pais/Area"] == pais_area.lower())
            & (df_promociones["Area/programa"] == region)
            & (df_promociones["Expats/No"] == particularidad)
        ]["Promocion"].iloc[0]
    except IndexError:
        promo = None
    
    extra_info = {
        "Programa/Área (Google)": g_area,
        "Demand gen o no": g_particularidad2,
    }

# ==========================
# Resultado y resumen
# ==========================

st.divider()

col_res, col_meta = st.columns([1.4, 1])

with col_res:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### Resultado")

    if promo and modalidad:
        promomod = f"{str(promo).upper()}{str(modalidad).upper()}"
        st.markdown(f"<span class='result'>{promomod}</span>", unsafe_allow_html=True)
        st.markdown(
            f"<div class='sub'>Plataforma: <b>{plataforma}</b> · Ámbito: <b>{pais_area}</b> · Región: <b>{region}</b></div>",
            unsafe_allow_html=True,
        )

        if extra_info:
            st.json(extra_info, expanded=False)

        # Export opcional
        export = {
            "PROMOMODALIDAD": promomod,
            "Plataforma": plataforma,
            "Ambito": pais_area,
            "Region": region,
            "Particularidad": particularidad if plataforma in ("Google", "LinkedIn") else None,
            **{k: v for k, v in extra_info.items()},
        }
        st.download_button(
            label="Descargar selección (JSON)",
            data=pd.Series(export).to_json(indent=2, force_ascii=False).encode("utf-8"),
            file_name="promomod_seleccion.json",
            mime="application/json",
        )
    else:
        st.info("Completa las selecciones para ver el resultado.")
    st.markdown("</div>", unsafe_allow_html=True)

with col_meta:
    st.markdown("""
    <div class="card">
      <h3>Consejos</h3>
      <ul>
        <li>Las listas se alimentan 100% del Excel.</li>
        <li>Si cambias las equivalencias, solo recarga la página.</li>
        <li>El JSON exportado te permite encadenar la selección con tus scripts.</li>
      </ul>
      <div class="note">Tip: Usa <span class="pill">st.secrets</span> si necesitas rutas dinámicas o credenciales.</div>
    </div>
    """, unsafe_allow_html=True)

# ==========================
# Validaciones suaves
# ==========================

missing = []
for col in ["Plataforma", "Pais/Area", "Area/programa"]:
    if col not in df_promociones.columns:
        missing.append(f"promocion.{col}")
for col in ["Plataforma", "Area/programa", "Modalidad"]:
    if col not in df_modalidades.columns:
        missing.append(f"modalidad.{col}")
if missing:
    st.warning("Columnas faltantes: " + ", ".join(missing))

st.caption("Hecho con ❤️ para agilizar tu flujo de campañas.")
