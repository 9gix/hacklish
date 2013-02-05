import csv
import re

def bracket2dict(text):
    phrases = text.splitlines()
    data = {}
    for phrase in phrases:
        to_phrase = re.sub(r'\([^)]*\)', '', phrase).strip()
        for c in ['(', ')']:
            phrase = phrase.replace(c, '')
        data[phrase] = to_phrase
    return data

def dict2csv(data, filename='data.csv'):
    w = csv.writer(open(filename, "w"))
    for key, val in data.items():
        w.writerow([key, val])

def csv2dict(filename='data.csv'):
    data = {}
    for key, val in csv.reader(open(filename)):
        data[key] = val
    return data

def main():
    f = open('redundancy1', 'r')
    text = f.read()
    data = bracket2dict(text)
    dict2csv(data)
    print csv2dict()

if __name__ == '__main__':
    main()
