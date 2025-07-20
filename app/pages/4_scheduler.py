from Home import st
import requests

st.title("Scheduler Control Panel")

st.info("Use the buttons below to manually run scheduled tasks.")

#trigger nightly refresh
if st.button("Run Nightly Refresh now (02:00am default)"):
    response = requests.post("http://localhost:8000/api/refresh")
    if response.ok:
        st.success("Nightly refresh completed.")
    else:
        st.error(f"Error: {response.text}")

# Trigger Nightly Evaluation
if st.button("Run Nightly Evaluation now (03:00am default)"):
    response = requests.post("http://localhost:8000/api/evaluate")
    if response.ok:
        st.success("Evaluation completed. Check the evaluation_report.md file.")
    else:
        st.error(f"Error: {response.text}")
