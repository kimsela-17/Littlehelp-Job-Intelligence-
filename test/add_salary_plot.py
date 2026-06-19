import json

notebook_path = "main_updated_final.ipynb"

with open(notebook_path, "r", encoding="utf-8") as f:
    nb = json.load(f)

markdown_cell = {
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "## 12. Salary Distribution by Category\n",
        "Visualizing the mean of minimum, average, and maximum salaries across different job categories."
    ]
}

code = """
# Convert salary columns to numeric, setting errors='coerce' to turn empty/invalid into NaN
salary_cols = ['salary_min', 'salary_avg', 'salary_max']
for col in salary_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Group by category and calculate the mean of the salary columns, dropping categories with no salary data
salary_by_cat = df.groupby('category')[salary_cols].mean().dropna(how='all')

# Sort by average salary to make the chart easier to read
if 'salary_avg' in salary_by_cat.columns:
    salary_by_cat = salary_by_cat.sort_values(by='salary_avg', ascending=False)

# Plot the distribution
ax = salary_by_cat.plot(kind='bar', figsize=(14, 8), width=0.8, colormap='viridis')
plt.title('Salary Distribution (Mean of Min, Avg, Max) by Category', fontsize=16, fontweight='bold', pad=15)
plt.xlabel('Job Category', fontsize=12, fontweight='bold')
plt.ylabel('Salary Amount', fontsize=12, fontweight='bold')
plt.xticks(rotation=45, ha='right', fontsize=10)
plt.legend(['Salary Min', 'Salary Avg', 'Salary Max'], title='Salary Metric', fontsize=10)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()
"""

code_cell = {
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [line + "\n" for line in code.strip().split("\n")]
}

# Remove trailing newline from the last line
if code_cell["source"]:
    code_cell["source"][-1] = code_cell["source"][-1].rstrip("\n")

nb["cells"].extend([markdown_cell, code_cell])

with open(notebook_path, "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=1)

print("Added cell to main_updated_final.ipynb")
