# Web Application Exercise

Sienna Maguire, Marco Gulino, Elton Yu, Sai Shettar 

## Product vision statement

Virtual Closet is a social web app focused on photos of users’ outfits using a certain clothing piece and links for where to buy it, with these posts being organized into threads of different clothing pieces, and users can interact with each other through liking and commenting.


In addition to the product vision statement, here is our UXUI reference for this project.  
[Wireframe](https://www.figma.com/design/jC1TPpkBrygT6ArfWTVpap/Project-2---Web-App?node-id=0-1&t=OVJtM033yJkgKo67-1)
[Prototype](https://www.figma.com/proto/jC1TPpkBrygT6ArfWTVpap/Project-2---Web-App?node-id=12-14&t=oxoGThtGmibutCFw-1&scaling=scale-down&content-scaling=fixed&page-id=0%3A1&starting-point-node-id=12%3A117)

## User stories

[User Stories](https://github.com/users/elbow74/projects/3)

## Steps necessary to run the software

The fastest way to see Virtual Closet in action on your own computer is to use [Docker](https://www.docker.com).

First you must...

- install and run [docker desktop](https://www.docker.com/get-started)
- create a [dockerhub](https://hub.docker.com/signup) account

## How to Run Virtual Closet

Clone the repo and run 'python .automations/setup.py' in the directory.

### Set up a Python virtual environment

There are multiple ways to set up a Python virtual environment - a specific area of memory and disk space where you can install the dependencies and settings necessary to run a specific app in isolation from other apps on the same computer... here are instructions for using pipenv.

### Using pipenv

To create a virtual environment, you'll need to use pipenv, which needs to be installed. 

Install `pipenv` using `pip`:

```
pip3 install pipenv
```

Activate it:

```
pipenv shell
```

The `pip` settings file named, `requirements.txt` contains a list of dependencies - other Python modules that this app depends upon to run.

To install the dependencies into the currently-active virtual environment, use `pip`:

```bash
pip3 install -r requirements.txt
```

Run a virtual environment with the command 'cp env.example .env'.


Use Docker Compose to boot up both the `mongodb` database and the `flask-app` web app with one command:

- `docker compose up --force-recreate --build` ... add -d to run in detached/background mode.

If you see an error message that a particular port is already in use, select a different port for either the `flask-app` or `mongodb` service, as necessary. To do so, edit the first port number for that service in the `docker-compose.yml` file and try again. E.g., change the `flask-app`'s port to `10000:5000` if you want the flask app to run on port `10000` on your computer. If changing the `flask-app` port in this way, you must also update the `FLASK_PORT` setting in the `docker-compose.yml` file to match.

View the app in your browser:

- open a web browser and go to `http://localhost:5000` 

_Note that you edit any of the files in the project, you will have to stop and then restart the containers, as indicated above._

Virtual Closet has several screens. Create an account on the authentication page, then press continue.

You will then be brought to the home page. Here, you can create a post, check your profile, view/like existing posts, or search for specific captions and hashtags. 

If you'd like to go back to the home page after an action, simply press 'Back to Feed' at the top of the screen.

To stop running Virtual Closet, enter 'Cntrl + C' into your terminal, followed by 'docker compose down'


## Task boards

[Sprint 1](https://github.com/users/elbow74/projects/4) 
[Sprint 2](https://github.com/users/elbow74/projects/3)
