from cmath import nan
import pandas as pd
import numpy as np
import re

art = pd.read_csv('artwork_sample.csv', low_memory=False)
data = pd.read_csv('artwork_data.csv', low_memory=False)


# -------Understanding-------

print(art.head())
print(art.dtypes)

print(art.year)
print(art.year.min())
print(art.year.max())
print(art.year.std())
print(art.agg(['min','max','mean', 'std']))
print(art.agg('mean', axis = "columns"))


# -------Fixing-------

height = art.height
norm = (height - height.mean()) / height.std() #standardization
print(norm)

minmax = (height - height.min()) / (height.max() - height.min())
print(minmax.max(), minmax.min())

art['standardized_height'] = norm #Creates a new column
# art.new_column = norm |||| This will not create a new column use the above method
print(art.standardized_height)

print(art.height.transform(lambda x: x))
print(art.groupby('artist').transform('nunique')) 
print(art.groupby('artist')['height'].transform('mean')) 
art['mean_height_by_artist'] = art.groupby('artist')['height'].transform('mean')

print(art.filter(items = ['id', 'artist']))
print(art.filter(like = 'year'))
print(art.filter(like = 'artist'))
print(art.filter(regex = '(?i)year'))
print(art.filter(axis = 0, regex = '^100.$'))

art.drop(0)
#art.drop('id) won't work because drop defaults to rows first
art.drop('id', axis = 1) # This will work because the axis = 1 switches the operation from rows to columns!
art.drop(columns=['id']) # This also works and you can drop more than 1 by adding a comma and then another column name
art.drop(columns=['id'], inplace=True) #The inplace = True makes sure the dropped column stays dropped
art_spec = pd.read_csv('artwork_sample.csv', low_memory=False, usecols=['artist', 'title']) # This reads only the columns specified 

print(art.columns)
art.columns.str.lower() # Lowercases all the columns names
art.columns = [re.sub(r'([A-Z])', r'_\1', x).lower() for x in art.columns] # This converts the columns from camel case to snake case
print(art.columns)

art.rename(columns={"thumbnailUrl": "thumbnail"}, inplace=True)
art.rename(columns=lambda x: x.lower(), inplace=True)


# -------Filtering and Indexing-------

print(art['id'])
print(art['id'][1])
print(art[1:5]) # Gives rows 1-4, the first number is inclusive and the last number is exclusive
print(art[art['year']>1800]['year'])

print(art.loc[0:]) #access a group of rows or columns by label, the 0 represents the row label we want and the ':' gets all the columns
print(art.loc[0:2, ['artist', 'title']])
print(art.loc[art.artist == 'Blake, Robert', :])

print(art.iloc[0:3,:])
art.set_index('id', inplace=True)
print(art.iloc[0:3, :])
print(art.loc[1035:1037, :])

print(art.medium)
print(art.medium.str.contains('Graphite'))
print(art.loc[art.medium.str.contains('Graphite'), ['artist', 'medium']])
print(art.loc[art.medium.str.contains('Graphite',case=False),  ['artist', 'medium']])
print(art.loc[art.medium.str.contains('(?i)Graphite',regex=True)| art.medium.str.contains('(?i)Line',regex=True),  ['artist', 'medium']])
print(art.loc[art.medium.str.contains('graphite|line',regex=True, case=False), ['artist', 'medium']]) #Best way to search 


# -------Handling Bad Data-------

print(data.loc[data.title.str.contains('\s$', regex=True)]) #searches for rows where title ends in a white space character
data.title = data.title.str.strip() #removes white space
print(data.loc[data.title.str.contains('\s$', regex=True)])

print(pd.isna(data.loc[:, 'dateText'])) #shows wich dates are not a number, such as 'date not known'
data.replace({ 'dateText': {'date not known': nan}}, inplace=True) #uses the replace method from numpy to replace the 'date not known' dates to not a number values
print(pd.isna(data.loc[:, 'dateText']))
#a different way to do what the above lines do
data.loc[data.dateText == 'date not known', ['dateText']] = nan
print(data.loc[data.year.notnull() & data.year.astype(str).str.contains('[^0-9]')]) #finds all the data where the year is not already a number, but contains something other than a number
data.loc[data.year.notnull() & data.year.astype(str).str.contains('[^0-9]'), ['year']] = nan # sets that data to not a number

data.fillna(value={'depth': 0}, inplace=True) #fills the NaN values in depths to be 0

print(data.shape)
data.dropna() #drops rows based on if they have NaN as a value
print(data.dropna().shape)
data.dropna(thresh=15) #drops rows if they have up to 15 values as NaN. These rows might be considere 'bad' due to how much missing data is in them
data.dropna(subset=['year', 'acquisitionYear'], how='all', inplace=True) #if both of the selected rows are NaN, the row is dropped

data.drop_duplicates() #only drops rows if every value is an exact duplicate of another row
data.drop_duplicates(subset=['artist'], keep='first') #keeps the first row of each duplicate and drops the rest