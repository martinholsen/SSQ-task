author: Martin H. Olsen

# This project is to be used as a talent assessment of its author

I have chosen to answer the task using python as it is the programming language I am currently most familiar with. It
might not be the ideal programming language for developing an app but it should suffice.

Initially the idea was to implement a SQLAlchemy database to store the data locally but this was dropped after the
author better understood the assignment. The data is now taken directly from the online database through url request and query.

## webapp enviornment setup

To avoid issues with downloading dependencies locally we first create an environment. The environment should have already
been created as 'webapp_env' but in case this environment gives you issues I suggest creating a new one. To do this, first
make sure you have a working version of python installed. This can be found in the microsoft store on windows or through the
python website. Once it is installed, use 'pip install virtualenv' or 'pip3 install virtualenv' to get the environment 
package we will be using. To create the enviornment we now type 'python -m venv /path/to/your/environment' on windows or 
'virtualenv path/...' on mac/linux. To activate the environment we use '\path\to\env\Scripts\activate' with windows or 
'source \path\..\bin\activate'. Once the environment is set up we can finally download our dependencies with 
'pip install -r requirements.txt'. Now the required files should be installed and you should be good to go.

## Flask project setup

To setup the project simply navigate out of the folder and type in the following command 'export FLASK_APP=project_name' 
or 'set FLASK_APP=project_name' if you are running this on windows. To run the project now simply run 
'flask run' and it should work.

# Deprecated section

## Flask SQLAlchemy DB

In this project the database is manually created by opening inline python and executing two lines of code:
"""
from folder-/project-name import db, create_app
db.create_all(app=create_app())
"""

