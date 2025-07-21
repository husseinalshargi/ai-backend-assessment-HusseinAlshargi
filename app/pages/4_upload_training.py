from Home import st
import requests

st.title("Upload Training Document")

st.info("Only `.txt` and `.json` files are accepted for training.")

api_key = st.text_input("Enter your API Key:", type="password") #currently ask the user for the api key here (could improve later)


tenant = st.text_input("Tenant Name")

uploaded_file = st.file_uploader("Upload a `.txt` or `.json` file", type=["txt", "json"])

if st.button("Upload") and uploaded_file and tenant:
    if not api_key.strip():
        st.error("API Key is required.")
    else:
        with st.spinner("Uploading... Please wait."):
            try:
                headers = {"X-API-Key": api_key} #to pass the key inside the header

                #prepare the form data
                files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
                data = {"tenant": tenant}

                response = requests.post(
                    "http://localhost:8000/api/user/training/accept",
                    files=files,
                    data=data,
                    headers=headers
                )

                if response.ok:
                    result = response.json()
                    st.success(f"File uploaded: {result['filename']}")
                else:
                    st.error(f"Upload failed: {response.text}")
            except Exception as e:
                st.error(f"Error: {str(e)}")
else:
    st.caption("Make sure both Tenant Name and a valid file are provided.")
