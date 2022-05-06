# swedishDemocracySearchTool22

## First time set up
### First time seting up enviroment:
`sh setup.sh`

### Start enviroment:
`source sokvenv/bin/activate`

### Install requriments in enviroment
`pip install -r requirements.txt`

## After first time set up
Run `source sokvenv/bin/activate` to start enviroment. If new requriemnts are added you need to install those using `pip3 install -r requirements.txt`.

# Run server
In the src folder run:
uvicorn main:app --reload

## Example queries

`http://localhost:8000/document/HAB313?text=true`

`http://localhost:8000/documents/search/?search_string=seniora%20åklagaren`

`http://localhost:8000/documents/search/?phrase_search=true&search_string=seniora%20%C3%A5klagaren`

`http://localhost:8000/documents/search/?end_date=2021-01-01&start_date=2018-03-08&search_string=en&phrase_search=true`

