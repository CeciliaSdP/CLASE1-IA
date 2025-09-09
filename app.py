import streamlit as st
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
fig.update_yaxes(autorange="reversed") # para que el primer ítem quede arriba
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
st.write(":bulb: Sugerencia: fija un horario de fin agregando un ítem \"Cierre\" con la duración restante.")


# ------------------------------
# Encabezado visual
# ------------------------------
st.markdown(f"""
> **{meeting_title}**
> **Fecha:** {meeting_date.strftime('%d/%m/%Y')} — **Inicio:** {meeting_start_time.strftime('%H:%M')} — **Total estimado:** {df['Duración (min)'].sum() if not df.empty else 0} min
""")
