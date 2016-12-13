OncoFinder 2
============

Versions
--------
Tested on:
- Ubuntu 14.04.3 LTS, Python 2.7
- R version 3.2.3, 2015-12-10


Install
-------
Everything related to installations is in `environment` directory

1) Install Ubuntu packages:
```
cd environment/packages
sudo ./install_packages.sh
```

Install MySQL if it is not installed:
```
sudo apt-get install -y mysql-server
```

Optionally install Python virtual environment:
```
sudo apt-get install -y python-virtualenv
```

Make sure `pip` is up-to-date (in a virtual environment / globally):

```
pip install -upgrade pip
```

2) Install Python packages:

```
cd environment/python
pip install -r requirements_<env>.txt
```

3) Install R packages listed in `R/R_reqs.txt`.

4) Create MySQL database `oncoFinder2` (check the name in the `settings_*.py`).
Populate it with data from backup (not included into the repository).


Test
----
Powered by py.test. There are some predefined *.ini files: `pytest_TEST_TYPE.ini`.

`test.sh` runs all tests (unit, functional, etc.):
```
./test.sh [OPTIONS]
```
