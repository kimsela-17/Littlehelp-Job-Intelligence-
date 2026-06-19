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
        "import numpy as np\n",
        "import pandas as pd\n",
        "\n",
        "def calculate_evaluation_metrics(recommendations_df, top_k=10):\n",
        "    \"\"\"\n",
        "    Calculates Precision, Recall, MAP, and NDCG for a single user profile's recommendations.\n",
        "    \n",
        "    Parameters:\n",
        "    - recommendations_df: A pandas DataFrame containing the recommended jobs sorted by rank.\n",
        "                          It MUST have a boolean column 'is_exact_match' (True if relevant, False if not)\n",
        "                          and an integer column 'total_exact_in_db' (total exact matches in the entire database).\n",
        "    - top_k: The number of top recommendations to evaluate (default is 10).\n",
        "    \"\"\"\n",
        "    # Get only the top K recommended jobs\n",
        "    top_recs = recommendations_df.head(top_k).copy()\n",
        "    top_recs['rank'] = np.arange(1, len(top_recs) + 1)\n",
        "    \n",
        "    # Ground truth values\n",
        "    exact_matches_found = top_recs['is_exact_match'].sum()\n",
        "    total_exact_matches = top_recs['total_exact_in_db'].iloc[0] if not top_recs.empty else 0\n",
        "    \n",
        "    # 1. Precision @ K: How many in the top K were correct?\n",
        "    precision = exact_matches_found / top_k\n",
        "    \n",
        "    # 2. Recall @ K: Out of all possible correct jobs, how many did we find?\n",
        "    recall = exact_matches_found / total_exact_matches if total_exact_matches > 0 else 0.0\n",
        "    \n",
        "    # 3. MAP (Mean Average Precision): Evaluates the ranking order\n",
        "    average_precision = 0.0\n",
        "    if exact_matches_found > 0:\n",
        "        matches_so_far = 0\n",
        "        precision_sum = 0.0\n",
        "        for _, row in top_recs.iterrows():\n",
        "            if row['is_exact_match']:\n",
        "                matches_so_far += 1\n",
        "                precision_sum += matches_so_far / row['rank']\n",
        "        \n",
        "        # Divide by the total number of relevant documents we COULD have found in top K\n",
        "        average_precision = precision_sum / min(total_exact_matches, top_k)\n",
        "        \n",
        "    # 4. NDCG @ K (Normalized Discounted Cumulative Gain): High penalty for ranking correct jobs lower\n",
        "    dcg = 0.0\n",
        "    for _, row in top_recs.iterrows():\n",
        "        if row['is_exact_match']:\n",
        "            # Gain of 1, discounted by the log of the rank\n",
        "            dcg += 1.0 / np.log2(row['rank'] + 1)\n",
        "            \n",
        "    # Calculate Ideal DCG (if all exact matches were ranked 1st, 2nd, 3rd...)\n",
        "    idcg = 0.0\n",
        "    ideal_hits = min(total_exact_matches, top_k)\n",
        "    for i in range(1, int(ideal_hits) + 1):\n",
        "        idcg += 1.0 / np.log2(i + 1)\n",
        "        \n",
        "    ndcg = dcg / idcg if idcg > 0 else 0.0\n",
        "    \n",
        "    return {\n",
        "        f'Precision@{top_k}': precision,\n",
        "        f'Recall@{top_k}': recall,\n",
        "        f'MAP@{top_k}': average_precision,\n",
        "        f'NDCG@{top_k}': ndcg\n",
        "    }\n",
        "\n",
        "# ---------------------------------------------------------\n",
        "# Example Usage (Testing the function with dummy data)\n",
        "# ---------------------------------------------------------\n",
        "mock_recommendations = pd.DataFrame({\n",
        "    'job_title': ['Job A', 'Job B', 'Job C', 'Job D', 'Job E', 'Job F', 'Job G', 'Job H', 'Job I', 'Job J'],\n",
        "    'is_exact_match': [True, False, True, False, True, False, False, False, False, False], # Found 3 exact matches\n",
        "    'total_exact_in_db': [5] * 10 # Let's assume there are 5 exact matches in the whole database\n",
        "})\n",
        "\n",
        "calculated_metrics = calculate_evaluation_metrics(mock_recommendations, top_k=10)\n",
        "print(\"Calculated Metrics for Profile:\")\n",
        "for metric, value in calculated_metrics.items():\n",
        "    print(f\"{metric}: {value:.4f}\")\n"
    ]
}

nb['cells'].append(new_cell)

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)

print("Cell appended successfully.")
