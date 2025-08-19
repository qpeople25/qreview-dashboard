import json
import csv
import random
from datetime import datetime, timedelta

groups = ['SLT', 'LDT', 'MGR', 'LNR']
responses_per_group = {g: random.randint(5, 8) for g in groups}

# Load question mapping
with open('question_mapping_fixed.json', 'r', encoding='utf-8') as f:
    question_map = json.load(f)

field_ids = list(question_map.keys())

rows = []
start_time = datetime(2024, 6, 1, 10, 0, 0)

# Define group score biases for misalignment
# e.g., SLT high, LDT medium, MGR low, LNR very low for some elements
score_bias = {
    'Strategic Connection': {'SLT': 5, 'LDT': 4, 'MGR': 2, 'LNR': 2},
    'Needs Analysis': {'SLT': 4, 'LDT': 3, 'MGR': 5, 'LNR': 2},
    'Learning Design': {'SLT': 3, 'LDT': 5, 'MGR': 2, 'LNR': 4},
    'Learning Culture': {'SLT': 2, 'LDT': 2, 'MGR': 4, 'LNR': 5},
    'Platform and Tools': {'SLT': 4, 'LDT': 2, 'MGR': 3, 'LNR': 5},
    'Integration with Talent': {'SLT': 2, 'LDT': 5, 'MGR': 4, 'LNR': 3},
    'Learning Impact': {'SLT': 5, 'LDT': 3, 'MGR': 2, 'LNR': 4},
    'Future Capability': {'SLT': 3, 'LDT': 4, 'MGR': 5, 'LNR': 2},
}

for group in groups:
    for i in range(responses_per_group[group]):
        respondent_id = f'{group}_{i+1}'
        timestamp = (start_time + timedelta(minutes=i)).isoformat() + 'Z'
        for field_id in field_ids:
            mapping = question_map[field_id]
            element = mapping['element']
            # Add some random noise around the group bias for each element
            base = score_bias[element][group]
            score = min(5, max(1, base + random.choice([-1, 0, 0, 1])))
            rows.append({
                'respondent_id': respondent_id,
                'group': group,
                'element': element,
                'subelement': mapping['subelement'],
                'score': score,
                'timestamp': timestamp
            })

with open('dummy_misaligned_clean.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['respondent_id', 'group', 'element', 'subelement', 'score', 'timestamp'])
    writer.writeheader()
    for row in rows:
        writer.writerow(row)

print(f"Generated dummy_misaligned_clean.csv with {len(rows)} rows (groups: {responses_per_group})") 