from datasets import load_dataset

dataset = load_dataset(
    "shariul-islam/bengali-sms-smishing-dataset"
)

train = {
    str(row["text"]).strip(): row["label"]
    for row in dataset["train"]
}

validation = {
    str(row["text"]).strip(): row["label"]
    for row in dataset["validation"]
}

overlap = set(train.keys()) & set(validation.keys())

print("===== TRAIN / VALIDATION OVERLAP =====")
print("Overlapping messages:", len(overlap))

for text in overlap:
    print("\nMESSAGE:")
    print(text)

    print("Train label:", train[text])
    print("Validation label:", validation[text])

    if train[text] == validation[text]:
        print("Status: SAME LABEL")
    else:
        print("Status: ⚠️ CONFLICTING LABEL")