import streamlit as st
from agent.graph import app
from agent.config import TestConfig

st.title("🤖 AI Web Testing Agent")

website_url = st.text_input("🌐 Website URL", "https://www.flipkart.com")
instruction = st.text_area("📝 Test Instruction", "Open the website and search for iphone")

if st.button("Run Test"):
    config = TestConfig()

    output = app.invoke({
        "instruction": instruction,
        "website_url": website_url,
        "config": config.__dict__
    })

    st.subheader("🧠 AI Steps")
    st.json(output["steps"])

    st.subheader("🧪 Result")
    st.json(output["result"])

    st.subheader("📊 Dashboard")
    st.json(output["stats"])
