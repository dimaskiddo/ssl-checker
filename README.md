# Domain SSL Checker using Python

This code will help you to automate Domain SSL expiration checking and will notify if the SSL expiration date is near of the treshold

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.
See deployment for notes on how to deploy the project on a live system.

### Prerequisites

Prequisites package:
* Python 3 (Python Runtime)

Optional package:
* Docker (Application Containerization)

### Installing

Below is the instructions to make this code running:
* Pull the code from this repository
```
git clone -b master https://github.com/dimaskiddo/ssl-checker.git
cd ssl-checker
```
* Remove any related git configuration
```
rm -rf .git
```
* Run following command to pull dependecies package
```
python3 -m venv .venv
source .venv/bin/activate

pip3 install --no-cache-dir --upgrade pip setuptools wheel
pip3 install --no-cache-dir -r requirements.txt
```
- Until this step you already can run this code by using this command
```
python3 main.py example.csv
```
- Exit from Virtual Environment
```
deactivate
```

## Running The Tests

Currently the test is not ready yet :)

## Built With

* [Python 3](https://www.python.org/) - Python Runtime
* [Docker](https://www.docker.com/) - Application Containerization

## Authors

* **Dimas Restu Hidayanto** - *Initial Work* - [DimasKiddo](https://github.com/dimaskiddo)

See also the list of [contributors](https://github.com/dimaskiddo/ssl-checker/contributors) who participated in this project

## Annotation

You can seek more information for the npm command parameters in the [package.json](https://raw.githubusercontent.com/dimaskiddo/ssl-checker/master/package.json)