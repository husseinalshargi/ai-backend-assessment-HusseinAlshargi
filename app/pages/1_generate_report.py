from Home import st
import requests #to get or post data through apis


st.title("Generate DOCX Summary Report")

#first thing is to take info from the user to create the report 
title = st.text_input("Enter Report Title:").strip()
sections = st.text_area("Sections (seperate by using ' , ' ):").split(',')
prompt_context = st.text_area("Enter Prompt Context:").strip()
tenant = st.text_input("Enter Tenant Name:").strip()

if st.button("Generate Report"):
    if title and prompt_context and tenant: #important inputs isn't empty
        #data in json form with the requirements to generate a document
        data = {
            "title": title,
            "sections": sections,
            "prompt_context": prompt_context,
            "tenant": tenant,
        }

        response = requests.post("http://localhost:8000/api/report/generate", json=data) #to return a request obj to know if it was a success and return info after

        if response.ok:
            st.success("Report generated..")
            result = response.json()
            st.session_state.report_id = result["report_id"]
            st.session_state.report_title = result["report_title"]
            download_url = f"http://localhost:8000/api/report/{st.session_state.report_id}/{st.session_state.report_title}/download"
            st.link_button(
            label="Download Report", #text displayed on the button
                url=download_url,           
                help="Click to download the generated report", #optional tooltip
                type="primary" #(highlighted) button
            )

        else:
            st.error(f"Error: {response.text}")
    else:
        st.error("Error: Title, Prompt Context, and Tenant shouldn't be empty")
