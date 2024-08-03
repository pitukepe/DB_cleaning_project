import pandas as pd
import matplotlib.pyplot as plt
import pycountry

sales = pd.read_csv("ds_salaries_messy.csv",delimiter=';',parse_dates=["work_year"])

##rmving dupes
sales.drop_duplicates(inplace=True)
sales.reset_index(inplace=True, drop=True)

##finding NaN's and then rmving NaN's
nulls = [(index, col) for index, row in sales.iterrows() for col in sales.columns if pd.isnull(row[col])]
sales.drop([index[0] for index in nulls], inplace=True)
sales.reset_index(inplace=True, drop=True)

##finding and repairing messy values
sales["salary"] = pd.to_numeric(sales["salary"], errors='coerce')
sales["remote_ratio"] = pd.to_numeric(sales["remote_ratio"], errors='coerce')
sales["company_size"] = sales["company_size"].apply(lambda x: x if isinstance(x,str) and not x.replace(".","").isdigit() else None)
##dropping again (with a different way), since we coerced messy values
sales.drop(sales.loc[sales.isnull().any(axis=1)].index, inplace=True)
sales.reset_index(inplace=True, drop=True)

##remapping values for improved readability
explvl_map = {
    'SE' : 'Senior',
    'EX' : 'Executive',
    'EN' : 'Junior',
    'MI' : 'Middle'
}
comsize_map = {
    'M': 'Middle',
    'L': 'Large',
    'S': 'Small'
}
remrat_map = {
    0: 'Not remote',
    50: 'Partially remote',
    100: 'Fully remote'
}
emptyp_map = {
    'FT': 'Full time',
    'PT': 'Part time',
    'CT': 'Contract',
    'FL': 'Freelance'
}
sales["experience_level"] = sales['experience_level'].map(explvl_map)
sales["company_size"] = sales["company_size"].map(comsize_map)
sales["remote_ratio"] = sales["remote_ratio"].map(remrat_map)
sales["employment_type"] = sales['employment_type'].map(emptyp_map)

##iso2 to iso3
sales['employee_residence'] = sales['employee_residence'].apply(lambda iso2: pycountry.countries.get(alpha_2=iso2).alpha_3)
sales['company_location'] = sales['company_location'].apply(lambda iso2: pycountry.countries.get(alpha_2=iso2).alpha_3)

## Changing indexing from start0 to start1
sales.index = pd.RangeIndex(start=1, stop=len(sales)+1, step=1)

##saving the cleaned data to a new file
#sales.to_csv("ds_salaries_cleaned.csv", index=False)


data = {
    'data' : [1, 1, 1, 1, 1, 1, 4, 6]
}

test = pd.DataFrame(data)
print(test.describe())

test['data'].plot(kind='box', figsize=(10,4), vert=False)
plt.axvline(test['data'].mean(), color="red", ls="--")
plt.show()