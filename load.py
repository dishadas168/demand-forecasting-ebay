import json
import jsonlines


data = []
with jsonlines.open('jsonout.jsonl') as reader:
    for obj in reader:
        data.extend(obj)

print(len(data))

