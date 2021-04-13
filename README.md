# redemet-crawler
A webcrawler for radar imagery from Brazil's airforce webpage.
This is a serverless aplication made to be run over AWS Lambda service.

# Installation
`npm install serverless`
`npm install serverless-requirements-plugin serverless-dotenv-plugin`
`pip install -r requirements.txt`




# Testing
export all Enviroment Variables using:
`export $(xargs < .env)`

To run all the tests use:
`pytest`

To run a specific test, use:
`pytest tests/<filename> -v`
Add `-v` for verbose mode
