import datetime
from Home import st
import requests

st.title("AI Assistant --- Ask a Question")

api_key = st.text_input("Enter your API Key:", type="password") #currently ask the user for the api key here (could improve later)


question = st.text_input("Ask your question:").strip()
tenant = st.text_input("Tenant (optional):").strip()
file_name = st.text_input("File name (optional):").strip()
from_date = st.date_input("From date (optional):", value=None)
to_date = st.date_input("To date (optional):", value=None)

#if the question and key isn't empty and the button is pressed
if st.button("Get Answer"): 
    if api_key.strip() and question:
        with st.spinner("Thinking..."): #until the the answer comes
            try:
                headers = {"X-API-Key": api_key} #to pass the key inside the header

                #build request payload to pass to the api call
                payload = {
                    "query": question,
                    "tenant": tenant or None,
                    "file_name": file_name or None,
                    "from_date": datetime.combine(from_date, datetime.min.time()).isoformat() if from_date else None,
                    "to_date": datetime.combine(to_date, datetime.min.time()).isoformat() if to_date else None,
                    "conversation_id": "default"
                }

                #send POST request
                response = requests.post("http://localhost:8000/api/user/chat", json=payload, headers=headers)

                if response.ok and response.json():
                    result = response.json()
                    st.subheader("Answer:")
                    st.success(result.get("answer", "No answer returned."))

                    # Display metadata separately
                    with st.expander("More Info"):
                        st.markdown(f"**Conversation ID:** `{result.get('conversation_id')}`")
                        st.markdown(f"**Latency:** `{result.get('latency_ms')} ms`")
                        st.markdown(f"**Tokens In:** `{result.get('tokens_in')}`")
                        st.markdown(f"**Tokens Out:** `{result.get('tokens_out')}`")

                        sources = result.get("sources", [])
                        if sources:
                            st.markdown("**Sources:**")
                            for source in sources:
                                st.markdown(f"- `{source.get('source')}` (score: `{source.get('score')}`)")
                        else:
                            st.markdown("**Sources:** None")
                else:
                    st.error(f"Error: {response.text}")
            except Exception as e:
                st.error(f"Request failed: {str(e)}")
    else:
        st.error(f"Please enter a valid api key and a question")
