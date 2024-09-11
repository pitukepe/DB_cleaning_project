import pandas as pd
import matplotlib.pyplot as plt
import pycountry
import numpy as np

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


## Changing indexing from start=0 to start=1
sales.index = pd.RangeIndex(start=1, stop=len(sales)+1, step=1)

## Saving the cleaned data to a new csv file
#sales.to_csv("ds_salaries_cleaned.csv", index=False)

## Saving the cleaned data to a new excel file (openpyxl module needed)
#sales.to_excel("ds_salaries_cleaned_excel.xlsx", index=False)

#plotting the data

fig, axs = plt.subplots(2,2,figsize=(7,7))

# plotting a histogram
histogram = sales["salary_in_usd"].plot(kind="hist", bins=30, ax=axs[0,0], title="Salary Histogram", xlabel="Salary in USD", ylabel="Frequency", color = "green", alpha=0.4, density=True)
sales["salary_in_usd"].plot(kind="kde", ax=histogram, color="red", alpha=0.4)
histogram.set_xticks(np.arange(-200000, 800001, 150000),labels=["-200k", "-50k", "100k", "350k", "500k", "650k", "800k"])

# plotting a boxplot
box = sales["salary_in_usd"].plot(kind="box", ax=axs[0,1], title="Salary Boxplot", color="green", vert=False)
# k as a shortcuts 1000's for x ticks
box.set_xticks(np.arange(0, 400001, 100000), labels=["0", "100k", "200k", "300k", "400k"])
box.axvline(sales["salary_in_usd"].mean(), color="red", linestyle="-.")
box.text(sales["salary_in_usd"].mean()+8000, 0.52, f"Mean: {round(sales['salary_in_usd'].mean())}", color="red", fontsize=9)


# getting outliers
outliers = sales[sales["salary_in_usd"] > sales["salary_in_usd"].quantile(0.99)]

# plotting a histogram of outliers
outlier_hist = outliers["salary_in_usd"].plot(kind="hist", bins=10, ax=axs[1,0], title="Outliers Histogram", xlabel="Salary in USD", ylabel="Frequency", color = "red", alpha=0.4, density=True)
outliers["salary_in_usd"].plot(kind="kde", ax=outlier_hist, color="green", alpha=0.7)
outlier_hist.set_xticks(np.arange(250000, 500001, 50000), labels=["250k", "300k", "350k", "400k", "450k","500k"])

# defining a custom autopct for pie plot
def mypct(values):
    def toto(pct):
        total = sum(values)
        unique = int(round(pct/100*total))
        return f"{pct:.2f}%\n({unique:d})"
    return toto
# plotting an outlier pie chart
pie_plpt = outliers["experience_level"].value_counts().plot(kind="pie", ylabel="", labels=outliers["experience_level"].unique(), title="Outliers by Experience Levels", autopct=mypct(outliers["experience_level"].value_counts()), ax=axs[1,1])

plt.tight_layout()
plt.show()
