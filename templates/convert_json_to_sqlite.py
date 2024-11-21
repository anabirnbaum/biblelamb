import sqlite3
import json
import os
import codecs

# Paths
json_folder = "json"  # Folder containing JSON files
db_file = "bible.db"  # SQLite database file

# Create SQLite database and table
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# Create the Bible table
cursor.execute("""
CREATE TABLE IF NOT EXISTS bible (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    book TEXT NOT NULL,
    chapter INTEGER NOT NULL,
    verse INTEGER NOT NULL,
    text TEXT NOT NULL,
    version TEXT NOT NULL
);
""")

# Loop through all JSON files in the folder
for filename in os.listdir(json_folder):
    if filename.endswith(".json"):
        json_path = os.path.join(json_folder, filename)
        version = filename.split(".")[0]  # Extract version name from filename

        print(f"Processing {filename} (version: {version})...")

        # Load data from JSON with utf-8-sig to handle BOM
        with codecs.open(json_path, "r", encoding="utf-8-sig") as file:
            try:
                data = json.load(file)  # Load JSON data
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON in {filename}: {e}")
                continue

        # Process each book
        for book_data in data:
            book = book_data["abbrev"]  # Book abbreviation
            chapters = book_data["chapters"]

            # Process each chapter
            for chapter_num, verses in enumerate(chapters, start=1):
                # Process each verse
                for verse_num, text in enumerate(verses, start=1):
                    cursor.execute("""
                    INSERT INTO bible (book, chapter, verse, text, version)
                    VALUES (?, ?, ?, ?, ?)
                    """, (book, chapter_num, verse_num, text, version))

        print(f"Data from {filename} added to the database.")

# Commit changes and close the database
conn.commit()
conn.close()

print(f"Database created and populated successfully: {db_file}")
