from datasets import load_dataset

print("Loading SCAMINTEL AI dataset...")

dataset = load_dataset(
    "shariul-islam/bengali-sms-smishing-dataset"
)

# Convert training texts into a set
train_texts = set(
    str(x).strip()
    for x in dataset["train"]["text"]
)

# Remove validation messages already present in training
clean_validation = dataset["validation"].filter(
    lambda example: str(example["text"]).strip() not in train_texts
)

# Keep train and test unchanged
cleaned_dataset = {
    "train": dataset["train"],
    "validation": clean_validation,
    "test": dataset["test"]
}

print("\n===== CLEANED DATASET =====")
print("Train:", len(cleaned_dataset["train"]))
print("Validation:", len(cleaned_dataset["validation"]))
print("Test:", len(cleaned_dataset["test"]))

# Save locally
for split, data in cleaned_dataset.items():
    output_path = f"data/processed/{split}"
    data.save_to_disk(output_path)
    print(f"Saved {split} → {output_path}")

print("\nDataset preparation complete!")