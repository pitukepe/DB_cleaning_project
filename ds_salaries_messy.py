import pandas as pd
import matplotlib.pyplot as plt
import pycountry

sales = pd.read_csv("ds_salaries_messy.csv",delimiter=';',parse_dates=["work_year"])

##rmving dupes
sales.drop_duplicates(inplace=True)
sales.reset_index(inplace=True, drop=True)

##finding NaN's and then rmving NaN's
nulls = [(index, col) for index, row in sales.iterrows() for col in sales.columns if pd.isnull(row[col])]
sales.drop([i[0] for i in nulls], inplace=True)
sales.reset_index(inplace=True, drop=True)

##finding and repairing messy values
sales["salary"] = pd.to_numeric(sales["salary"], errors='coerce')
sales["remote_ratio"] = pd.to_numeric(sales["remote_ratio"], errors='coerce')
sales["company_size"] = sales["company_size"].apply(lambda x: x if isinstance(x,str) and not x.replace(".","").isdigit() else None)
##dropping again (with a different way), since we coerced messy values
sales.dropna(how='any', inplace=True)
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

##iso2 to iso3 (we can change '.alpha_3' to '.name' for the full name of the country)
sales['employee_residence'] = sales['employee_residence'].apply(lambda iso2: pycountry.countries.get(alpha_2=iso2).alpha_3)
sales['company_location'] = sales['company_location'].apply(lambda iso2: pycountry.countries.get(alpha_2=iso2).alpha_3)

##iso3 to full name for the currency abbreviations
sales['salary_currency'] = sales['salary_currency'].apply(lambda iso3: pycountry.currencies.get(alpha_3=iso3).name)


## Changing indexing from start=0 to start=1
sales.index = pd.RangeIndex(start=1, stop=len(sales)+1, step=1)

##saving the cleaned data to a new csv file
#sales.to_csv("ds_salaries_cleaned.csv", index=False)

##saving the cleaned data to a new excel file (openpyxl module needed)
#sales.to_excel("ds_salaries_cleaned_excel.xlsx", index=False)


data = pd.DataFrame({'month':['january', 'february', 'march','april','may'], 'salesman':['mark', 'jan', 'pete', 'michael','alex'],'sales':[1234,415,453,3,12], 'profit':[123,41,45,3,12], 'expenses':[12,4,4,3,1]})
melted = data.melt(id_vars=['month','salesman'], var_name='type', value_name='num')

crosstab = pd.crosstab(data['month'], data['sales'].diff() > 0, colnames=['higher than previous month'], rownames=['months'])


print(crosstab)
