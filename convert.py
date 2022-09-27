import pandas as pd
  
# read contents of csv file
file = pd.read_csv("questionsdata.csv")
print("\nOriginal file:")
print(file)
  
# adding header
headerList = ['prompt', 'completion']
  
# converting data frame to csv
file.to_csv("questionsdata2.csv", header=headerList, index=False)
  
# display modified csv file
file2 = pd.read_csv("questionsdata2.csv")
print('\nModified file:')
print(file2)