# swedishDemocracySearchTool22

## First time set up

### First time setting up environment:
Run `sh setup.sh` in the root of the folder. This creates a python virtual environment.

### Start environment:
`source sokvenv/bin/activate`

### Install requirements in environment
`pip install -r requirements.txt`

## If already set up before
Run `source sokvenv/bin/activate` to start environment. If new requirements are added you need to install those using `pip3 install -r requirements.txt`.

## Add Elastic credentials
In the `src` folder add a file called `example.ini`. It should include the Elastic Cloud credentials in the following format:

    [DEFAULT]
    cloud_id = {YOUR ELASTIC CLOUD ID}

    apikey_id = {YOUR ELASTICSEARCH API ID}

    apikey_key = {YOUR ELASTICSEARCH API KEY}

## Run local back-end server
In the `src` folder run:
`uvicorn main:app --reload`

If the elastic credentials was provided the back-end server will expose an API on http://localhost:8000/ see examples below:
 
http://localhost:8000/document/HAB313?text=true

http://localhost:8000/documents/search/?search_string=seniora%20åklagaren

http://localhost:8000/documents/search/?phrase_search=true&search_string=seniora%20%C3%A5klagaren

http://localhost:8000/documents/search/?end_date=2021-01-01&start_date=2018-03-08&search_string=en&phrase_search=true

## Run local front-end
From the root folder go to `./front-end/search-ui`
If it's the first time running the front-end, first run `npm install` to install
the dependencies.

Then run `npm run start`

The front-end should now run on http://localhost:3000/
