ALMAFE-CTS-Database
===================
Python classes for access to the NRAO ALMA Band 6 database.

The package **[DBBand6Cart](https://gitlab.nrao.edu/mmcleod/almafe-cts-database/-/tree/master/DBBand6Cart)** contains a module for each table of interest in the database.

Each module has create, read, update, and delete methods, as required.

**[schemas](https://gitlab.nrao.edu/mmcleod/almafe-cts-database/-/tree/master/DBBand6Cart/schemas)** contains data models corresponding to individual records of the tables, plus helper data models and enums.

By convention in this package, **schemas** have singular names and top-level classes have plural names.  E.g. `./schemas/CartTest` corresponds to `./CartTests` and `./schemas/BPRawDatum` is for `./BPRawData`.

**[Tests](https://gitlab.nrao.edu/mmcleod/almafe-cts-database/-/tree/master/DBBand6Cart/Tests)** contains unit tests for each table and data model.

### _Project-level files_
**ALMAFE-CTS-Database_template.ini**: Rename this to ALMAFE-CTS-Database.ini and provide the database credentials.  This is only required to run the Tests.  Otherwise, credentials will be provided by the application using this package.

**.gitignore**: We don't want to check in datbase credentials, .pyc files, and .vscode files.

**requirements.txt**: Other packages required by this one.  In your Python environment:

`pip install -r requirements.txt`

notes:
* **pydantic** is required for all the **schemas**.
* **ALMAFE-Lib** contains shared routines and database access wrappers used by all the classes.
* **pandas** is only used by the noise temperature classes: **NoiseTempRawData.py, NoiseTempCalcData.py, WarmIFNoiseData.py**.  You can remove this requirement if your application doesn't need use those.
