# Fortunoff-Archive-Project Installation Instructions

**Note:** The Python scripts for this web application were developed using a virtual Python environment (pipenv) for Python version control. Although this is not necessary to install this project, please do ensure all Python scripts are run with Python3 to avoid any errors.

Install Python modules (after installing pip):
```
pip install
```

Install npm packages:
```
npm install
```

After acquiring the ```.mrc``` and ```.csv``` data files, rename them ```fortunoff.mrc``` and ```path_data.csv```, respectively. Places these files into a folder named ```data```.
Sample path data available here
https://docs.google.com/spreadsheets/d/1BdhQ04tYE5m2QmQXM2G1Oxm4L89jjgkSE7C__Wb7C-c/edit?usp=sharing 

Run
```Python ./scripts/database.py```
to create the database file, create the necessary tables, and populate the database with data from the .mrc file.

Next, run
```Python ./scripts/csvData.py```
to populate the database with the places and paths data from the .csv file.

The ```resetdb.py``` script is also available to delete all data from the database while maintaining the overall schema.

Run
```node server```
and direct your browser to ```http://localhost:8080/``` to view the web application
