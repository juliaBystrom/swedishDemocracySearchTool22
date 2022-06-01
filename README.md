# swedishDemocracySearchTool22



## First time set up
### First time seting up enviroment:
run `sh setup.sh` in the root of the folder. This creates a python virtual enviroment.

### Start enviroment:
`source sokvenv/bin/activate`

### Install requriments in enviroment
`pip install -r requirements.txt`

## If already set up before
Run `source sokvenv/bin/activate` to start enviroment. If new requriemnts are added you need to install those using `pip3 install -r requirements.txt`.

## Add Elastic credentials
In the src folder add an file called `example.ini`. It should include the elastic instance credentials by beeing filled in like this:

    [DEFAULT]
    cloud_id = {YOUR ELASTIC CLOUD ID}

    apikey_id = {YOUR ELASTICSEARCH API ID}

    apikey_key = {YOUR ELASTICSEARCH API KEY}

## Run local backend server
In the src folder run:
uvicorn main:app --reload

If the elastic credentials was provided the backend server will expouse an API on http://localhost:8000/ see examples below:
 
http://localhost:8000/document/HAB313?text=true

http://localhost:8000/documents/search/?search_string=seniora%20åklagaren

http://localhost:8000/documents/search/?phrase_search=true&search_string=seniora%20%C3%A5klagaren

http://localhost:8000/documents/search/?end_date=2021-01-01&start_date=2018-03-08&search_string=en&phrase_search=true



## Run local front-end
From the root folder go to ./front-end/search-ui and run
`npm run start`
It should now run on http://localhost:3000/
