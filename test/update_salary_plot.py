import json

notebook_path = "main_updated_final.ipynb"

with open(notebook_path, "r", encoding="utf-8") as f:
    nb = json.load(f)

# Remove the last two cells (the ones I just added)
nb["cells"] = nb["cells"][:-2]

markdown_cell = {
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "## 12. Salary Distribution (Ridgeline Plot) by Category\n",
        "This plot shows the distribution of salaries across different job categories. The \"mountain\" shapes represent the density of salary values (including min, avg, and max) for each category."
    ]
}

code = """
import seaborn as sns

# Prepare salary data
salary_cols = ['salary_min', 'salary_avg', 'salary_max']
for col in salary_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Melt the dataframe to get a distribution of all salary points (min, avg, max) per category
df_melted = df.melt(id_vars=['category'], value_vars=salary_cols, 
                    var_name='salary_type', value_name='salary_value')
df_melted = df_melted.dropna(subset=['salary_value'])

# Filter out categories with too few data points to produce a meaningful distribution
cat_counts = df_melted['category'].value_counts()
top_cats = cat_counts[cat_counts > 10].index
df_filtered = df_melted[df_melted['category'].isin(top_cats)].copy()

# Sort categories by median salary for a cleaner look
median_salaries = df_filtered.groupby('category')['salary_value'].median().sort_values(ascending=False)
df_filtered['category'] = pd.Categorical(df_filtered['category'], categories=median_salaries.index, ordered=True)

# Ridgeline Plot (Mountain Plot)
sns.set_theme(style="white", rc={"axes.facecolor": (0, 0, 0, 0)})

# Initialize the FacetGrid object
# Adjust height and hspace for the "mountain" overlap effect
g = sns.FacetGrid(df_filtered, row="category", hue="category", aspect=15, height=.7, palette="viridis")

# Draw the densities in a few steps
g.map(sns.kdeplot, "salary_value", bw_adjust=.5, clip_on=False, fill=True, alpha=1, linewidth=1.5)
g.map(sns.kdeplot, "salary_value", clip_on=False, color="w", lw=2, bw_adjust=.5)

# Add a horizontal line for each category
g.refline(y=0, linewidth=2, linestyle="-", color=None, clip_on=False)

# Label the categories
def label(x, color, label):
    ax = plt.gca()
    ax.text(0, .2, label, fontweight="bold", color=color,
            ha="left", va="center", transform=ax.transAxes, fontsize=10)

g.map(label, "salary_value")

# Set the subplots to overlap
g.figure.subplots_adjust(hspace=-.25)

# Remove axes details
g.set_titles("")
g.set(yticks=[], ylabel="")
g.despine(bottom=True, left=True)

# Set x-axis label and title
g.set_xlabels("Salary Amount", fontsize=12, fontweight='bold')
plt.suptitle('Salary Distribution Ridgeline Plot by Category (Mountain View)', fontsize=16, fontweight='bold', y=0.98)

plt.show()

# Reset seaborn theme for other plots
sns.set_theme(style="whitegrid")
"""

code_cell = {
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [line + "\n" for line in code.strip().split("\n")]
}

if code_cell["source"]:
    code_cell["source"][-1] = code_cell["source"][-1].rstrip("\n")

nb["cells"].extend([markdown_cell, code_cell])

with open(notebook_path, "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=1)

print("Updated main_updated_final.ipynb with Ridgeline (mountain) plot")
