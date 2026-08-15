from datasets import load_dataset
from pathlib import Path
import pandas as pd


# ============================================================
# SCAMINTEL AI — URL DATASET PREPARATION
# ============================================================

DATASET_NAME = "kmack/Phishing_urls"

OUTPUT_DIR = Path("data/processed_url")

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


print("=" * 60)
print("     SCAMINTEL AI — URL DATA PREPARATION")
print("=" * 60)

print("\nLoading Hugging Face dataset...")

dataset = load_dataset(DATASET_NAME)

print("\nDataset loaded.")

for split_name in ["train", "valid", "test"]:

    split = dataset[split_name]

    print(
        f"\nProcessing {split_name}: "
        f"{len(split)} URLs"
    )

    df = split.to_pandas()

    # --------------------------------------------------------
    # Keep only required columns
    # --------------------------------------------------------

    df = df[
        ["text", "label"]
    ].copy()

    # --------------------------------------------------------
    # Rename URL column
    # --------------------------------------------------------

    df.rename(
        columns={
            "text": "url"
        },
        inplace=True
    )

    # --------------------------------------------------------
    # Remove missing values
    # --------------------------------------------------------

    df.dropna(
        subset=[
            "url",
            "label"
        ],
        inplace=True
    )

    # --------------------------------------------------------
    # Convert URL to string
    # --------------------------------------------------------

    df["url"] = df["url"].astype(str)

    # --------------------------------------------------------
    # Remove exact duplicate URLs INSIDE each split
    # --------------------------------------------------------

    before = len(df)

    df.drop_duplicates(
        subset=["url"],
        inplace=True
    )

    removed = before - len(df)

    print(
        "Duplicates removed:",
        removed
    )

    # --------------------------------------------------------
    # Normalize labels
    # --------------------------------------------------------

    df["label"] = df["label"].astype(int)

    # --------------------------------------------------------
    # Save
    # --------------------------------------------------------

    output_file = (
        OUTPUT_DIR
        / f"{split_name}.csv"
    )

    df.to_csv(
        output_file,
        index=False
    )

    print(
        "Saved:",
        output_file
    )

    print(
        "Final samples:",
        len(df)
    )

    print("\nLabel distribution:")

    print(
        df["label"]
        .value_counts()
        .sort_index()
    )


print("\n" + "=" * 60)
print("URL DATASET PREPARATION COMPLETE")
print("=" * 60)