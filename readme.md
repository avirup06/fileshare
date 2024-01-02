
# Project Title

A fastapi based simple filesharing application where one user can upload files and share with another user to be downloaded. The user can also set expiry time for each uploaded files after which it cannot be downloaded and deleted from the server.


## Authors

- [Avirup Banerjee @avirup06](https://www.github.com/avirup06)


## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`STAGE`

`STORAGE`


## Run Locally

Clone the project

poetry is required

```bash
  git clone https://link-to-project
```

Go to the project directory

```bash
  cd fileshare
```

Install dependencies

```bash
  poetry install
  poetry shell
```

Start the server

```bash
  poetry run server
```


## Tech Stack


**Server:** Python, FastAPI, PostgreSQL, SQLAlchemy, Poetry

