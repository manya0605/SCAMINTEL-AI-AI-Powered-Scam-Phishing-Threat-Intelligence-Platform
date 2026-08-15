# ============================================================
# SCAMINTEL AI — CAMPAIGN HISTORY
# ============================================================

import json
import os


# ============================================================
# HISTORY FILE PATH
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

DATA_DIR = os.path.join(
    BASE_DIR,
    "data"
)

HISTORY_FILE = os.path.join(
    DATA_DIR,
    "campaign_history.json"
)


# ------------------------------------------------------------
# LOAD HISTORY
# ------------------------------------------------------------

def load_campaign_history():

    if not os.path.exists(HISTORY_FILE):
        return []

    try:

        with open(
            HISTORY_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except Exception:

        return []


# ------------------------------------------------------------
# SAVE MESSAGE
# ------------------------------------------------------------

def save_campaign_message(text: str):

    history = load_campaign_history()

    history.append({
        "message": text
    })

    # Keep the history manageable
    history = history[-100:]

    os.makedirs(
        DATA_DIR,
        exist_ok=True
    )

    with open(
        HISTORY_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            history,
            file,
            indent=4,
            ensure_ascii=False
        )


# ------------------------------------------------------------
# GET PREVIOUS MESSAGES
# ------------------------------------------------------------

def get_previous_messages():

    history = load_campaign_history()

    return [
        item["message"]
        for item in history
        if "message" in item
    ]