import json
import os

file_path = '/media/radayou/DATA/Study/ITC/Year 3/2nd semester/Mini Project/Final/Job_Recommendation/test/main_updated_final.ipynb'

with open(file_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# The robust code block to be inserted
robust_code = [
    "# ── Robust Model Performance Evaluation ──────────────────────────────────\n",
    "import pandas as pd\n",
    "import numpy as np\n",
    "\n",
    "def clean_columns(df):\n",
    "    \"\"\"Removes debugger-injected paths from column names (e.g., P @../../...)\"\"\"\n",
    "    mapping = {}\n",
    "    for col in df.columns:\n",
    "        if 'P@10' in col or 'P @10' in col: mapping[col] = 'Precision @10'\n",
    "        elif 'R@10' in col or 'R @10' in col: mapping[col] = 'Recall @10'\n",
    "        elif 'MAP' in col: mapping[col] = 'MAP @100'\n",
    "        elif 'NDCG' in col: mapping[col] = 'NDCG @10'\n",
    "    return df.rename(columns=mapping)\n",
    "\n",
    "try:\n",
    "    # 1. Access the evaluation data\n",
    "    if 'eval_df' not in globals():\n",
    "        print(\"❌ Error: 'eval_df' not found. Please run the cell where the models are evaluated first!\")\n",
    "    else:\n",
    "        # 2. Clean the column names to handle corrupted paths\n",
    "        clean_df = clean_columns(eval_df.copy())\n",
    "        \n",
    "        # 3. Calculate Aggregate Metrics\n",
    "        metrics = ['Precision @10', 'Recall @10', 'MAP @100', 'NDCG @10']\n",
    "        # Filter metrics that actually exist after cleaning\n",
    "        existing_metrics = [m for m in metrics if m in clean_df.columns]\n",
    "        \n",
    "        aggregate = clean_df.groupby('model')[existing_metrics].mean()\n",
    "        \n",
    "        # 4. Add Accuracy (which is same as Precision @10)\n",
    "        if 'Precision @10' in aggregate.columns:\n",
    "            aggregate['Accuracy (P@10)'] = aggregate['Precision @10']\n",
    "        \n",
    "        # 5. Final Formatting\n",
    "        final_cols = [c for c in ['Accuracy (P@10)'] + metrics if c in aggregate.columns]\n",
    "        final_table = aggregate[final_cols] * 100\n",
    "        \n",
    "        print(\"=== Final Model Performance Comparison (All Profiles) ===\")\n",
    "        display(final_table.round(2).astype(str) + '%')\n",
    "        \n",
    "        best_model = aggregate['NDCG @10'].idxmax() if 'NDCG @10' in aggregate.columns else \"Unknown\"\n",
    "        print(f\"\\n🏆 Best Model (by Ranking Quality): {best_model}\")\n",
    "\n",
    "except Exception as e:\n",
    "    print(f\"❌ An unexpected error occurred: {e}\")\n"
]

# Find the indices of the cells we added previously to remove them
# We look for unique strings in the cells we added
indices_to_remove = []
for i, cell in enumerate(nb['cells']):
    source_str = "".join(cell.get('source', []))
    if "def calculate_evaluation_metrics" in source_str or "aggregate_results = eval_df.groupby" in source_str:
        indices_to_remove.append(i)

# Remove old cells in reverse order to keep indices valid
for index in sorted(indices_to_remove, reverse=True):
    nb['cells'].pop(index)

# Append the new robust cell
new_cell = {
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": robust_code
}
nb['cells'].append(new_cell)

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)

print("Notebook fixed and robust evaluation cell added.")
