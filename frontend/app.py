import streamlit as st
import requests

st.set_page_config(page_title="AI Web Test Agent", layout="wide")

st.markdown("""
<style>
body { background-color:#0f172a; color:white; }
.card {
    background:#020617;
    padding:15px;
    border-radius:12px;
    margin-bottom:10px;
}
.pass { color:#22c55e; }
.fail { color:#ef4444; }
</style>
""", unsafe_allow_html=True)

st.title("🤖 AI Agent Web Tester")

instruction = st.text_area(
    "Enter Test Steps (Natural Language)",
    placeholder="Open spotify\nSearch for Arijit Singh\nVerify results page"
)

if "report" not in st.session_state:
    st.session_state.report = None

try:
    res = requests.post(
        "http://127.0.0.1:5000/run",
        json={"instruction": instruction},
        timeout=120
    )

    if res.status_code == 200:
        st.session_state.report = res.json()
    else:
        st.error("Backend error")
        st.text(res.text)

except requests.exceptions.ConnectionError:
    st.error("Backend crashed or browser blocked the test")


# 🟢 Display Results
if st.session_state.report:
    summary = st.session_state.report["summary"]

    st.subheader("📊 Test Summary")
    st.write(summary)

    st.subheader("🧪 Step Execution")
    for step in st.session_state.report["steps"]:
        status_class = "pass" if step["status"] == "PASS" else "fail"
        st.markdown(f"""
        <div class="card">
            <b>Step {step['step_no']}:</b> {step['action']} → {step['target']}<br>
            <span class="{status_class}">Status: {step['status']}</span>
        </div>
        """, unsafe_allow_html=True)
st.markdown("---")

import requests

import requests

if "json_file" not in st.session_state:
    st.session_state.json_file = None

if st.button("🧾 Download JSON Report"):
    response = requests.get("http://127.0.0.1:5000/download/json")
    if response.status_code == 200:
        st.session_state.json_file = response.content
    else:
        st.error("Failed to fetch JSON report")

if st.session_state.json_file:
    st.download_button(
        label="⬇️ Save JSON Report",
        data=st.session_state.json_file,
        file_name="test_report.json",
        mime="application/json"
    )

if "pdf_file" not in st.session_state:
    st.session_state.pdf_file = None

if st.button("📄 Download PDF Report"):
    response = requests.get("http://127.0.0.1:5000/download/pdf")
    if response.status_code == 200:
        st.session_state.pdf_file = response.content
    else:
        st.error("Failed to fetch PDF report")

if st.session_state.pdf_file:
    st.download_button(
        label="⬇️ Save PDF Report",
        data=st.session_state.pdf_file,
        file_name="test_report.pdf",
        mime="application/pdf"
    )

    st.success(f"Pass %: {summary['pass_percentage']}%")
