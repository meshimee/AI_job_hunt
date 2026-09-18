import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
import streamlit as st

from app.database.database import get_connection


st.set_page_config(
    page_title="JobHunt AI",
    page_icon="🎯",
    layout="wide",
)


st.title("🎯 JobHunt AI")
st.subheader("Your AI Job Search Employee")

st.divider()


connection = get_connection()

cursor = connection.cursor()

cursor.execute("""
    SELECT
        id,
        company,
        role,
        source,
        stage,
        status,
        priority,
        next_action
    FROM opportunities
    ORDER BY id DESC
""")

opportunities = cursor.fetchall()

connection.close()


# Summary
total = len(opportunities)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Opportunities", total)

with col2:
    active = sum(
        1 for opportunity in opportunities
        if opportunity["status"] not in ("Rejected", "Closed")
    )
    st.metric("Active", active)

with col3:
    interviews = sum(
        1 for opportunity in opportunities
        if opportunity["stage"] == "Interview"
    )
    st.metric("Interviews", interviews)


st.divider()

st.header("📋 Opportunities")


if not opportunities:
    st.info("No opportunities yet.")
else:
    for opportunity in opportunities:

        with st.container(border=True):

            col1, col2, col3 = st.columns([3, 2, 1])

            with col1:
                st.subheader(
                    f"{opportunity['company']} — "
                    f"{opportunity['role'] or 'Role not specified'}"
                )

                st.write(
                    f"**Source:** {opportunity['source']}  \n"
                    f"**Stage:** {opportunity['stage']}  \n"
                    f"**Status:** {opportunity['status']}"
                )

            with col2:
                st.write(
                    f"**Priority:** "
                    f"{opportunity['priority'] or 'Not set'}"
                )

                st.write(
                    f"**Next Action:** "
                    f"{opportunity['next_action'] or 'Not set'}"
                )

            with col3:
                st.write(f"ID: {opportunity['id']}")