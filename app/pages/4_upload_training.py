from Home import st
import requests

st.title("Upload Training Document")

st.info("Only `.txt` and `.json` files are accepted for training.")

tenant = st.text_input("Tenant Name")

uploaded_file = st.file_uploader("Upload a `.txt` or `.json` file", type=["txt", "json"])

if st.button("Upload") and uploaded_file and tenant:
    with st.spinner("Uploading... Please wait."):
        try:
            #prepare the form data
            files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
            data = {"tenant": tenant}

            response = requests.post(
                "http://localhost:8000/api/training/accept",
                files=files,
                data=data
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
