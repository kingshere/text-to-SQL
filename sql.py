from dotenv import load_dotenv
load_dotenv()

import os
import sqlite3
import streamlit as st
from google import genai

# -------------------------------
# Gemini Client Configuration
# -------------------------------
client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)
MODEL_NAME = "models/gemini-flash-lite-latest"


# -------------------------------
# Gemini → SQL Function
# -------------------------------
def get_gemini_response(question, prompt):
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt[0] + "\n\n" + question
    )
    return response.text.strip()

# -------------------------------
# SQL Execution Function
# -------------------------------
def read_sql_query(sql, db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    return rows

# -------------------------------
# Prompt Definition
# -------------------------------
prompt = [
    """
You are an expert in converting English questions into SQL queries.

The SQLite database is named STUDENT with the following columns:
NAME, CLASS, SECTION, MARKS

Rules:
- Output ONLY the SQL query
- Do NOT add explanations
- Do NOT use ``` or the word SQL

Examples:
Q: How many students are present?
A: SELECT COUNT(*) FROM STUDENT;

Q: Show students studying Data Science
A: SELECT * FROM STUDENT WHERE CLASS = "Data Science";
"""
]

# -------------------------------
# Streamlit UI
# -------------------------------
st.set_page_config(page_title="Text to SQL with Gemini")
st.header("Gemini Text-to-SQL App")

question = st.text_input("Ask a question about the database:")

if st.button("Generate & Execute SQL"):
    try:
        sql_query = get_gemini_response(question, prompt)
        st.subheader("Generated SQL")
        st.code(sql_query)

        results = read_sql_query(sql_query, "student.db")

        st.subheader("Query Results")
        if results:
            st.dataframe(results)
        else:
            st.info("No results found.")

    except Exception as e:
        st.error(f"Error: {e}")
