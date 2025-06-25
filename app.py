import streamlit as st
from streamlit_chat import message

# --- Page Config ---
st.set_page_config(page_title="DOT Bot", layout="centered")
st.markdown('<style>' + open('styles.css').read() + '</style>', unsafe_allow_html=True)

# --- Compact Header ---
st.markdown("<div class='chat-title'>🤖 DOT Bot</div>", unsafe_allow_html=True)

# --- Message State ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "👋 Hi, I'm **Mira**, your GDOT specs explorer! How can I assist you with Georgia’s transportation standards today?"}
    ]

# --- Show Messages ---
for i, msg in enumerate(st.session_state.messages):
    message(msg["content"], is_user=(msg["role"] == "user"), key=str(i))

# --- Input Box ---
user_input = st.chat_input("Type your question here...")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Placeholder Bot Logic
    bot_response = f"📘 You asked: **{user_input}**\n\nLet me fetch the most accurate GDOT specification for you..."
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
    st.rerun()



# import streamlit as st
# from streamlit_chat import message

# st.set_page_config(page_title="DOTBot Demo", page_icon="🚧", layout="centered")
# st.markdown('<style>' + open('styles.css').read() + '</style>', unsafe_allow_html=True)

# st.markdown("<div class='chat-title'>🤖 DOTBot 1.2 (Demo) – GDOT Assistant</div>", unsafe_allow_html=True)

# if "selected_module" not in st.session_state:
#     st.session_state.selected_module = "GDOT Specifications"

# st.session_state.selected_module = st.selectbox(
#     "📦 Select a module to search:",
#     ["Contractor Directory", "Construction Standards", "GDOT Specifications"],
#     index=["Contractor Directory", "Construction Standards", "GDOT Specifications"].index(st.session_state.selected_module)
# )

# placeholder_text = {
#     "Contractor Directory": "Search for contractors, work classes, or expiry details...",
#     "Construction Standards": "Search for construction standard IDs or descriptions...",
#     "GDOT Specifications": "Search for specification sections (e.g., Section 149)..."
# }

# if "messages" not in st.session_state:
#     st.session_state.messages = [
#         {"role": "assistant", "content": "👋 Hi! I'm Mira, your GDOT Assistant. Please choose a module and ask your question."}
#     ]

# for i, msg in enumerate(st.session_state.messages):
#     message(msg["content"], is_user=(msg["role"] == "user"), key=str(i))

# query = st.chat_input(placeholder_text[st.session_state.selected_module])

# if query:
#     module = st.session_state.selected_module
#     st.session_state.messages.append({"role": "user", "content": query})

#     if module == "Contractor Directory":
#         results = search_contractors(query)
#         if results:
#             response = "\n\n".join(
#                 [f"🏗️ **{r['name']}** – Work Class: {r['class']}, Expiry: {r['expiry']}" for r in results]
#             )
#         else:
#             response = "⚠️ No matching contractors found."

#     elif module == "Construction Standards":
#         results = search_standards(query)
#         if results:
#             sections = []
#             for r in results:
#                 desc = clean_description(r["description"])
#                 image_url = f"https://raw.githubusercontent.com/tejadev23/DOTBot/main/data/standards/{r['files'][0]['filename']}"
#                 sections.append(
#                     f"📄 **{r['standard_id']}** – {desc}\n[🔗 View Image]({image_url})"
#                 )
#             response = "### 📐 Construction Standards\n\n" + "\n\n".join(sections)
#         else:
#             response = "⚠️ No matching standards found."

#     elif module == "GDOT Specifications":
#         results = search_specifications(query)
#         if results:
#             response = show_specification_results(results, return_text=True)
#         else:
#             response = "⚠️ No matching specifications found."

#     st.session_state.messages.append({"role": "assistant", "content": response})
#     st.rerun()
