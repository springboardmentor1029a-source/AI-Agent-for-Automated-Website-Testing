import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import json
from datetime import datetime


# ---------- MILESTONE 2: PARSING ----------
def instruction_parser(text):
    steps = text.lower().split(",")
    parsed_steps = []

    for step in steps:
        step = step.strip()

        if step.startswith("open"):
            parsed_steps.append({
                "action": "open",
                "target": step.replace("open", "").strip()
            })

        elif "search" in step:
            parsed_steps.append({
                "action": "search",
                "value": step.replace("search for", "").strip()
            })

        elif "click" in step:
            parsed_steps.append({
                "action": "click",
                "target": step.replace("click on", "").strip()
            })

    return parsed_steps


# ---------- MILESTONE 2: MAPPING ----------
def map_to_commands(parsed_steps):
    return {
        "steps": parsed_steps,
        "total_steps": len(parsed_steps)
    }


# ---------- INTELLIGENT ROUTING ----------
def decide_website(search_query):
    product_keywords = [
        "iphone", "mobile", "laptop", "headphones",
        "watch", "tv", "shoes", "camera"
    ]

    for keyword in product_keywords:
        if keyword in search_query.lower():
            return "amazon"

    return "google"


# ---------- MILESTONE 3 & 4: EXECUTION ----------
def run_browser_test(search_query):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    screenshots = []

    if not os.path.exists("screenshots"):
        os.makedirs("screenshots")

    website = decide_website(search_query)

    # GOOGLE
    if website == "google":
        driver.get("https://www.google.com")
        time.sleep(3)

        shot1 = "screenshots/google_home.png"
        driver.save_screenshot(shot1)
        screenshots.append(shot1)

        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys(search_query)
        search_box.send_keys(Keys.RETURN)
        time.sleep(4)

        shot2 = "screenshots/google_results.png"
        driver.save_screenshot(shot2)
        screenshots.append(shot2)

    # AMAZON
    else:
        driver.get("https://www.amazon.in")
        time.sleep(4)

        shot1 = "screenshots/amazon_home.png"
        driver.save_screenshot(shot1)
        screenshots.append(shot1)

        search_box = driver.find_element(By.ID, "twotabsearchtextbox")
        search_box.send_keys(search_query)
        search_box.send_keys(Keys.RETURN)
        time.sleep(5)

        shot2 = "screenshots/amazon_results.png"
        driver.save_screenshot(shot2)
        screenshots.append(shot2)

    driver.quit()

    report = {
        "test_name": "Intelligent Website Routing Test",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "search_query": search_query,
        "website_chosen": website,
        "screenshots": screenshots,
        "status": "SUCCESS"
    }

    with open("test_report.json", "w") as f:
        json.dump(report, f, indent=4)

    return screenshots, website


# ---------- STREAMLIT UI ----------
st.set_page_config(page_title="AI Agent for Automated Website Testing", layout="centered")

st.title("AI Agent for Automated Website Testing")
st.caption(
    "Rule-based fallback mode • Intelligent routing • Automated browser execution • Screenshot-based evidence"
)

st.write(
    "This application accepts natural language test instructions, "
    "parses them into structured actions, and executes automated tests on the appropriate website."
)

user_input = st.text_area(
    "Enter test steps in natural language:",
    placeholder="Example: Open Google, search for Infosys"
)


# ---------- PARSING ----------
if st.button("Run Test"):
    if user_input.strip() == "":
        st.warning("Please enter test steps.")
    else:
        parsed_output = instruction_parser(user_input)
        mapped_output = map_to_commands(parsed_output)

        st.success("Test parsed successfully!")

        st.subheader("Parsed Output")
        st.json(parsed_output)

        st.subheader("Mapped Commands")
        st.json(mapped_output)


# ---------- EXECUTION ----------
if st.button("Run Automated Test"):
    if user_input.strip() == "":
        st.warning("Please enter test steps.")
    else:
        parsed_output = instruction_parser(user_input)

        search_value = None
        for step in parsed_output:
            if step["action"] == "search":
                search_value = step.get("value")
                break

        if not search_value:
            st.error("No search step found.")
        else:
            screenshots, website = run_browser_test(search_value)

            st.success(f"Automated test executed on {website.upper()}")

            for img in screenshots:
                st.image(img, caption=img.split("/")[-1])

            st.code("test_report.json generated")
