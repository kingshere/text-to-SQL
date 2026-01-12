# -----------------------------------
# Environment Setup
# -----------------------------------
from dotenv import load_dotenv
load_dotenv()

import os
import sqlite3
import streamlit as st
from google import genai

# -----------------------------------
# Gemini Client Configuration
# -----------------------------------
client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)

MODEL_NAME = os.getenv(
    "GEMINI_MODEL",
    "models/gemini-flash-lite-latest"  # Free-tier safe
)

# -----------------------------------
# Prompt Definition
# -----------------------------------
prompt = [
    """
Convert the following English question into a valid SQLite SQL query.

Database: STUDENT
Columns:
- NAME (TEXT)
- CLASS (TEXT)
- SECTION (TEXT)
- MARKS (INTEGER)

Rules:
- Return ONLY the SQL query
- Do NOT add explanations
- Do NOT use ``` or the word SQL
- Only SELECT queries are allowed

Examples:
Q: How many students are present?
A: SELECT COUNT(*) FROM STUDENT;

Q: Show students studying Data Science
A: SELECT * FROM STUDENT WHERE CLASS = "Data Science";
"""
]

# -----------------------------------
# Gemini → SQL Function
# -----------------------------------
def get_gemini_response(question, prompt):
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt[0] + "\n\n" + question
    )
    return response.text.strip()

# -----------------------------------
# SQL Execution Function
# -----------------------------------
def read_sql_query(sql, db="student.db"):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.close()
    return rows

# -----------------------------------
# Streamlit Page Config
# -----------------------------------
st.set_page_config(
    page_title="AI Text-to-SQL",
    page_icon="🧠",
    layout="wide"
)

# -----------------------------------
# Sidebar
# -----------------------------------
with st.sidebar:
    st.title("🧠 Text-to-SQL AI")
    st.markdown(
        """
        Ask questions in plain English and
        query a SQLite database using Gemini.

        **Tech Stack**
        - Gemini LLM
        - SQLite
        - Streamlit
        """
    )
    st.divider()
    st.caption("Running on Gemini Free Tier")

    with st.expander("📋 Database Schema"):
        st.code(
            """
STUDENT(
  NAME TEXT,
  CLASS TEXT,
  SECTION TEXT,
  MARKS INTEGER
)
            """
        )

# -----------------------------------
# Main UI
# -----------------------------------
st.markdown("### Ask questions about the database")

col1, col2 = st.columns([5, 1], vertical_alignment="center")

with col1:
    question = st.text_input(
        label="Your question",
        placeholder="e.g. List students with marks above 80",
        label_visibility="visible"
    )

with col2:
    st.markdown("<br>", unsafe_allow_html=True)  # vertical alignment fix
    submit = st.button("Run Query", use_container_width=True)


# -----------------------------------
# Example Queries
# -----------------------------------
st.markdown("**Try these examples:**")
example_cols = st.columns(3)

examples = [
    "How many students are present?",
    "Show students studying Data Science",
    "List students with marks above 80"
]

for col, ex in zip(example_cols, examples):
    if col.button(ex):
        question = ex

# -----------------------------------
# Query Processing
# -----------------------------------
if submit and question:
    with st.spinner("Generating SQL and querying database..."):
        try:
            sql_query = get_gemini_response(question, prompt)

            # Safety check
            forbidden = ["drop", "delete", "update", "insert", "alter"]
            if any(word in sql_query.lower() for word in forbidden):
                st.error("Unsafe SQL detected. Only SELECT queries are allowed.")
                st.stop()

            # Show generated SQL
            st.markdown("### Generated SQL")
            st.code(sql_query, language="sql")

            # Execute query
            results = read_sql_query(sql_query)

            # Show results
            st.markdown("### Query Results")
            if results:
                st.dataframe(results, use_container_width=True)
            else:
                st.info("No records found.")

        except Exception as e:
            st.error(f"Error: {e}")

elif submit:
    st.warning("Please enter a question.")
