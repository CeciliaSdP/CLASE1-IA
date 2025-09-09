import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px

st.set_page_config(page_title="Agenda de reunión", page_icon="🗓️", layout="wide")

# ------------------------------
# Estado inicial
# ------------------------------
if "agenda_items" not in st.session_state:
    st.session_state.agenda_items = []  # cada item: {topic, owner, duration_min}

# ------------------------------
# Encabezado
# ------------------------------
st.title("🗓️ Agenda de reunión – Demo sin dataset")

with st.sidebar:
    st.header("Configuración de la reunión")
    meeting_title = st.text_input("Título de la reunión", value="Reunión de coordinación")
    meeting_date = st.date_input("Fecha", value=pd.Timestamp.today())
    meeting_start_time = st.time_input("Hora de inicio", value=pd.Timestamp("09:00").time())

    st.divider()
    st.subheader("Agregar punto a la agenda")
    with st.form("add_item_form", clear_on_submit=True):
        topic = st.text_input("Tema / Actividad", placeholder="Ej.: Bienvenida y objetivos")
        owner = st.text_input("Responsable", placeholder="Ej.: Helen")
        duration = st.number_input("Duración (min)", min_value=1, max_value=480, value=10, step=5)
        submitted = st.form_submit_button("➕ Agregar a la agenda")
        if submitted:
            if topic.strip() == "":
                st.warning("Por favor, escribe un tema.")
            else:
                st.session_state.agenda_items.append({
                    "topic": topic.strip(),
                    "owner": owner.strip() if owner else "",
                    "duration_min": int(duration)
                })

    if st.button("🧹 Vaciar agenda"):
        st.session_state.agenda_items = []

# ------------------------------
# Si no hay ítems, muestra ejemplo
# ------------------------------
if len(st.session_state.agenda_items) == 0:
    example = [
        {"topic": "Bienvenida y objetivos", "owner": "Helen", "duration_min": 10},
        {"topic": "Estado del proyecto", "owner": "Equipo", "duration_min": 20},
        {"topic": "Bloque de decisiones", "owner": "Coordinación", "duration_min": 25},
        {"topic": "Próximos pasos", "owner": "Todos", "duration_min": 15},
    ]
    st.info("No hay puntos todavía. Se muestra un ejemplo editable.")
    items = example
else:
    items = st.session_state.agenda_items

# ------------------------------
# Construcción de horarios (start/end)
# ------------------------------
start_dt = datetime.combine(meeting_date, meeting_start_time)

rows = []
current_start = start_dt
for i, it in enumerate(items, start=1):
    start = current_start
    end = start + timedelta(minutes=it["duration_min"])
    rows.append({
        "Orden": i,
        "Tema": it["topic"],
        "Responsable": it["owner"],
        "Inicio": start,
        "Fin": end,
        "Duración (min)": it["duration_min"],
    })
    current_start = end

if rows:
    df = pd.DataFrame(rows)
else:
    df = pd.DataFrame(columns=["Orden", "Tema", "Responsable", "Inicio", "Fin", "Duración (min)"])

# ------------------------------
# Presentación
# ------------------------------
left, right = st.columns((0.6, 0.4))

with left:
    st.subheader("📝 Agenda detallada")
    st.caption("Edita desde la barra lateral. El orden lo define la secuencia de agregado.")
    st.dataframe(
        df[["Orden", "Tema", "Responsable", "Inicio", "Fin", "Duración (min)"]]
        .style.format({"Inicio": "{:%H:%M}", "Fin": "{:%H:%M}"}),
        use_container_width=True,
        hide_index=True,
    )

with right:
    st.subheader("📈 Visualización temporal")
    if not df.empty:
        # Gráfico tipo timeline con Plotly
        fig = px.timeline(
            df,
            x_start="Inicio",
            x_end="Fin",
            y="Tema",
            color="Responsable",
            hover_data={"Duración (min)": True, "Inicio": True, "Fin": True, "Responsable": True},
        )
        fig.update_yaxes(autorange="reversed")  # primer ítem arriba
        fig.update_layout(height=500, margin=dict(l=10, r=10, t=30, b=10))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Agrega al menos un punto para ver la línea de tiempo.")

# ------------------------------
# Exportaciones simples
# ------------------------------
st.divider()
col1, col2 = st.columns(2)
with col1:
    st.caption("Descarga un CSV para compartir la agenda.")
    st.download_button(
        label="⬇️ Descargar CSV",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="agenda.csv",
        mime="text/csv",
        disabled=df.empty,
    )

with col2:
    st.caption("Comparte esta página: el estado se reconstruye con cada sesión.")
    st.write(":bulb: Sugerencia: agrega un ítem 'Cierre' con la duración restante.")

# ------------------------------
# Encabezado visual final
# ------------------------------
st.markdown(f"""
> **{meeting_title}**  
> **Fecha:** {meeting_date.strftime('%d/%m/%Y')} — **Inicio:** {meeting_start_time.strftime('%H:%M')} — **Total estimado:** {df['Duración (min)'].sum() if not df.empty else 0} min
""")
