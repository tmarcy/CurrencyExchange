# Project Title

Currency Exchange

## The project in short

Simple Google App Engine Web Application example with minimal style, written in Python 2.7, using API to convert 
different currencies (see references in "Built With" section).


## Specifications

* A form is used to retrieve conversion data.
* The app response shows conversion result. 
* User data and conversions are saved automatically in the Datastore.
* Two API GET are given to show statistics about user conversions.
* An API POST is given: it allows inserting a new conversion in the Datastore; 
in this case, parameters control is not required.

## Before starting
* Add a lib folder to the project, in which you have to install the libraries listed in "requirements.txt" file.
* You must ask for an API key here: http://data.fixer.io/api/latest, in order to use the service; paste it in the 
variable named "API_KEY" before you run this project.
Please, PAY ATTENTION: be sure to select "FREE" type account in the site.

## Built With

* [Google App Engine](https://cloud.google.com/appengine) - Platform used
* [Flask](http://flask.pocoo.org/) - The microframework for Python used
* [data.fixer](http://data.fixer.io/api/latest) - API usedl

## Author

**Marcella Tincani** - [Marcella](https://github.com/tmarcy)
