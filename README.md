# Vault
A tool to deploy a static site to a fully protected GAE instance

## What is this for?
Have a static site or just an HTML page you wanna show a client? You can easily push content to a remote, secure and whitelisted site.

## Features
* Defaults to protected, including asset files (css, img and js)
* Allows management of authorized users @ /admin
* Allows wild card domains, like leftfieldlabs.com, to allow whole groups

## TODO
* Tests
* ~~Delete/update users~~

## Requirements
* Python 2.7
* [GoogleAppEngineLauncher](http://code.google.com/appengine/) >= 1.9.23 (installed and running)

## Using and deploying
1. Clone repo
2. Run `./scripts/install`
3. Run `vault deploy [gae app id]`
4. Visit `[gae app id].appspot.com` to see your site
