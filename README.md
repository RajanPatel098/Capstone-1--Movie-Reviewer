# Capstone-1--Movie-Reviewer
Movie Reviewer Using OMDBAPI

https://www.omdbapi.com/


 ## Purpose

This OMDB web appliation will allow for users to search for movies and create reviews for any movie. 

User Demographics

Anyone who enjoys watching movies and wants to track/comment on what they've recently seen would be able to use this.

## API Used:
https://www.omdbapi.com/  retrieving all movie info including posters for movies.

## Technology Stack Used:

Backend: Python, Flask, and PostgresSQL

Frontend:  Javascript, HTML, CSS, and Bootstrap

## Functionality of the App:

User will be able to create their own profile

User can search for any movie

Authenticated Users (logged in users) will be able to leave a comment and record what they recently watched.

## User Flow:

User logs on and is able to see all their previous reviews.

User can search for a movie on homepage

## How to Run:
__ 1) Download the .zip of this repository
__ 2) Unpack anywhere easily accesible by your WSL/Ubuntu client
   3)  Start your postgresql server and load the database by running models.py
   3) Create a virtual env using 'python3 -m venv venv' then enter the virtual environment by doing 'source venv/bin/activate'
   4) Install all necessary repositories using python3 (flask, bcrypt, sqlalchemy, etc)
   5)  Run 'flask run'  and the site will exist on localhost:5000
