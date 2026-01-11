import streamlit as st
from agent.graph import app as graph_app
from agent.config import TestConfig

st.set_page_config(page_title="AI Web Testing Agent", layout="wide")

st.title("🤖 AI Web Testing Agent")

# ---------------- Sidebar ----------------
st.sidebar.header("⚙️ Test Configuration")

headed = st.sidebar.checkbox("Run in Headed Mode", value=True)
slowmo = st.sidebar.slider("Slow Motion (ms)", 0, 2000, 0, step=100)

screenshot = st.sidebar.selectbox(
    "Screenshot Mode",
    ["off", "on", "only-on-failure"]
)

video = st.sidebar.checkbox("Record Video")

# ---------------- Main UI ----------------
st.subheader("🌐 Website URL")
website_url = st.text_input("Enter Website URL", "https://example.com")

st.subheader("📝 Test Instruction")
instruction = st.text_area(
    "Describe the test in natural language",
    "Open the website and verify the page loads"
)

if st.button("▶️ Run Test"):
    config = TestConfig(
        headed=headed,
        slowmo=slowmo,
        screenshot=screenshot,
        video=video
    )

    with st.spinner("Running test..."):
        output = graph_app.invoke({
            "instruction": instruction,
            "website_url": website_url,
            "config": config.__dict__
        })

    st.subheader("🧠 AI Steps")
    st.json(output["steps"])

    st.subheader("🧪 Result")
    st.json(output["result"])
