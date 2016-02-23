# Vault
A tool to deploy a static site to a fully protected GAE instance

![Vault Tect](fallout-boy.png)

## What is this for?
Have a static site or just an HTML page you wanna show a client? You can easily push content to a remote, secure and whitelisted site.

## Release 2.0
Now manages all projects under a single GAE App ID. Each project is considered a project version, which gets around the 10 project limit Google imposes.

## Features
* Defaults to protected, including asset files (css, img and js)
* Allows management of authorized users @ /admin
* Allows wild card domains, like `leftfieldlabs.com`, to allow whole groups

## TODO
* Tests
* Cleaner admin
* ~~Apps are deployed to subdomain of unified system~~
* ~~Delete/update users~~

## Requirements
* Python 2.7
* [GoogleAppEngineLauncher](http://code.google.com/appengine/) >= 1.9.23 (installed and running)

## Installing
1. Clone repo
1. Navigate to your newly cloned folder and run `sudo ./scripts/install`

## Using and deploying
1. From inside the directory with all your site assets, run `vault deploy [project name]`
1. Visit `[project name]-dot-lflwebreview.appspot.com` to see your site

## Updating
Run `vault update` from anywhere to get latest vault code

## Local server
Run `vault local` from directory with content to test locally. Keep in mind this does not currently refresh code changes. You'll need to re-run the command to get latest changes from your code.

## Notes
* If a URI goes to a directory, like `http://someapp-dot-lflwebreview.appspot.com/something/`, it will attempt to load an index.html. It will not work with anything else

## Feature requests
If you need a new feature, please create an issue or (better yet) submit a pull request.
