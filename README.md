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
* Cleaner admin
* ~~Delete/update users~~

## Requirements
* Python 2.7
* [GoogleAppEngineLauncher](http://code.google.com/appengine/) >= 1.9.23 (installed and running)

## Installing
1. Clone repo
1. Navigate to your newly cloned folder and run `sudo ./scripts/install`

## Using and deploying
1. Create a GAE app (if you don't already have one) at [GAE console](http://console.developers.google.com) and get an app id
1. From inside the directory with all your site assets, run `vault deploy [gae app id]`
1. Visit `[gae app id].appspot.com` to see your site

## Updating
Run `vault update` from anywhere to get latest vault code

## Local server
Run `vault local` from directory with content to test locally

## Notes
* If a URI goes to a directory, like `http://someapp.appspot.com/something/`, it will attempt to load an index.html. It will not work with anything else
* `vault deploy` automatically sets your new deploy as default

## Feature requests
If you need a new feature, please create an issue or (better yet) submit a pull request.
