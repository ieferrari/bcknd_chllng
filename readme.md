# Software Engineer - Exercise

> script to normalize the company name variations using fuzzywuzzy library and  python-Levenshtein to speed up the process

# Quick setup

Create virtual env, activate it and install packages 

```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Run on with default values (in the root of this repo)

```
python script.py
```

console output:
```
input file: patent-backend-challenge.csv ,       unique organizations: 34 
input file: fixed_patent-backend-challenge.csv ,         unique organizations: 4
```



***
***
***


# Usage examples


### Help command
```
python script.py --help
```

```
Take a .csv file as input, will use fuzzy match to   fix the cities names
  (grouped by country) fix the organization name (grouped by country & city)
  output the fixed .csv file adding the fixed_ prefix to input_file name

Options:
  --input-file TEXT               [default: patent-backend-challenge.csv]
  --min-fuzzy-dist INTEGER        [default: 60]
  --company-suffixes TEXT         [default: LLC, LLP, LTD, INC]
```


### Change target input-file

```
python script.py --input-file my_file.csv
```

### Change target minimum fuzzy distance to compare

```
python script.py --min-fuzzy-dist 90
```

### Example with custom fuzzy distance, and custom company-suffixes to remove

```
python script.py --min-fuzzy-dist 90 --company-suffixes LLC --company-suffixes NEW_EXPRESSION
```

> notice that you need to call the option  `--company-suffixes` once for each element in the new list