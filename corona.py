import os
import json
import pandas as pd
import re
import matplotlib.pyplot as plt
dirs = ["biorxiv_medrxiv"]
docs= []
for d in dirs:
    text_abstract = ''
    for file in os.listdir(f"{d}/{d}"):
        file_path = f"{d}/{d}/{file}"
        specific_json = json.load(open(file_path,"rb"))
        title = specific_json['metadata']['title']
        try:
            abstract = specific_json['abstract'][0]
            text_abstract += abstract['text'] + '\n\n'
        except:
            abstract = ""
        text_in_body = ""
        for text in specific_json['body_text']:
            text_in_body += text['text'] + '\n\n'
        docs.append([title, text_abstract, text_in_body])

df = pd.DataFrame(docs, columns=['title', 'text_abstract', 'text_in_body'])
incubation = df[df['text_in_body'].str.contains('incubation')]
texts = incubation['text_in_body'].values
incubation_times = []
for t in texts:
    for sentence in t.split('. '):
        if "incubation" in sentence:
            incubation_days = re.findall(r"\d*\.\d+ days", sentence)
            if len(incubation_days) != 0:
                num = incubation_days[0].split(' ')
                incubation_times.append(float(num[0]))
plt.hist(incubation_times, bins=20)
plt.ylabel('bin counts')
plt.xlabel('incubation time (days)')
plt.show()