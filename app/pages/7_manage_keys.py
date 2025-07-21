from Home import st
import requests

st.title("View & Manage API Keys")

admin_api_key = st.text_input("Enter your Admin API Key:", type="password")

if admin_api_key.strip():
    headers = {"X-API-Key": admin_api_key.strip()}

    # Fetch keys
    try:
        response = requests.get("http://localhost:8000/api/admin/keys/get_keys", headers=headers)
        if response.ok:
            keys = response.json()
            if not keys:
                st.info("No API keys found.")
            else:
                for key_entry in keys:
                    col1, col2, col3, col4 = st.columns([3, 3, 2, 2])
                    with col1:
                        st.text_input("Email", key_entry["owner_email"], disabled=True, key=key_entry["key"] + "_email")
                    with col2:
                        st.text_input("Role", key_entry["role"], disabled=True, key=key_entry["key"] + "_role")
                    with col3:
                        status = "Active" if key_entry["active"] else "Inactive"
                        st.markdown(f"**Status:** {status}")
                    with col4:
                        if key_entry["active"]:
                            if st.button("Deactivate", key=key_entry["key"] + "_deactivate"):
                                deactivate_url = f"http://localhost:8000/api/admin/keys/{key_entry['key']}/deactivate"
                                deact_response = requests.post(deactivate_url, headers=headers)
                                if deact_response.ok:
                                    st.success(f"Key deactivated")
                                    st.rerun()
                                else:
                                    st.error(f"Error: {deact_response.status_code} - {deact_response.text}")
                        else:
                            if st.button("Activate", key=key_entry["key"] + "_activate"):
                                activate_url = f"http://localhost:8000/api/admin/keys/{key_entry['key']}/activate"
                                act_response = requests.post(activate_url, headers=headers)
                                if act_response.ok:
                                    st.success(f"Key activated")
                                    st.rerun()
                                else:
                                    st.error(f"Error: {act_response.status_code} - {act_response.text}")
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        st.error(f"Failed to connect to API: {e}")
else:
    st.warning("Please enter your Admin API Key.")
