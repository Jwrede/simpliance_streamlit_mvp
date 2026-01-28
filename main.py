import streamlit as st
import pandas as pd
import plotly.express as px

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="simplayce | Basic Calculator", page_icon="🏢")

# --- SIDEBAR: INPUTS ---
st.sidebar.header("1. Ist-Zustand")
num_employees = st.sidebar.number_input("Anzahl Mitarbeiter", value=150, step=10)
sqm_per_desk = st.sidebar.number_input("Fläche pro Tisch (m²)", value=12)
rent_per_sqm = st.sidebar.number_input("Miete (€/m²)", value=25.0)

st.sidebar.header("2. New Work Szenario")
remote_days = st.sidebar.slider("Homeoffice Tage / Woche", 0, 5, 2)
sharing_ratio = st.sidebar.slider("Desk Sharing Quote", 0.5, 1.0, 0.8, help="1.0 = Jeder hat einen Tisch. 0.8 = 10 Leute teilen sich 8 Tische.")

st.sidebar.markdown("---")
st.sidebar.caption("Basic MVP v1.0")

# --- CALCULATION LOGIC (The "Math") ---
# 1. Baseline
baseline_desks = num_employees
baseline_sqm = baseline_desks * sqm_per_desk
baseline_cost = baseline_sqm * rent_per_sqm * 12 # Yearly

# 2. Optimized
# Logic: Attendance factor based on remote days
attendance_factor = 1 - (remote_days / 5)
# Real required desks based on attendance AND sharing policy
required_desks = int(num_employees * attendance_factor * sharing_ratio)
# Buffer (Safety margin 10%)
required_desks = int(required_desks * 1.1)

# Constraints: Can't have more desks than employees or less than 1
required_desks = max(1, min(required_desks, num_employees))

optimized_sqm = required_desks * sqm_per_desk
optimized_cost = optimized_sqm * rent_per_sqm * 12

savings = baseline_cost - optimized_cost
savings_percent = (savings / baseline_cost) * 100

# --- MAIN DASHBOARD ---
st.title("🏢 simplayce | Potenzial-Rechner")
st.markdown("Datengrundlage für Flächenoptimierung")

# 1. KPI Row (Standard Metrics)
col1, col2, col3 = st.columns(3)
col1.metric("Benötigte Tische", f"{required_desks}", delta=f"{required_desks - baseline_desks}", delta_color="inverse")
col2.metric("Fläche (m²)", f"{optimized_sqm:,.0f}", delta=f"{optimized_sqm - baseline_sqm:,.0f}", delta_color="inverse")
col3.metric("Kostenersparnis (Jahr)", f"{savings:,.2f} €", delta=f"{savings_percent:.1f}%", delta_color="normal")

st.markdown("---")

# 2. Basic Visualizations (No Heatmap!)
tab1, tab2 = st.tabs(["📊 Kosten-Analyse", "👥 Belegung"])

with tab1:
    st.subheader("Vergleich: Status Quo vs. New Work")
    
    # Simple Bar Chart
    data = pd.DataFrame({
        "Szenario": ["Status Quo", "Simplayce Optimiert"],
        "Kosten (p.a.)": [baseline_cost, optimized_cost],
        "Fläche (m²)": [baseline_sqm, optimized_sqm]
    })
    
    fig_cost = px.bar(data, x="Szenario", y="Kosten (p.a.)", text_auto=True, color="Szenario",
                      color_discrete_sequence=["#95a5a6", "#2ecc71"])
    st.plotly_chart(fig_cost, use_container_width=True)

with tab2:
    st.subheader("Kapazitäts-Planung")
    
    # Simple Pie Chart instead of Heatmap
    labels = ["Belegte Tische", "Eingespart / Leerstand"]
    values = [required_desks, baseline_desks - required_desks]
    
    fig_pie = px.pie(names=labels, values=values, hole=0.4, color_discrete_sequence=["#3498db", "#bdc3c7"])
    st.plotly_chart(fig_pie, use_container_width=True)
    
    st.info(f"Bei **{remote_days} Tagen Homeoffice** und einer Sharing-Quote von **{sharing_ratio}** werden nur noch **{required_desks}** Arbeitsplätze benötigt.")

# 3. Data Table
st.markdown("### 📋 Detail-Daten")
st.dataframe(data, use_container_width=True)