# Salary Database Cleaning

This repository is dedicated to learning to `clean` and `preprocessing` a kaggle salary database.
The project involves applying various data cleaning techniques to ensure the data is accurate, consistent, and ready for analysis.

## Table of Contents

- [Introduction](#introduction)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)
- [Setup](#setup)
- [Usage](#usage)
- [Contributing](#contributing)

## Introduction

The main objective of this project is to practice and improve data cleaning skills using a kaggle salary database.
The database may contain various issues such as missing values, inconsistencies, and errors that need to be addressed.

## Project Structure

```bash
├── ds_salaries_messy.csv                # Unprocessed data files CSV
├── ds_salaries_messy.numbers            # Unprocessed data files NUMBERS
├── ds_salaries_cleaned.csv              # Cleaned and processed data files CSV
├── de_salaries_cleaned_excel.xlxs       # Cleaned and processed data files EXCEL
├── ds_salaries_messy.py                 # Python scripts for cleaning and processing data
└── README.md
```
`ds_salaries_messy.csv` and `ds_salaries_messy.numbers`: Contain the original, uncleaned data files.
`ds_salaries_cleaned.csv`: Contains the cleaned and processed data files in CSV format.
`de_salaries_cleaned_excel.xlxs`: Contains the cleaned and processed data files in an Excel file.
`ds_salaries_messy.py`: Python scripts that automate the data cleaning process.


## Technologies Used

- **Python**
- **Pandas**
- **PyCountry**
- **Matplotlib** *(for visualizations)*

## Setup

**Clone the repository:**
```bash
git clone https://github.com/yourusername/salary-database-cleaning.git
```
**Install the required packages:**
```bash
pip install -r requirements.txt
```

## Usage

Python Scripts: Run the scripts in the scripts/ directory to automate the cleaning process of the messy database.
Example:
```bash
python3 ds_salaries_messy.py
```

## Contributing

Contributions are welcome! Feel free to submit a pull request or open an issue if you find a bug or have a suggestion.
