import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_excel(r"c:\Users\Admin\Desktop\online_retail_II.xlsx")

print(df.head())
print(df.shape)

df = df.dropna(subset=["Customer ID"])

df = df[~df["Invoice"].astype(str).str.startswith("C")]

df = df[df["Quantity"] > 0]

print(df.shape)
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

print(df["InvoiceDate"].head())
df["InvoiceMonth"] = df["InvoiceDate"].dt.to_period("M")

print(df[["InvoiceDate", "InvoiceMonth"]].head())
df["CohortMonth"] = df.groupby("Customer ID")["InvoiceMonth"].transform("min")

print(df[["Customer ID", "InvoiceMonth", "CohortMonth"]].head(10))
# Step 6: Calculate Retention Month

df["RetentionMonth"] = (
    (df["InvoiceMonth"].dt.year - df["CohortMonth"].dt.year) * 12
    + (df["InvoiceMonth"].dt.month - df["CohortMonth"].dt.month)
)
cohort_counts = (
    df.groupby(["CohortMonth", "RetentionMonth"])["Customer ID"]
      .nunique()
      .reset_index(name="Customers")
)

cohort_table = cohort_counts.pivot(
    index="CohortMonth",
    columns="RetentionMonth",
    values="Customers"
)

print("Cohort Customer Table:")
print(cohort_table)

retention_table = cohort_table.divide(
    cohort_table.iloc[:, 0],
    axis=0
) * 100

print("\nRetention Percentage Table:")
print(retention_table.round(2))

plt.figure(figsize=(15, 9))

sns.heatmap(
    retention_table,
    annot=True,
    fmt=".1f",
    cmap="YlGnBu",
    vmin=0,
    vmax=100
)

plt.title("Cohort Retention Heatmap")
plt.xlabel("Retention Month")
plt.ylabel("Cohort Month")
plt.tight_layout()

plt.show()