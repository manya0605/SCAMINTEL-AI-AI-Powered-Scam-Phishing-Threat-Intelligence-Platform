from datasets import load_dataset
from collections import Counter

dataset = load_dataset("shariul-islam/bengali-sms-smishing-dataset")

print("\n===== SCAMINTEL AI DATASET INSPECTION =====")

for split in dataset:
    data = dataset[split]

    print(f"\n--- {split.upper()} ---")
    print("Samples:", len(data))

    labels = Counter(data["label"])
    sources = Counter(data["source"])

    print("\nLabels:")
    for label, count in labels.items():
        print(f"  {label}: {count}")

    print("\nSources:")
    for source, count in sources.items():
        print(f"  {source}: {count}")

print("\n===== INSPECTION COMPLETE =====")