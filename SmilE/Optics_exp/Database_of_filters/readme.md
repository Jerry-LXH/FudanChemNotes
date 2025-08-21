# Notes on Filter Database
### How to Add Filters to Database ?
- Data is stored in 2 tables in SQLite database (filters.db), which is connected with python through a bunch of ports.
- One may use the interactive 'import_or_revise_data.ipynb' to import wavelength(nm)-transmittion(0-100) csv data into the database. (Jupyter Notebook environment is required)
### How to Use the Database ?
- Run the script 'filter_viwer.py' to use the visualized browser interface, where a searching system(name/type/manufacturer/note) is avaliable. 
- Check the directory if anything goes wrong.
- Add Notes and the updates will be stored.
- 'Select' buttun allows one to combine filters, the data will be automatically interpolated if necessary.
