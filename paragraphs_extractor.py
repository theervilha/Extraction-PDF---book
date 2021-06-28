import pandas as pd
import re
import pdftotext

with open("InteligenciaEmocional-DanielGoleman.pdf", 'rb') as file: 
    pdf = list(pdftotext.PDF(file))

def cleanText(text): 
    if text[0] == "•": 
        text = ' '.join(text.split()) 
    return text 


paragraphs = []
for page in pdf[10:351]: # Start and end
    lastIndex = 0 
    iterador = list(re.finditer(r'\n    [a-zA-Z\•]', page)) 
    for i, match in enumerate(iterador): 
        if i == 0: 
            paragraph = page[:match.start()] 
            paragraph = cleanText(paragraph) 
            paragraphs.append(paragraph) 
            if i < len(iterador) - 1: 
                nextStart = iterador[i+1].start() 
                paragraph = page[match.end()-1:nextStart] 
                paragraph = cleanText(paragraph) 
                paragraphs.append(paragraph) 
            continue 
        elif i == len(iterador) - 1: 
            paragraph = page[match.end()-1:] 
        else: 
            nextStart = iterador[i+1].start() 
            paragraph = page[match.end()-1:nextStart]  

            paragraph = cleanText(paragraph) 
            paragraphs.append(paragraph) 


def cleanParagraph(text):
    text = text.lower()
    text = ' '.join(text.split())
    return text
    
newParagraphs = []
for i, paragraph in enumerate(paragraphs):
    if paragraph[-1:] == '\n':
        # quando quebra o parágrafo de uma página para outra, tem um \n no final
        paragraph = paragraph[:-1] + paragraphs[i+1]

    paragraph = cleanParagraph(paragraph)
    if len(paragraph.split()) <= 500:
        newParagraphs.append(paragraph)

data = {'index_name': 'inteligência_emocional', 'items': newParagraphs}
df = pd.DataFrame(data)
df.to_csv('extracted.csv', index=False, encoding='utf-8', sep=';')