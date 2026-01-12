## Text-to-SQL with Google Gemini (Streamlit App)

An AI-powered Text-to-SQL application that converts natural language questions into SQL queries using Google Gemini, executes them on a SQLite database, and displays the results via a Streamlit web interface.

This project demonstrates practical LLM integration for database querying and serves as a foundation for agentic data-access systems.

## 🚀 Features

Natural language → SQL query conversion using Google Gemini (gemini-pro)

Executes generated SQL queries on a SQLite database

Interactive Streamlit UI

Environment-variable–based API key management

Simple, extensible architecture for LLM-powered data tools

## 🧠 How It Works

User enters a question in plain English

Google Gemini converts the question into a valid SQL query

The query runs against a local SQLite database

Results are returned and displayed in the UI

## 📦 Tech Stack

Python

Streamlit – UI framework

Google Gemini API – LLM for SQL generation

SQLite – Lightweight relational database

python-dotenv – Environment variable management

## 🔧 Prerequisites

Python 3.9+

VS Code (recommended)

Google Gemini API Key