## fastapibasics

Fast API Basic code for references, make useful this.

# Support

For support or inquiries related to this project, please contact [sanjeevsanju929@gmail.com]).

## Create virtual environment and activate
```bash
python -m venv envname
```
## Installation
```bash
pip install -r requirements.txt
```
## Setup sql database
Open database.py file then replace your sql database name and password to SQLALCHEMY_DATABASE_URL variable.
```bash
SQLALCHEMY_DATABASE_URL = "postgresql://name:password@localhost:5432/postgres"
```
## Run the project using following command
```bash
cd sql_app
```
```bash
python main.py
```
Now your project is almost ready, you can view the Swagger UI by open your browser and type
### your ip address with port
```bash
127.0.0.1:8000/docs
```
Now you can see the Swagger UI click that and enter try make changes in body or value fields then click Execute.
your can see your response in Response field.

# Note

If any other queries visit official website [https://fastapi.tiangolo.com/tutorial/]).

