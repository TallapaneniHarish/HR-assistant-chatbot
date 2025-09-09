# frontend_streamlit.py
import streamlit as st
import requests

API_BASE = "http://localhost:8000"  # change if your API is elsewhere

st.title("HR Finder — Chat")

query = st.text_input("Ask something (e.g. 'Find Python developers with 3+ years experience')")

k = st.slider("Number of candidates to return", 1, 8, 3)

if st.button("Search"):
    if not query.strip():
        st.warning("Please enter a query.")
    else:
        try:
            with st.spinner("Searching..."):
                r = requests.post(f"{API_BASE}/chat", json={"query": query, "k": k})
                r.raise_for_status()
                resp = r.json()
                st.markdown("### Assistant response")
                st.markdown(resp.get("response_text", ""))
                st.markdown("### Candidates")
                for c in resp.get("candidates", []):
                    st.markdown(f"**{c['name']}** — {c['experience_years']} yrs — {c['availability']}")
                    st.markdown(f"Skills: {', '.join(c['skills'])}")
                    st.markdown(f"Projects: {', '.join(c['projects'])}")
                    st.markdown("---")
        except Exception as e:
            st.error(f"Error contacting API: {e}")
