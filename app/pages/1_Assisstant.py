import datetime
from Home import st
import requests

st.title("AI Assistant --- Ask a Question")

question = st.text_input("Ask your question:").strip()
tenant = st.text_input("Tenant (optional):").strip()
file_name = st.text_input("File name (optional):").strip()
from_date = st.date_input("From date (optional):", value=None)
to_date = st.date_input("To date (optional):", value=None)


if st.button("Get Answer") and question: #if the question isn't empty and the button is pressed
    with st.spinner("Thinking..."): #until the the answer comes
        try:
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
            response = requests.post("http://localhost:8000/api/ask", json=payload)

            if response.ok and response.json():
                result = response.json()
                st.subheader("Answer:")
                st.success(result)
            else:
                st.error(f"Error: {response.text}")
        except Exception as e:
            st.error(f"Request failed: {str(e)}")
