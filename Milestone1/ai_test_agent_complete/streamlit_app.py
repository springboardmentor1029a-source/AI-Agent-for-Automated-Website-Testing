import streamlit as st
import requests
st.title("AI Website Testing Agent — Streamlit UI")
instruction = st.text_area("Enter test instruction", height=150)
if st.button("Run Test"):
    with st.spinner("Running..."):
        r = requests.post("http://127.0.0.1:5000/run_test", json={"instruction": instruction})
        st.json(r.json())
