# Drawbridge
A tool to deploy a static site to a fully protected GAE instance

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
1. From inside the directory with all your site assets, run `drawbridge deploy [app-id] [release]`
1. Visit `[release]-dot-[app-id].appspot.com` to see your site

## Updating
Run `drawbridge update` from anywhere to get latest vault code

## Local server
Run `drawbridge local` from directory with content to test locally. Keep in mind this does not currently refresh code changes. You'll need to re-run the command to get latest changes from your code.

## Using DrawbridgeJS
If you are using Drawbridge, this is a tool to help you store data persistently in a rush. Think of Parse or Firebase, but exclusively for Drawbridge.

### Including it in your project
Simply add `<script src="/__tools__/drawbridge.js"></script>` to the `<head />` of your index.html and you're set.

### Notes
Just like Drawbridge, this is not intended to be high performing. Nor can you store tons of data. When you save, the data object is serialized and stored in a GAE Datastore instance. There is currently a 1MB max size.

### Example

```javascript
var dr = new Drawbridge.Record("some-drawbridge-project-name");
dr.set('someKey', 2); // Not yet saved
dr.set('someOtherKey', ["example", 2, "something"]); // Not yet saved
dr.save(function(data) {
    // on success, do something
});

console.log(dr.get('someKey'));

```


## Notes
* If a URI goes to a directory, like `http://someapp-dot-something.appspot.com/something/`, it will attempt to load an index.html. It will not work with anything else

## Feature requests
If you need a new feature, please create an issue or (better yet) submit a pull request.
