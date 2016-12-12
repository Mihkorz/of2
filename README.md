OncoFinder 2
============

Versions
--------
Tested on:
- Ubuntu 14.04.3 LTS, Python 2.7
- R version 3.2.3, 2015-12-10

Install
-------
To install OncoFinder go to `environment` directory, then:

1) Install Ubuntu packages:
```
cd environment/packages
sudo ./install_packages.sh
```

Probably you need MySQL and Python virtual environment as well:
```
sudo apt-get install -y mysql-server
sudo apt-get install -y python-virtualenv
```

2) Make sure `pip` is up-to-date (in virtual environment or globally, it's up to you):

```
pip install -upgrade pip
```

Then install required packages:
```
pip install -r python/requirements_<env>.txt
```

3) Install R packages listed in `R/R_reqs.txt`.

4) Create MySQL database `oncoFinder2` (check the name in the `settings_*.py`) and populate it.
