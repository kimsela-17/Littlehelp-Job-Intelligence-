import json

notebook_path = "main_updated_final.ipynb"

with open(notebook_path, "r", encoding="utf-8") as f:
    nb = json.load(f)

# Remove the last two cells from the previous Ridgeline attempt
nb["cells"] = nb["cells"][:-2]

markdown_cell = {
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "## 12. Detailed Salary Distributions (Mountain Plots) by Category\n",
        "This section visualizes the distribution of **Minimum**, **Average**, and **Maximum** salaries across job categories using Ridgeline plots to illustrate the \"mountain range\" of salary densities."
    ]
}

code = """
import seaborn as sns
import matplotlib.pyplot as plt

# 1. Data Preparation
salary_cols = ['salary_min', 'salary_avg', 'salary_max']
for col in salary_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Filter categories with at least 5 data points for better distribution curves
def get_filtered_df(df, column):
    temp_df = df.dropna(subset=[column]).copy()
    counts = temp_df['category'].value_counts()
    valid_cats = counts[counts >= 5].index
    return temp_df[temp_df['category'].isin(valid_cats)]

# 2. Reusable Mountain (Ridgeline) Plot Function
def plot_mountain_range(data, column, title_suffix):
    sns.set_theme(style="white", rc={"axes.facecolor": (0, 0, 0, 0)})
    
    # Sort categories by median salary for the specific column
    medians = data.groupby('category')[column].median().sort_values(ascending=False)
    data['category_sorted'] = pd.Categorical(data['category'], categories=medians.index, ordered=True)
    
    # Initialize the FacetGrid
    g = sns.FacetGrid(data, row="category_sorted", hue="category_sorted", 
                      aspect=10, height=0.8, palette="viridis")

    # Draw the densities (the mountains)
    g.map(sns.kdeplot, column, bw_adjust=.5, clip_on=False, fill=True, alpha=0.8, linewidth=1.5)
    g.map(sns.kdeplot, column, clip_on=False, color="w", lw=2, bw_adjust=.5)
    g.refline(y=0, linewidth=2, linestyle="-", color=None, clip_on=False)

    # Label categories
    def label_cats(x, color, label):
        ax = plt.gca()
        ax.text(0, .2, label, fontweight="bold", color=color,
                ha="left", va="center", transform=ax.transAxes, fontsize=10)
    
    g.map(label_cats, column)

    # Styling
    g.figure.subplots_adjust(hspace=-0.2)
    g.set_titles("")
    g.set(yticks=[], ylabel="")
    g.despine(bottom=True, left=True)
    
    plt.suptitle(f'Distribution of {title_suffix} Salary by Category', fontsize=18, fontweight='bold', y=0.98)
    g.set_xlabels(f'{title_suffix} Salary Amount', fontsize=12, fontweight='bold')
    plt.show()

# 3. Generate the 3 Plots
plot_mountain_range(get_filtered_df(df, 'salary_min'), 'salary_min', 'Minimum')
plot_mountain_range(get_filtered_df(df, 'salary_avg'), 'salary_avg', 'Average')
plot_mountain_range(get_filtered_df(df, 'salary_max'), 'salary_max', 'Maximum')

# Reset theme
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

print("Updated notebook with 3 separate mountain plots for min, avg, and max salaries.")
