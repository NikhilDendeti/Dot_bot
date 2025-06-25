import streamlit as st
import json
from openai import OpenAI
from vendor_directory_backend import (
    get_vendor_by_name,
    get_vendor_number,
    get_by_work_class,
    get_expiring_soon
)

OPENAI_API_KEY = "*"
client = OpenAI(api_key=OPENAI_API_KEY)

system_prompt = """
You are a smart assistant for a contractor directory.
Classify each user query into one of the following types:
- 'vendor_details': for full info of a vendor
- 'vendor_number': to find just the vendor number
- 'work_class': to list vendors by a work class code (like 615)
- 'expiring_soon': to list vendors with expiring prequalification

Respond in JSON like:
{
  "query_type": "...",
  "vendor_name": "...",  // or "code": "...", or "days": 90
}
"""

st.set_page_config(page_title="Vendor Directory AI Assistant", layout="wide")
st.title("🔍 Vendor Directory AI Assistant")

user_input = st.text_input("Ask a question about vendors (e.g., 'Details for Kelly Construction')")

if user_input:
    with st.spinner("Thinking..."):
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ]
            )
            message = response.choices[0].message.content.strip()

            try:
                result = json.loads(message)
            except json.JSONDecodeError:
                st.error("Failed to parse GPT response. Raw response:")
                st.code(message)
                st.stop()

            query_type = result.get("query_type")

            if query_type == "vendor_details":
                name = result.get("vendor_name", "")
                vendors = get_vendor_by_name(name)
                if not vendors.empty:
                    st.dataframe(vendors)
                else:
                    st.warning("No vendor found.")

            elif query_type == "vendor_number":
                name = result.get("vendor_name", "")
                number = get_vendor_number(name)
                if number:
                    st.success(f"Vendor Number: {number}")
                else:
                    st.warning("Vendor not found.")

            elif query_type == "work_class":
                code = result.get("code", "")
                vendors = get_by_work_class(code)
                if not vendors.empty:
                    st.dataframe(vendors)
                else:
                    st.warning("No vendors found for this work class.")

            elif query_type == "expiring_soon":
                days = int(result.get("days", 90))
                vendors = get_expiring_soon(days)
                if not vendors.empty:
                    st.dataframe(vendors)
                else:
                    st.warning(f"No vendors expiring in next {days} days.")

            else:
                st.error("Query type not understood. Try rephrasing your question.")

        except Exception as e:
            st.error("An error occurred while processing the request.")
            st.exception(e)
