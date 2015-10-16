# Vault
A tool to deploy a static site to a fully protected GAE instance

![Vault Tect](fallout-boy.png)

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
1. Navigate to your newly cloned folder and run `sudo ./scripts/install`
1. Create an GAE app at [GAE console](http://console.developers.google.com) and get an app id
1. From inside the directory with all your site assets, run `vault deploy [gae app id]`
1. Visit `[gae app id].appspot.com` to see your site

## Notes
* When you deploy, make sure your updates are displayed by going to (replaced with your app id) https://console.developers.google.com/project/your-app-id-here/appengine/versions and setting the latest deploy to `default`
