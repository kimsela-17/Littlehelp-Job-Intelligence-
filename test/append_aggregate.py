import json

file_path = '/media/radayou/DATA/Study/ITC/Year 3/2nd semester/Mini Project/Final/Job_Recommendation/test/main_updated_final.ipynb'

with open(file_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

new_cell = {
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "# ── Global Aggregate Model Comparison ──────────────────────────────────\n",
        "import pandas as pd\n",
        "\n",
        "# 1. Calculate the mean metrics for each model\n",
        "# We use P@10 as the proxy for 'Accuracy' in recommendation systems\n",
        "aggregate_results = eval_df.groupby('model')[['P @10', 'R @10', 'MAP @100', 'NDCG @10']].mean()\n",
        "\n",
        "# 2. Rename columns for clarity and add 'Accuracy' label\n",
        "comparison_table = aggregate_results.copy()\n",
        "comparison_table.columns = ['Precision @10', 'Recall @10', 'MAP @100', 'NDCG @10']\n",
        "comparison_table['Accuracy (P@10)'] = comparison_table['Precision @10']\n",
        "\n",
        "# 3. Reorder to show Accuracy first as requested\n",
        "cols = ['Accuracy (P@10)', 'Precision @10', 'Recall @10', 'MAP @100', 'NDCG @10']\n",
        "comparison_table = comparison_table[cols] * 100 # Convert to percentage\n",
        "\n",
        "print(\"=== Final Model Performance Comparison (All Profiles) ===\")\n",
        "display(comparison_table.round(2).astype(str) + '%')\n",
        "\n",
        "print(\"\\nSummary of Best Performing Model:\")\n",
        "best_model = aggregate_results['NDCG @10'].idxmax()\n",
        "print(f\"Based on NDCG (ranking quality), the best model is: {best_model}\")\n"
    ]
}

nb['cells'].append(new_cell)

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)

print("Aggregate cell appended successfully.")
