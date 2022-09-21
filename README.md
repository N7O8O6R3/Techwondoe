# Techwondoe
Round1 Assignment

## <b>Local Environment Setup</b>

    ## Installing Virtual Environment
    
    python3 -m pip install --user virtualenv
    
    ## Creating Virtual Environment
    
    python3 -m venv <virtual_environment_name>
    
    ## Activating Virtual Environment
    
    <virtual_environment_name>/Scripts/activate      -> Windows
    
    source <virtual_environment_name>/bin/activate   -> Linux
    
## Clone Repository

    git clone https://github.com/N7O8O6R3/Techwondoe.git
    
## Install Dependencies

    cd CompanyTask
    
    pip3 install -r requirements.txt
    
## Run the Project

    python3 manage.py makemigrations
    
    python3 manage.py migrate
    
    python3 manage.py createsuperuser
    
    python3 manage.py runserver
    
### <b>Now Open Web Browser and search http://127.0.0.1:8000 </b>


## RUN PROJECT USING DOCKER

    docker-compose build
    
    Now Open Web Browser and search http://127.0.0.1:8000

# API Structure 
  
## Total Developed APIs
    
    ---> APIs created for POSTMAN(external use)
    
    1. Login API (For SuperUser Login)
    
    2. CreateCompany API (For Creating a Company)
    
    3. CreateTeam API (For Creating a Team in company)
    
    4. GetCompany API (For Getting a single Company Details with id)
    
    5. GetTeams API (For getting all teams of a Company)
    
    6. SearchCompanyByName API (For Searching a Company By Its name)
    
    ---> APIs used for GUI (Web Application Integration)
    
    1. Login API (For Super User Login)
    
    2. create_company API (For Creating a New Company)
    
    3. compnay API (For getting company details, all teams in company and for creating a new team)
    
    4. delete_company API (For deleting Company)
    
    5. delete_team API (For deleting a team from a company)
    
 
### You can find Complete API Documentation <a href="https://docs.google.com/document/d/1VUrhx5qRrrZI98LU9mJsE8HeW-7S3tOKio3I9tI1x00/edit?usp=sharing" target="_blank" > here</a>
    
    
# Note

### Here Initially I have developed mentioned 6 APIs( LoginAPIView, CreateCompany, CreateTeam, getCompanyAPI, getAllTeams, searchCompany_byName ) which are accessible using postman. Later I have developed another 8 APIs (login, home, create_comapny, getCompany, delete_team, logout, delete_company, contact) which are integrated with django templates. You can see all the apis in frontend. I have differentiated the POSTMAN apis and Template APIs in urls.py You can check it.
    

## I have attached the Screenshots of WebApp Pages and POSTMAN Results. you can check in screenshots folder.
