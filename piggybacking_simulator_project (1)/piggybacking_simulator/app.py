import streamlit as st
import pandas as pd
from src.simulator import simulate
from src.database import init_db, save_run, load_runs
from src.socket_demo import send_demo_message
from src.diagram import ensure_diagram_image

st.set_page_config(
    page_title="Piggybacking Simulator",
    page_icon="📡",
    layout="wide",
    menu_items={
        "Get Help": None,
        "Report a bug": None,
        "About": None,
    }
)
init_db()

# Hide Streamlit Deploy button, 3-dots options menu, toolbar, and footer
st.markdown("""
<style>
    .stAppDeployButton, [data-testid="stAppDeployButton"] {
        display: none !important;
        visibility: hidden !important;
    }
    #MainMenu, [data-testid="stMainMenu"] {
        display: none !important;
        visibility: hidden !important;
    }
    [data-testid="stToolbar"] {
        display: none !important;
        visibility: hidden !important;
    }
    [data-testid="stDecoration"] {
        display: none !important;
        visibility: hidden !important;
    }
    footer, [data-testid="stFooter"] {
        display: none !important;
        visibility: hidden !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("📡 Efficient Frame Communication Using Piggybacking")

with st.sidebar:
    st.header("Simulation Parameters")
    a_to_b = st.slider("A → B data frames", 1, 50, 10)
    b_to_a = st.slider("B → A data frames", 0, 50, 6)
    data_size = st.number_input("Data payload per frame (bytes)", 64, 9000, 1000, 64)
    ack_size = st.number_input("ACK size (bytes)", 8, 256, 40, 8)
    wait_limit = st.number_input("Piggyback wait limit (ms)", 1, 5000, 100, 1)
    seed = st.number_input("Simulation seed", 0, 999999, 42)

    run = st.button("▶ Run Simulation", use_container_width=True)

if run:
    result = simulate(a_to_b, b_to_a, data_size, ack_size, wait_limit, seed)
    save_run(result)
    st.session_state["result"] = result
elif "result" not in st.session_state:
    st.session_state["result"] = simulate(a_to_b, b_to_a, data_size, ack_size, wait_limit, seed)

if "result" in st.session_state:
    result = st.session_state["result"]
    st.success("Simulation completed.")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Normal transmissions", result["normal"]["total_frames"])
    c2.metric("Piggyback transmissions", result["piggyback"]["total_frames"])
    c3.metric("Frames saved", result["comparison"]["frames_saved"])
    c4.metric("Bandwidth saved", f'{result["comparison"]["bandwidth_saved_pct"]:.2f}%')

    st.subheader("Communication Timeline")
    st.dataframe(pd.DataFrame(result["timeline"]), use_container_width=True, hide_index=True)

    st.subheader("Comparison")
    comparison_df = pd.DataFrame([
        {"Metric": "Data frames", "Normal ACK": result["normal"]["data_frames"],
         "Piggybacking": result["piggyback"]["data_frames"]},
        {"Metric": "Separate ACK frames", "Normal ACK": result["normal"]["ack_frames"],
         "Piggybacking": result["piggyback"]["ack_frames"]},
        {"Metric": "Combined DATA+ACK frames", "Normal ACK": 0,
         "Piggybacking": result["piggyback"]["piggyback_frames"]},
        {"Metric": "Total transmitted frames", "Normal ACK": result["normal"]["total_frames"],
         "Piggybacking": result["piggyback"]["total_frames"]},
        {"Metric": "Total bytes", "Normal ACK": result["normal"]["total_bytes"],
         "Piggybacking": result["piggyback"]["total_bytes"]},
        {"Metric": "ACK overhead %", "Normal ACK": round(result["normal"]["ack_overhead_pct"], 2),
         "Piggybacking": round(result["piggyback"]["ack_overhead_pct"], 2)},
    ])
    st.dataframe(comparison_df, use_container_width=True, hide_index=True)

    chart = pd.DataFrame({
        "Method": ["Normal ACK", "Piggybacking"],
        "Total Frames": [result["normal"]["total_frames"], result["piggyback"]["total_frames"]]
    }).set_index("Method")
    st.bar_chart(chart)

    st.subheader("Transmission Sequence Comparison")
    diagram_img = ensure_diagram_image()
    st.image(diagram_img, use_container_width=True)
    st.markdown(
        """<div style="background: rgba(56, 189, 248, 0.08); border-left: 4px solid #38bdf8; padding: 12px 18px; border-radius: 0 8px 8px 0; margin: 12px 0 16px 0; color: #cbd5e1; font-size: 0.95rem; line-height: 1.6;">
        Normal ACK requires separate acknowledgment frames. In piggybacking, the acknowledgment is attached to an outgoing data frame, reducing separate ACK transmissions and improving communication efficiency.
        </div>""",
        unsafe_allow_html=True
    )

    st.subheader("Formula")
    st.latex(r"\text{Bandwidth Saved \%}=\frac{\text{Normal Frames}-\text{Piggyback Frames}}{\text{Normal Frames}}\times100")

st.divider()
st.subheader("🌐 Real TCP Socket Demonstration")
msg = st.text_input("Message to send", "Hello from Piggybacking Simulator")
if st.button("Send TCP Demo"):
    response = send_demo_message(msg)
    st.info(response)

st.subheader("🗃️ Previous Runs")
history = load_runs()
if history:
    st.dataframe(pd.DataFrame(history), use_container_width=True, hide_index=True)
else:
    st.write("No simulations saved yet.")
