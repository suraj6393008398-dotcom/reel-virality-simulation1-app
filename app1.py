import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
st.set_page_config(page_title="Reel Virality Simulator", layout="wide")
st.title(" Instagram Reel Virality Simulator")
st.markdown("Enter your metrics below. **No Sidebar**—everything is right here!")
st.markdown("---")
if "history" not in st.session_state:
    st.session_state.history = []
st.subheader(" Input Parameters")
col1, col2, col3 = st.columns(3)
def get_float(value, default=0):
    try:
        return float(value)
    except:
        return default
def get_int(value, default=0):
    try:
        return int(value)
    except:
        return default
with col1:
    v0 = get_int(st.text_input("Initial Viewers (V0)", placeholder="enter initial viewer"))
    growth_rate = get_float(st.text_input("Growth Rate (Spread)", placeholder="enter growth rate"))
with col2:
    s0 = get_int(st.text_input("Initial Sharers (S0)", placeholder="enter shared viewer"))
    decay_rate = get_float(st.text_input("Decay Rate (Drop-off)", placeholder="enter decay rate"))
with col3:
    total_pop = get_int(st.text_input("Total Audience (N)", placeholder="enter total audience"))
    duration = get_int(st.text_input("Time Duration (T)", placeholder="enter time duration"))
run_button = st.button(" Run Simulation", use_container_width=True)
st.markdown("---")
def simulate_virality(V0, g, d, T, N):
    t = np.arange(0, int(T))
    viewers_list = []
    V = V0   
    for i in t:
        new_views = g * V * (1 - V / N)
        drop_off = d * V
        V = V + new_views - drop_off
        V = max(0, min(V, N)) 
        viewers_list.append(V)    
    return t, viewers_list
if run_button:
    t, viewers = simulate_virality(v0, growth_rate, decay_rate, duration, total_pop)
    peak_val = max(viewers)
    peak_time = t[viewers.index(peak_val)]
    final_val = viewers[-1]
    st.session_state.history.append({
        "Growth": growth_rate,
        "Decay": decay_rate,
        "Peak": int(peak_val),
        "Peak Time": int(peak_time),
        "Final": int(final_val),
        "graph_data": viewers
    })
    m1, m2, m3 = st.columns(3)
    m1.metric(" Peak Viewers", f"{int(peak_val):,}")
    m2.metric(" Time to Peak", f"{int(peak_time)} units")
    m3.metric(" Final Status", f"{int(final_val):,}")
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.plot(t, viewers, color='#E1306C', linewidth=3, label="Current Run")
    ax.fill_between(t, viewers, color='#FD1D1D', alpha=0.1)
    ax.set_xlabel("Time")
    ax.set_ylabel("Viewers")
    ax.grid(True, linestyle='--', alpha=0.5)
    st.pyplot(fig)
if st.session_state.history:
    st.markdown("---")
    st.subheader(" History & Comparison")
    history_df = pd.DataFrame(st.session_state.history).drop(columns=['graph_data'])
    st.dataframe(history_df, use_container_width=True)
    btn_col1, btn_col2 = st.columns(2)
    with btn_col1:
        if st.button(" Clear History"):
            st.session_state.history = []
            st.rerun()
    with btn_col2:
        compare_btn = st.button(" Compare All Runs")
    if compare_btn:
        if len(st.session_state.history) > 1:
            st.markdown("### Comparison Analysis")
            fig_comp, ax_comp = plt.subplots(figsize=(12, 5))
            for i, run in enumerate(st.session_state.history):
                ax_comp.plot(run['graph_data'], label=f"Run {i+1} (G:{run['Growth']})")           
            ax_comp.legend()
            ax_comp.set_xlabel("Time")
            ax_comp.set_ylabel("Viewers")
            ax_comp.grid(True, linestyle='--', alpha=0.5)
            st.pyplot(fig_comp)
        else:
            st.warning("Bro, you need at least 2 runs in history to compare them!")