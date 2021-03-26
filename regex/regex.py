import re
# from pprint import pprint
import csv

with open('phonebook_raw.csv') as f:
    rows = csv.reader(f, delimiter=',')
    contacts_list = list(rows)
# pprint(contacts_list)

header = contacts_list.pop(0)
result = {}

pattern_tel = re.compile(r"(\+7|8)\s*\(?(\d{3})\)?[-\s]?(\d+)[-\s]?(\d{2})[\s-]?(\d{2})")
pattern_dob = re.compile(r"(\+7|8)\s*\(?(\d{3})\)?[-\s]?(\d+)[-\s]?(\d{2})[\s-]?(\d{2})\s?\(?(доб.)?\s?(\d+)\)?")

for item in contacts_list:
    contact = item[:]

    surname = contact[0].split(' ', 3)
    if len(surname) > 1:
        contact[0] = surname[0]
        contact[1] = surname[1]
    if len(surname) == 3:
        contact[2] = surname[2]

    name = contact[1].split(' ', 2)
    if len(name) == 2:
        contact[1] = name[0]
        contact[2] = name[1]

    tel = contact[5]
    if tel != '':
        if 'доб.' in tel:
            tel = pattern_dob.sub(r"+7(\2)\3-\4-\5 доб.\7", tel)
        else:
            tel = pattern_tel.sub(r"+7(\2)\3-\4-\5", tel)
        contact[5] = tel

    key = contact[0] + ' ' + contact[1];

    if key in result:
        for id, value in enumerate(contact):
            if value != '':
                result[key][id] = value
    else:
        result[key] = contact

contacts_list = []
for row in result.values():
    contacts_list.append(row)

with open('phonebook.csv', 'w') as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerow(header)
    datawriter.writerows(contacts_list)