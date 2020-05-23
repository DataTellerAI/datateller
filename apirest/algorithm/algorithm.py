from pymongo import MongoClient
import pandas as pd

# client = MongoClient("mongodb://Campo:Campo1987@names-shard-00-00-f54kh.mongodb.net:27017,\
# 					  names-shard-00-01-f54kh.mongodb.net:27017,\
# 					  names-shard-00-02-f54kh.mongodb.net:27017/test?ssl=true&\
# 					  replicaSet=names-shard-0&authSource=admin&retryWrites=true&w=majority")
# db = client.Names
# collection = db.genderName
# objs = db.genderName.find({"Pais": "USA"})
# for i in objs:
# 	print(i)
# data = pd.DataFrame(list(collection.find()))




import os
print(os.getcwd())
os.chdir()


import pandas as pd

df = pd.read_excel('/Users/campopinillos/Documents/Proyecto Final/nombres.xlsx')
print(type(df))
print(df.head())



input = sys.argv[1].lower()
gender = ''
probability = ''
# if (len(input) == 2): 
	
name = input.split(" ") 

if (name[0][-1] == 'a'): 
	gender = 'Female'
	probability = 1
elif (name[0][-1] == 'o'): 
	gender = 'Male'
	probability = 1

print('Name: {}\nGender: {}\nProbability: {}'.format(input.title(), gender, probability))


