from flask import Flask, render_template, request, session, redirect, url_for, jsonify
import markdown
import sqlite3
from dotenv import load_dotenv
import os
import google.generativeai as genai

app = Flask(__name__)

# Load environment variables from .env (only in development)
if os.getenv("FLASK_ENV") != "production":
    load_dotenv("secret.env")

# Set the secret key (use env variable or generate dynamically for development)
app.secret_key = os.getenv("SECRET_KEY", os.urandom(24))
if os.getenv("FLASK_ENV") == "production" and not os.getenv("SECRET_KEY"):
    raise ValueError("SECRET_KEY must be set in production!")

# Retrieve the API key from the environment
api_key = os.getenv("api_key")
if not api_key:
    raise ValueError("API key is missing. Check your environment variables.")

# Configure the Gemini API
genai.configure(api_key=api_key)

# Initialize the generative model
model = genai.GenerativeModel(model_name="gemini-1.5-flash")  # Replace with your specific model name


# Dictionary mapping version abbreviations to full names
VERSION_NAMES = {
    "ar_svd": "Arabic - The Arabic Bible",
    "zh_cuv": "Chinese - Chinese Union Version",
    "zh_ncv": "Chinese - New Chinese Version",
    "de_schlachter": "German - Schlachter",
    "el_greek": "Greek - Modern Greek",
    "en_bbe": "English - Basic English",
    "en_kjv": "English - King James Version",
    "eo_esperanto": "Esperanto - Esperanto",
    "es_rvr": "Spanish - Reina Valera",
    "fi_finnish": "Finnish - Finnish Bible",
    "fi_pr": "Finnish - Pyhä Raamattu",
    "fr_apee": "French - Le Bible de l'Épée",
    "ko_ko": "Korean - Korean Version",
    "pt_aa": "Portuguese - Almeida Revisada Imprensa Bíblica",
    "pt_acf": "Portuguese - Almeida Corrigida e Revisada Fiel",
    "pt_nvi": "Portuguese - Nova Versão Internacional",
    "ro_cornilescu": "Romanian - Versiunea Dumitru Cornilescu",
    "ru_synodal": "Russian - Синодальный перевод",
    "vi_vietnamese": "Vietnamese - Tiếng Việt"
}


def generate_dynamic_summary(query, results, language):
    """Generate a dynamic summary of Bible verses using Gemini."""
    verses = " ".join([f"{row['book']} {row['chapter']}:{row['verse']} - {row['text']}" for row in results])

    prompt = (
        f"Summarize the occurrences of the word '{query}' in the following Bible verses: "
        f"{verses}. Provide a concise, insightful summary in {language}."
    )

    try:
        response = model.generate_content(
            contents=prompt,
            generation_config=genai.GenerationConfig(max_output_tokens=1024)
        )
        # Convert Markdown-style text to HTML
        html_summary = markdown.markdown(response.text)
        return html_summary
    
    except Exception as e:
        print(f"Error generating dynamic summary: {e}")
        return "Could not generate a summary. Please try again later."

def get_db_connection():
    """Establish a connection to the SQLite database."""
    conn = sqlite3.connect("bible.db")
    conn.row_factory = sqlite3.Row
    return conn

def get_scripture(query, version="en_kjv"):
    """Search for Bible verses matching the query and version."""
    with get_db_connection() as conn:
        cursor = conn.cursor()

        # Fetch matching verses
        cursor.execute(
            """
            SELECT book, chapter, verse, text
            FROM bible
            WHERE text LIKE ? AND version = ?
            """,
            (f"%{query}%", version)
        )
        results = cursor.fetchall()

        # Count occurrences
        cursor.execute(
            """
            SELECT COUNT(*)
            FROM bible
            WHERE text LIKE ? AND version = ?
            """,
            (f"%{query}%", version)
        )
        occurrence_count = cursor.fetchone()[0]

    return results, occurrence_count


def ask_gemini(query, language="English"):
    try:
        prompt = (
            f"You are a helpful assistant specializing in the Bible. "
            f"Your primary role is to answer questions about the Bible with scriptural references. "
            f"All responses should align with Christian theology and use the {language} language. "
            f"Be clear and concise. Here is the question: {query}"
        )

        response = model.generate_content(
            contents=prompt,
            generation_config=genai.GenerationConfig(max_output_tokens=1024)  # Increased limit
        )
        print(f"Generated response: {response.text}")  # Debugging
        return response.text
    except Exception as e:
        print(f"Error with Gemini API: {e}")
        return "Error retrieving response. Please try again later."

@app.route("/about")
def about():
    """Information about the chatbot and credits."""
    return render_template("about.html")

@app.route("/", methods=["GET", "POST"])
def select_language():
    """Allow users to select their preferred language for the site."""
    if request.method == "POST":
        selected_language = request.form.get("language")
        session["language"] = selected_language
        return redirect(url_for("query_scripture"))

    return render_template("select_language.html")

@app.route("/query", methods=["GET", "POST"])
def query_scripture():
    """Allow users to input a query and select their preferred Bible version."""
    # Clear session data on GET request
    if request.method == "GET":
        session.pop("query", None)
        session.pop("version", None)

    language = session.get("language", "English")

    if request.method == "POST":
        query = request.form.get("query")
        version = request.form.get("version", "en_kjv")

        # Store query in session for potential reuse
        session["query"] = query
        session["version"] = version

        # Fetch scripture results and count occurrences
        scripture_results, occurrence_count = get_scripture(query, version)

        # Generate a dynamic summary using Gemini
        dynamic_summary = None
        if scripture_results:
            dynamic_summary = generate_dynamic_summary(query, scripture_results, language)

        # If no results are found, fallback to a GPT/Gemini response
        gpt_response = None
        if not scripture_results:
            gpt_response = ask_gemini(query, language)

        # Get the full version name
        full_version_name = VERSION_NAMES.get(version, "Unknown Version")

        return render_template(
            "results.html",
            query=query,
            summary=dynamic_summary,
            results=scripture_results,
            gpt_response=gpt_response,
            language=language,
            version=version,
            full_version_name=full_version_name
        )

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT version FROM bible")
    versions = [row[0] for row in cursor.fetchall()]
    conn.close()

    return render_template("query_scripture.html", language=language, versions=versions)

if __name__ == "__main__":
    app.run(debug=True)
