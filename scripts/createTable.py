import pandas as pd

count = 4513
df = pd.DataFrame(index=range(0,4513), columns=['title', 'summary', 'camps', 'subjects', 'places', 'finlist'])
from pymarc import MARCReader
count = 0
with open('data/fortunoff.mrc', 'rb') as fh:
    reader = MARCReader(fh)
    for record in reader:
        print(record.title())
       
        title = record.title()
        df['title'][count] = title
        summ = ""
        for f in record.get_fields('520'):
            summ += f['a']
        df['summary'][count] = summ
        print(summ)
        print("-")

        for f in record.get_fields('600'):
            print(f['a'])
        print("-")
       
        camps = []
        for f in record.get_fields('610'):
            camps.append(f['a'])
        df['camps'][count] = camps
        print(camps)
        print("-")
       
        places = []
        for f in record.get_fields('651'):
            places.append(f['a'])
        for f in record.get_fields('691'):
            places.append(f['a'])
        df['places'][count] = places
        print(places)
        print("-")
       
        subjects = []
        for f in record.get_fields('650'):
            subjects.append(f['a'])
        for f in record.get_fields('690'):
            subjects.append(f['a'])
        df['subjects'][count] = subjects
        print(subjects)
        print("-")
       
        count+=1
        print("-----")