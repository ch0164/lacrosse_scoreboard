Our lacrosse scorebook website was created using the Python web framework, Django.
In order to build our project, Django and other dependencies must first be installed.
In addition, Python 3+ or higher must be installed and properly configured in the system's PATH (preferably version 3.10).
For ease of use builing this project, it is best to import this via JetBrains Pycharm (Community or Professional editions).

1. Run `pip install django-rest-framework` to install Django -- this gives access to some special commands.

2. Run `py.exe manage.py makemigrations` (if there are errors, it is because a missing package dependency is not installed -- 
   view the console output to `pip install' it appropriately, then run the command again after successful installation).

3. When the previous command is run successfully, run `py.exe manage.py migrate --run-syncdb`to create an empty db.sqlite3 database file
   (and like the previous step, `pip install` any dependencies if there are any and run the command again).

4. Finally, all that is left is to run the local webserver -- run `py.exe manage.py runserver`
   to see an instance created on one of your network's local ports.
