# Fortunoff-Archive-Project Installation Instructions

**Note:** The Python scripts for this web application were developed using a virtual Python environment (pipenv) for Python version control. Although this is not necessary to install this project, please do ensure all Python scripts are run with Python3 to avoid any errors.

Install Python modules (after installing pip):
```
pipenv install
```
If you're having difficulties, install these packages:
```
pip3 install pymarc
pip3 install requests
```
Install npm packages:
```
npm install sqlite3
npm install
```

After acquiring the ```.mrc``` and ```.csv``` data files, rename them ```fortunoff.mrc``` and ```path_data.csv```, respectively. Places these files into a folder named ```data``` in the scripts folder.

Sample path data available here:
https://docs.google.com/spreadsheets/d/1BdhQ04tYE5m2QmQXM2G1Oxm4L89jjgkSE7C__Wb7C-c/edit?usp=sharing 

Run
```Python ./scripts/database.py```
to create the database file, create the necessary tables, and populate the database with data from the .mrc file.

Next, run
```Python ./scripts/csvData.py```
to populate the database with the places and paths data from the .csv file. This will take a bit (set a time for 4 minutes and let it run) as the API requests can take some time. 

The ```resetdb.py``` script is also available to delete all data from the database while maintaining the overall schema.

Run
```node server```
and the server should run on ```https://localhost:3000```

Then enter the ```arcgis-vue-app``` and run ```npm start```. Redirect your browser to ```https://localhost:8080```, or the server indicated in the terminal to view the web application.
