import os
import requests

# GitHub base URL for the JSON files
BASE_URL = "https://raw.githubusercontent.com/thiagobodruk/bible/13225a15fa5e3e3043495b0c82df56c3fdfeb7f4/json/"
TARGET_FOLDER = "json"  # Local folder to store downloaded files

# Bible versions to download
VERSIONS = [
    "ar_svd.json",          # Arabic
    "de_schlachter.json",   # German Schlachter
    "el_greek.json",        # Modern Greek
    "en_bbe.json",          # Basic English
    "en_kjv.json",          # King James Version
    "eo_esperanto.json",    # Esperanto
    "es_rvr.json",          # Reina Valera (Spanish)
    "fi_finnish.json",      # Finnish Bible
    "fi_pr.json",           # Pyhä Raamattu (Finnish)
    "fr_apee.json",         # French Bible
    "ko_ko.json",           # Korean
    "pt_aa.json",           # Almeida Revisada Imprensa Bíblica (Portuguese)
    "pt_acf.json",          # Almeida Corrigida e Revisada Fiel (Portuguese)
    "pt_nvi.json",          # Nova Versão Internacional (Portuguese)
    "ro_cornilescu.json",   # Romanian
    "ru_synodal.json",      # Russian
    "vi_vietnamese.json",   # Vietnamese
    "zh_cuv.json",          # Chinese Union Version
    "zh_ncv.json"           # New Chinese Version
]
# Ensure the target folder exists
if not os.path.exists(TARGET_FOLDER):
    os.makedirs(TARGET_FOLDER)

# Download the selected JSON files
for version in VERSIONS:
    url = f"{BASE_URL}{version}"
    local_path = os.path.join(TARGET_FOLDER, version)

    print(f"Downloading {version}...")
    response = requests.get(url)

    if response.status_code == 200:
        with open(local_path, "wb") as file:
            file.write(response.content)
        print(f"Saved {version} to {local_path}")
    else:
        print(f"Failed to download {version}. Status code: {response.status_code}")
