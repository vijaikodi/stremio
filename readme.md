install on stremio using this link

 -https://vijai-stremio.herokuapp.com/manifest.json

To update the app

Install the Heroku CLI

Download and install the Heroku CLI.

If you haven't already, log in to your Heroku account and follow the prompts to create a new SSH public key.

```$ heroku login```

Clone the repository

Use Git to clone vijai-stremio's source code to your local machine.

```
$ heroku git:clone -a vijai-stremio
$ cd vijai-stremio
```

Activate virtual environment

```
Python -m venv venv
cd scripts/activate.bat
pip install -r requirements.txt
```


Deploy your changes

Make some changes to the code you just cloned and deploy them to Heroku using Git.

```
$ git add .
$ git commit -am "make it better"
$ git push heroku master
```

Thats it over !!!!
