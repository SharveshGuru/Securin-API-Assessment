import json

with open(r'C:\stuff\Securin-API-Assessment\backend\US_recipes_null.json') as file:
    file_data = json.load(file)
    lst=file_data['0']
    c=0
    for i in file_data:
        dic=file_data[i]
        print("id " +i)
        print(dic["rating"])
        c+=1
        if c==10000:
            break