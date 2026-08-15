from datasets import load_dataset
from collections import Counter

print("Loading SCAMINTEL AI dataset...")

dataset = load_dataset("shariul-islam/bengali-sms-smishing-dataset")

print("\n===== SCAMINTEL AI DATA QUALITY CHECK =====")

# --------------------------------------------------
# 1. Basic information
# --------------------------------------------------

for split in dataset:
    print(f"\n{split.upper()} DATA")
    print("Samples:", len(dataset[split]))
    print("Columns:", dataset[split].column_names)

# --------------------------------------------------
# 2. Empty messages
# --------------------------------------------------

print("\n===== EMPTY TEXT CHECK =====")

for split in dataset:
    texts = dataset[split]["text"]

    empty_count = sum(
        1 for text in texts
        if text is None or str(text).strip() == ""
    )

    print(f"{split}: {empty_count} empty messages")

# --------------------------------------------------
# 3. Duplicate messages inside each split
# --------------------------------------------------

print("\n===== DUPLICATE CHECK =====")

for split in dataset:
    texts = [str(x).strip() for x in dataset[split]["text"]]

    unique_texts = set(texts)
    duplicate_count = len(texts) - len(unique_texts)

    print(f"{split}: {duplicate_count} duplicate messages")

# --------------------------------------------------
# 4. Label distribution
# --------------------------------------------------

print("\n===== LABEL DISTRIBUTION =====")

for split in dataset:
    labels = Counter(dataset[split]["label"])

    print(f"\n{split}:")
    for label, count in labels.items():
        percentage = count / len(dataset[split]) * 100
        print(f"  {label}: {count} ({percentage:.2f}%)")

# --------------------------------------------------
# 5. Very short messages
# --------------------------------------------------

print("\n===== SHORT MESSAGE CHECK =====")

for split in dataset:
    texts = dataset[split]["text"]

    short_count = sum(
        1 for text in texts
        if len(str(text).strip()) < 10
    )

    print(f"{split}: {short_count} messages shorter than 10 characters")

# --------------------------------------------------
# 6. Cross-split leakage
# --------------------------------------------------

print("\n===== CROSS-SPLIT LEAKAGE CHECK =====")

train_texts = set(
    str(x).strip()
    for x in dataset["train"]["text"]
)

validation_texts = set(
    str(x).strip()
    for x in dataset["validation"]["text"]
)

test_texts = set(
    str(x).strip()
    for x in dataset["test"]["text"]
)

train_validation_overlap = train_texts & validation_texts
train_test_overlap = train_texts & test_texts
validation_test_overlap = validation_texts & test_texts

print(
    "Train ↔️ Validation:",
    len(train_validation_overlap)
)

print(
    "Train ↔️ Test:",
    len(train_test_overlap)
)

print(
    "Validation ↔️ Test:",
    len(validation_test_overlap)
)

print("\n===== DATA QUALITY CHECK COMPLETE =====")