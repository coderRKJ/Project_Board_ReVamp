# Project_Board_ReVamp
 This is a project for the Project Board ReVamp Challenge for WinHacks 2022.

 My implementation of this project is a Python-Flask sever that uses sever side rendering and SQLlite for database storage.

 There is a login page for Administrators, Partners and Students.

 Currently there is only sign in page for Partners and Students.

 ## Roles

 ### Partners
 - Have access to create, edit and delete projects.
 - Once approved they can select candidates who applied.
 ### Students
 - Have access to view approved projects.
 - Can select projects that listed and create applications for the same.
 ### Administrators
 - Currently only view submitted projects.
 - They can manually accept a project or reject with a specified reason.

 ## Features to be implemnted
 1. Some sign-up procedure for Administrators.
 1. Add more details such as profile photo uploads, project videos, markdown editor
 1. Notification (Push notification, email servers, etc.)

# Project Run Instructions
 To run this project clone this repository and add the following dependencies:
 ```bash
 sudo apt update
 sudo apt upgrade
 sudo apt install python3 python3-pip git htop vim screen dnsutils neofetch gunicorn
 ``` 
# Setup Candy (Optional)
## Installing Caddy

```bash
sudo apt install -y debian-keyring debian-archive-keyring apt-transport-https
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | sudo tee /etc/apt/trusted.gpg.d/caddy-stable.asc
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | sudo tee /etc/apt/sources.list.d/caddy-stable.list
sudo apt update
sudo apt install caddy
```

## Configuring Caddy

```bash
cd ~

# here, put in your Caddyfile config. An example of the required format is given in the repository
nano Caddyfile

sudo caddy stop
sudo caddy start
```

# Setting up and running the site

```bash
# cd into the project repo
cd <repo-name>
cp *.json secrets.json

# update your secret
nano secrets.json

# change debug=True to debug=False in app.py
nano app.py

# install python dependencies dependencies
pip install -r requirements.txt

# run the app!
python3 app.py &
```

**Credit:** This repo is based on Jeremie Bornais's [gcp-caddy-tutorial](https://github.com/jere-mie/gcp-caddy-tutorial)