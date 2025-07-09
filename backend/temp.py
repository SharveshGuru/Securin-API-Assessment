import json

with open(r'C:\stuff\Securin-API-Assessment\backend\recipies.json') as file:
    file_data = json.load(file)
    lst=file_data['data']
    c=0
    for i in lst:
        c+=1
print(c)