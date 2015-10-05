# Secure Static GAE Scaffold
A quick app engine skeleton for deploying static sites and protecting them from prying eyes

## What is this for?
Have a static site or just an HTML page you wanna show a client? Download the zip, unpack, install, add your files and you'll be able to deploy a protected site, with SSL, to app engine.

## Features
* Defaults to protected, including asset files (css, img and js)
* Allows management of authorized users
* Allows wild card domains, like leftfieldlabs.com, to allow whole groups

## TODO
* Tests
* Delete/update users

## Requirements
* Python 2.7
* [http://code.google.com/appengine/](GoogleAppEngineLauncher) >= 1.9.23 (installed and running)

## Using and deploying
1. Download zip
1. Rename unpacked folder to whatever you want
1. Run `./scripts/install` inside folder
1. When prompted, name your project the same as the app engine APP ID
1. Add your HTML files to app/templates/project
1. Add any static assets to app/templates/[css|js|img]
1. To view locally, run `./scripts/run`
1. To deploy, run `./scripts/deploy`
