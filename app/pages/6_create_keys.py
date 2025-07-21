from Home import st
import requests

st.title("Create New API Key")


api_key = st.text_input("Enter your Admin API Key:", type="password")


role = st.selectbox("Select Role for this Key:", options=["admin", "user"])
owner_email = st.text_input("Email:")


if st.button("Create API Key"):
    if not api_key.strip():
        st.error("Admin API Key is required.")
    elif not owner_email.strip():
        st.error("Email is required.")
    else:
        data = {
            "owner_email": owner_email.strip(),
            "role": role
            }

        headers = {"X-API-Key": api_key.strip()}

        try:
            response = requests.post("http://localhost:8000/api/admin/keys/create_key", json=data, headers=headers)
            if response.ok:
                result = response.json()
                st.success("API Key created successfully!")
                st.code(result["api_key"], language="text")
                st.info("Copy the key now. It won't be shown again.")
            else:
                st.error(f"Error: {response.status_code} - {response.text}")
        except Exception as e:
            st.error(f"Could not connect: {e}")

