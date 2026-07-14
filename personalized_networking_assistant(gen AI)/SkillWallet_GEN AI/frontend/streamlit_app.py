
import streamlit as st
import requests
from datetime import datetime

BACKEND_URL = "http://127.0.0.1:8000"

def configure_page():
    """Set Streamlit page title, icon, and layout."""
    st.set_page_config(
        page_title="Personalized Networking Assistant",
        page_icon="🤝",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Inject custom styling for rich aesthetics
    st.markdown("""
        <style>
        /* Main Styling */
        .main {
            background-color: #0e1117;
            color: #ffffff;
        }
        /* Title design */
        .title-container {
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            padding: 2rem;
            border-radius: 12px;
            margin-bottom: 2rem;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
            text-align: center;
        }
        .title-text {
            color: #ffffff !important;
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
            font-family: 'Outfit', sans-serif;
        }
        .subtitle-text {
            color: #e0e0e0;
            font-size: 1.1rem;
        }
        /* Cards styling */
        .custom-card {
            background-color: #1a1c23;
            border: 1px solid #2d3139;
            padding: 1.5rem;
            border-radius: 10px;
            margin-bottom: 1rem;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .custom-card:hover {
            border-color: #4a90e2;
            box-shadow: 0 6px 12px rgba(74, 144, 226, 0.2);
            transition: all 0.3s ease;
        }
        .badge-verified {
            background-color: #2e7d32;
            color: white;
            padding: 0.2rem 0.6rem;
            border-radius: 4px;
            font-size: 0.8rem;
            font-weight: bold;
        }
        .badge-unverified {
            background-color: #c62828;
            color: white;
            padding: 0.2rem 0.6rem;
            border-radius: 4px;
            font-size: 0.8rem;
            font-weight: bold;
        }
        </style>
    """, unsafe_allow_html=True)


# ──────────────────────────────────────────────
# Sidebar
# ──────────────────────────────────────────────

def render_sidebar():
    """Render the sidebar with user input fields."""
    st.sidebar.image("https://img.icons8.com/clouds/200/handshake.png", width=120)
    st.sidebar.title("🎯 Assistant Panel")
    st.sidebar.write("Configure your next networking event to get tailored discussion topics.")

    event_name = st.sidebar.text_input(
        "📅 Event Name",
        placeholder="e.g., Global AI Summit 2026",
        help="The name or title of the professional networking event."
    )

    user_role = st.sidebar.text_input(
        "💼 Your Professional Role",
        placeholder="e.g., Senior AI Research Scientist",
        help="Your current job role or designation."
    )

    interests_input = st.sidebar.text_area(
        "💡 Your Interests / Keywords",
        placeholder="e.g., Deep Learning, MLOps, LLMs, Python",
        help="Enter interests separated by commas."
    )

    # Process interests list
    user_interests = [i.strip() for i in interests_input.split(",") if i.strip()]

    st.sidebar.markdown("---")
    generate_button = st.sidebar.button("🚀 Generate Topics", use_container_width=True)
    analyze_button = st.sidebar.button("🔍 Analyze Event Only", use_container_width=True)

    return event_name, user_role, user_interests, generate_button, analyze_button


# ──────────────────────────────────────────────
# Main Content Area
# ──────────────────────────────────────────────

def render_topics(topics: list):
    """Display generated conversation topics in the main area."""
    if not topics:
        st.info("No topics generated yet.")
        return

    st.subheader("💡 Tailored Conversation Starters")
    for i, topic_data in enumerate(topics):
        topic_title = topic_data.get("topic", "")
        talking_points = topic_data.get("talking_points", [])
        status = topic_data.get("fact_check_status", "unverified")

        badge_class = "badge-verified" if status == "verified" else "badge-unverified"

        st.markdown(f"""
            <div class="custom-card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                    <h3 style="margin: 0; color: #4a90e2;">Topic {i+1}: {topic_title}</h3>
                    <span class="{badge_class}">{status.upper()}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

        cols = st.columns(len(talking_points) if talking_points else 1)
        for idx, pt in enumerate(talking_points):
            with cols[idx]:
                st.markdown(f"**💬 Point {idx+1}: {pt.get('point', '')}**")
                st.info(pt.get("details", ""))


def render_history():
    """Display past conversation history."""
    st.subheader("📜 Conversation History Log")
    try:
        response = requests.get(f"{BACKEND_URL}/history")
        if response.status_code == 200:
            history_data = response.json()
            if not history_data:
                st.info("No past sessions found in history.json.")
                return

            # Display newest first
            for item in reversed(history_data):
                dt_str = item.get("timestamp", "")
                try:
                    dt = datetime.fromisoformat(dt_str)
                    formatted_dt = dt.strftime("%Y-%m-%d %H:%M:%S")
                except Exception:
                    formatted_dt = dt_str

                with st.expander(f"📅 {item.get('event_name', 'Event')} — {formatted_dt} (ID: {item.get('conversation_id', 'N/A')[:8]}...)"):
                    st.json(item)
        else:
            st.error(f"Failed to load history (Status Code: {response.status_code})")
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to FastAPI server. Please ensure the backend is running.")


# ──────────────────────────────────────────────
# Feedback Section
# ──────────────────────────────────────────────

def render_feedback_form():
    """Render the feedback submission form."""
    st.subheader("💬 Session Feedback")
    st.write("Help us improve by providing feedback on your generated conversation topics.")

    with st.form("feedback_form_inputs"):
        conversation_id = st.text_input("🔑 Conversation Session ID", placeholder="Paste the unique Session ID here")
        rating = st.slider("⭐ Rating", min_value=1, max_value=5, value=5, help="Rate the quality of talking points.")
        comments = st.text_area("📝 Comments / Recommendations", placeholder="Add any details or suggestions here...")

        submit_btn = st.form_submit_button("Submit Feedback", type="primary")

    if submit_btn:
        if not conversation_id.strip():
            st.warning("Please enter a valid Conversation ID.")
            return

        payload = {
            "conversation_id": conversation_id.strip(),
            "rating": rating,
            "comments": comments.strip()
        }

        try:
            response = requests.post(f"{BACKEND_URL}/feedback", json=payload)
            if response.status_code == 200:
                st.success("✅ Feedback successfully logged. Thank you!")
            else:
                st.error(f"Error logging feedback: {response.text}")
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to FastAPI server. Please check the backend service status.")


# ──────────────────────────────────────────────
# Main Page Entry Point
# ──────────────────────────────────────────────

def main():
    """Main function to run the Streamlit application."""
    configure_page()

    # Header section
    st.markdown("""
        <div class="title-container">
            <div class="title-text">🤝 Personalized Networking Assistant</div>
            <div class="subtitle-text">Generative AI-Powered Conversation Topics tailored to your professional networking events</div>
        </div>
    """, unsafe_allow_html=True)

    # Sidebar inputs
    event_name, user_role, user_interests, generate_button, analyze_button = render_sidebar()

    # Define Tabs
    tab_gen, tab_hist, tab_feed, tab_chk = st.tabs([
        "🚀 Conversation Assistant",
        "📜 History Log",
        "💬 User Feedback",
        "🔍 Wikipedia Fact-Checker"
    ])

    # ── Tab 1: Generation & Event Analysis ──
    with tab_gen:
        if generate_button:
            if not event_name.strip() or not user_role.strip():
                st.warning("⚠️ Both Event Name and Professional Role are required to generate topics.")
            else:
                with st.spinner("🧠 Analyzing event details and generating personalized talking points using DistilBERT & GPT-2..."):
                    payload = {
                        "event_name": event_name.strip(),
                        "user_role": user_role.strip(),
                        "user_interests": user_interests
                    }
                    try:
                        response = requests.post(f"{BACKEND_URL}/generate-conversation", json=payload)
                        if response.status_code == 200:
                            data = response.json()
                            st.success("🎉 Conversation starters generated successfully!")
                            st.subheader("🔑 Session ID")
                            st.code(data.get("conversation_id", ""), language="text")

                            render_topics(data.get("topics", []))
                        else:
                            st.error(f"Backend Server Error: {response.text}")
                    except requests.exceptions.ConnectionError:
                        st.error("Unable to connect to backend server. Make sure FastAPI server is running on port 8000.")

        elif analyze_button:
            if not event_name.strip() or not user_role.strip():
                st.warning("⚠️ Both Event Name and Professional Role are required for event analysis.")
            else:
                with st.spinner("🔍 Running classification and semantic analysis..."):
                    payload = {
                        "event_name": event_name.strip(),
                        "user_role": user_role.strip()
                    }
                    try:
                        response = requests.post(f"{BACKEND_URL}/analyze-event", json=payload)
                        if response.status_code == 200:
                            data = response.json()
                            st.subheader("📊 Event Analysis Result")
                            st.markdown(f"**Audience Profile Recommendation:** {data.get('audience_profile', '')}")

                            st.write("**Extracted Semantics / Themes:**")
                            for theme_item in data.get("themes", []):
                                conf = theme_item.get("confidence", 0.0)
                                st.write(f"- **{theme_item.get('theme', '')}** (Confidence: {conf:.2%})")
                                st.progress(conf)
                        else:
                            st.error(f"Backend Error: {response.text}")
                    except requests.exceptions.ConnectionError:
                        st.error("Unable to connect to backend server.")
        else:
            st.info("👈 Enter your event details in the Sidebar Panel and click **Generate Topics** or **Analyze Event Only**.")

    # ── Tab 2: History Log ──
    with tab_hist:
        render_history()

    # ── Tab 3: Feedback Tab ──
    with tab_feed:
        render_feedback_form()

    # ── Tab 4: Standalone Fact Checker ──
    with tab_chk:
        st.subheader("🔎 Standalone Wikipedia Fact-Verification")
        st.write("Directly verify any specific claims or topics using the Wikipedia knowledge engine.")
        claims_input = st.text_area(
            "Enter claims/topics (one per line)",
            placeholder="e.g.\nQuantum Computing\nArtificial Intelligence\nGoogle DeepMind"
        )
        check_btn = st.button("Verify Claims", type="primary")

        if check_btn:
            claims = [c.strip() for c in claims_input.split("\n") if c.strip()]
            if not claims:
                st.warning("Please enter at least one claim.")
            else:
                with st.spinner("Searching Wikipedia..."):
                    try:
                        resp = requests.post(f"{BACKEND_URL}/fact-check", json={"claims": claims})
                        if resp.status_code == 200:
                            results = resp.json().get("results", [])
                            for r in results:
                                verified = r.get("verified", False)
                                color = "green" if verified else "red"
                                label = "VERIFIED" if verified else "NOT VERIFIED"
                                st.markdown(f"### Claim: **{r.get('claim', '')}** — <span style='color:{color}; font-weight:bold;'>{label}</span>", unsafe_allow_html=True)
                                st.write(f"**Confidence:** {r.get('confidence', 0.0):.2%}")
                                st.write(f"**Summary:** {r.get('summary', '')}")
                                if r.get("source"):
                                    st.write(f"**Source URL:** [{r.get('source')}]({r.get('source')})")
                                st.markdown("---")
                        else:
                            st.error(f"Error checking facts: {resp.text}")
                    except requests.exceptions.ConnectionError:
                        st.error("Could not connect to backend.")
if __name__ == "__main__":
    main()