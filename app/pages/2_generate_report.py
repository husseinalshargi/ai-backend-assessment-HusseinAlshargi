from Home import st
import requests #to get or post data through apis
import urllib.parse

st.title("Generate DOCX Summary Report")


api_key = st.text_input("Enter your API Key:", type="password") #currently ask the user for the api key here (could improve later)



#first thing is to take info from the user to create the report 
title = st.text_input("Enter Report Title:").strip()
sections = st.text_area("Sections (seperate by using ' , ' ):").split(',')
prompt_context = st.text_area("Enter Prompt Context:").strip()
tenant = st.text_input("Enter Tenant Name:").strip()

if st.button("Generate Report"):
    if not api_key.strip():
        st.error("API Key is required.")
    elif not (title and prompt_context and tenant):
        st.error("Title, Prompt Context, and Tenant are required.")
    else:
        #data in json form with the requirements to generate a document
        data = {
            "title": title,
            "sections": sections,
            "prompt_context": prompt_context,
            "tenant": tenant,
        }
        headers = {"X-API-Key": api_key} #to pass the key inside the header

        response = requests.post("http://localhost:8000/api/user/report/generate", json=data, headers=headers) #to return a request obj to know if it was a success and return info after

        if response.ok:
            st.success("Report generated..")
            result = response.json()
            st.session_state.report_id = result["report_id"]
            st.session_state.report_title = result["report_title"]
            st.session_state.api_key = api_key  # save key for reuse
        else:
            st.error(f"Error: {response.text}")

if "report_id" in st.session_state and "report_title" in st.session_state:
    headers = {"X-API-Key": st.session_state.api_key}
    encoded_report_title = urllib.parse.quote(st.session_state.report_title)

    download_url = f"http://localhost:8000/api/user/report/{st.session_state.report_id}/{encoded_report_title}/download"
    response = requests.get(download_url, headers=headers)

    if response.ok:
        file_bytes = response.content
        filename = f"{st.session_state.report_title}.docx" 

        st.download_button(
            label="Download Report",
            data=file_bytes,
            file_name=filename,
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",  # or adjust as needed
        )
    else:
        st.error("Download failed: Invalid API key or report not ready.")
    