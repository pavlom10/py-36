# Написать программу, которая будет выводить топ 10 самых часто встречающихся
# в новостях слов длиннее 6 символов для каждого файла.

import json
import xml.etree.ElementTree as ET

def get_top_words(text, top=10, min_length=6):
    words_count = {}
    words = text.split(' ')
    for word in words:
        if len(word) >= min_length:
            if word in words_count:
                words_count[word] += 1
            else:
                words_count[word] = 1
    sorted_words = sorted(words_count, key=words_count.get, reverse=True)
    return sorted_words[:top]

#json
with open('newsafr.json', encoding='utf-8') as f:
    data = json.load(f)
    items = data['rss']['channel']['items']
    text = ''
    for item in items:
        text += item['description'] + ' '

    top_words = get_top_words(text)
    print(top_words)

#xml
parser = ET.XMLParser(encoding='utf-8')
tree = ET.parse('newsafr.xml')
root = tree.getroot()
xml_items = root.findall('channel/item')
text = ''
for xml_item in xml_items:
    text += xml_item.find('description').text

top_words = get_top_words(text)
print(top_words)


