from Home import st
import requests

st.title("Scheduler Control Panel")

st.info("Use the buttons below to manually run scheduled tasks.")


api_key = st.text_input("Enter your API Key:", type="password") #currently ask the user for the api key here (could improve later)



#trigger nightly refresh
if st.button("Run Nightly Refresh now (02:00am default)"):
    if not api_key.strip():
        st.error("API Key is required.")
    else:
        headers = {"X-API-Key": api_key} #to pass the key inside the header

        response = requests.post("http://localhost:8000/api/admin/refresh", headers=headers)
        if response.ok:
            st.success("Nightly refresh completed.")
        else:
            st.error(f"Error: {response.text}")

# Trigger Nightly Evaluation
if st.button("Run Nightly Evaluation now (03:00am default)"):
    if not api_key.strip():
        st.error("API Key is required.")
    else:
        headers = {"X-API-Key": api_key} #to pass the key inside the header

        response = requests.post("http://localhost:8000/api/admin/evaluate", headers=headers)
        if response.ok:
            st.success("Evaluation completed. Check the evaluation_report.md file.")
        else:
            st.error(f"Error: {response.text}")
