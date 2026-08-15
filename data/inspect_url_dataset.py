from datasets import load_dataset
from collections import Counter

print("=" * 60)
print("       SCAMINTEL AI — URL DATASET INSPECTION")
print("=" * 60)

print("\nDownloading/loading URL dataset...")
print("URLs will be treated ONLY as text. No URLs will be opened.")

dataset = load_dataset(
    "kmack/Phishing_urls"
)

print("\n===== DATASET LOADED =====")

print(dataset)

for split_name in dataset.keys():

    split = dataset[split_name]

    print("\n" + "=" * 50)
    print("SPLIT:", split_name.upper())
    print("=" * 50)

    print("Samples:", len(split))

    print("Columns:", split.column_names)

    labels = Counter(split["label"])

    print("\nLabels:")

    for label, count in sorted(labels.items()):

        if label == 0:
            name = "BENIGN"
        elif label == 1:
            name = "PHISHING"
        else:
            name = str(label)

        percentage = count / len(split) * 100

        print(
            f"  {name}: {count} "
            f"({percentage:.2f}%)"
        )

    print("\nFirst 3 URLs:")

    for i in range(min(3, len(split))):

        print(
            f"\nURL {i + 1}:"
        )

        print(
            split[i]["text"]
        )

        print(
            "Label:",
            split[i]["label"]
        )

print("\n" + "=" * 60)
print("URL DATASET INSPECTION COMPLETE")
print("=" * 60)