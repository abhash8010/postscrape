import json
import os

if os.path.exists('formatted_output.txt'):
    os.remove('formatted_output.txt')
with open('output.json', 'r', encoding='utf-8') as file:
    texts = json.load(file)

formatted_text = ''
changedTitle = ''

for text in texts:
    title = text['h1_text']
    stepNumber = text['h2_text']
    instructions = text['p_texts']
    if (title != changedTitle):
        changedTitle = title
        formatted_text += f'{title}\n'
    formatted_text += f"{stepNumber}\n"

    for instruction in instructions:
        formatted_text += f"{instruction}\n"

    formatted_text += "\n"

with open('formatted_output.txt', 'w', encoding='utf-8') as out_file:
    out_file.write(formatted_text)
