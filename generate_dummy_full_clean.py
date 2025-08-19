import json
import csv
import random
from datetime import datetime, timedelta

groups = ['SLT', 'LDT', 'MGR', 'LNR']
respondents_per_group = 5

# Load question mapping
with open('question_mapping_fixed.json', 'r', encoding='utf-8') as f:
    question_map = json.load(f)

field_ids = list(question_map.keys())

rows = []
start_time = datetime(2024, 6, 1, 10, 0, 0)

for group in groups:
    for i in range(respondents_per_group):
        respondent_id = f'{group}_{i+1}'
        timestamp = (start_time + timedelta(minutes=i)).isoformat() + 'Z'
        for field_id in field_ids:
            mapping = question_map[field_id]
            score = random.randint(1, 5)
            rows.append({
                'respondent_id': respondent_id,
                'group': group,
                'element': mapping['element'],
                'subelement': mapping['subelement'],
                'score': score,
                'timestamp': timestamp
            })

with open('dummy_full_clean.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['respondent_id', 'group', 'element', 'subelement', 'score', 'timestamp'])
    writer.writeheader()
    for row in rows:
        writer.writerow(row)

print(f"Generated dummy_full_clean.csv with {len(rows)} rows ({len(groups)*respondents_per_group} respondents, {len(field_ids)} questions each)") 