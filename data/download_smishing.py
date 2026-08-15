from datasets import load_dataset

print("Downloading SCAMINTEL AI smishing dataset...")

dataset = load_dataset("shariul-islam/bengali-sms-smishing-dataset")

print("\nDataset downloaded successfully!")
print(dataset)

for split in dataset:
    print(f"\n{split} samples: {len(dataset[split])}")
    print("Columns:", dataset[split].column_names)
    print("First sample:")
    print(dataset[split][0])