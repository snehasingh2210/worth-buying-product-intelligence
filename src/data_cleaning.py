import pandas as pd


# Load raw dataset
input_file = "data/raw/products.csv"
output_file = "data/processed/clean_products.csv"

df = pd.read_csv(input_file)

print("Original dataset shape:", df.shape)

# Remove completely empty columns
df = df.dropna(axis=1, how="all")

# Remove duplicate rows
df = df.drop_duplicates()

# Clean column names
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

# Convert rating to numeric
if "reviews.rating" in df.columns:
    df["reviews.rating"] = pd.to_numeric(
        df["reviews.rating"], errors="coerce"
    )

# Remove reviews without rating
if "reviews.rating" in df.columns:
    df = df.dropna(subset=["reviews.rating"])

# Keep ratings between 1 and 5
if "reviews.rating" in df.columns:
    df = df[
        (df["reviews.rating"] >= 1) &
        (df["reviews.rating"] <= 5)
    ]

# Clean review text
if "reviews.text" in df.columns:
    df["reviews.text"] = df["reviews.text"].fillna("").astype(str).str.strip()

# Clean product names
if "name" in df.columns:
    df["name"] = df["name"].fillna("Unknown Product").astype(str).str.strip()

# Save cleaned dataset
df.to_csv(output_file, index=False)

print("Cleaned dataset shape:", df.shape)
print("Saved to:", output_file)