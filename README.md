# MovieRecommederSystem
This is our final year project


## Steps to run the project

1. Clone the project
`git clone https://github.com/iamrames/MovieRecommenderSystem.git`
2. Create a virtual environment

   - **Create and activate a virtual environment**

     ```bash
     # create virtual environment named "myenv"
     python3 -m venv myenv       # rename environment as required
     
     # activate the environment 
     source myenv/bin/activate   # for linux
     myenv\Scripts\activate      # for windows
     ```

3. Install flask, pandas
` pip install -r requirements.txt`
4. Run following command to start the project <br />
  <br />
  For Windows PowerShell, use $env: instead of export:<br />
  a. $env:FLASK_APP = "flaskr"<br />
  b. $env:FLASK_ENV = "development"<br />
  c. flask run<br />
  <br />
  For Windows cmd, use set instead of export:<br />
  a. set FLASK_APP=flaskr<br />
  b. set FLASK_ENV=development<br />
  c. flask run<br />
  <br />
  for linux or mac<br />
  a. $ export FLASK_APP=flaskr<br />
  b. $ export FLASK_ENV=development<br />
  c. $ flask run<br />
  
  
 `Note`
 Version to be used
  Flask>=1.0.2
  Flask-Login==0.4.1
  Werkzeug==0.14.1
