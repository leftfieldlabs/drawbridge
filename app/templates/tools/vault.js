/**
 * Copyright 2016-present, Left Field Labs, Inc.
 * All rights reserved.
 *
 * @providesModule Vault
 * @author Sebastian Lemery
 */

(function(global) {

    'use strict';

    /**
    * Create a new instance of Record
    * @param {string} releaseName - The name of your Vault project (usually top line of app.yaml)
    * @constructor
    */
    function Record(releaseName) {
        if (typeof releaseName === 'undefined') {
            console.error("Invalid releaseName supplied to Vault.Record. Please provide a string.");
            return;
        }
        this._releaseName = releaseName;
        this._xsrfToken = null;
        this._data = {};
    }

    /**
    * Fetches XSRF token
    * @param {Function} callback - Function to execute after load
    * @private
    */
    Record.prototype._getXSRFToken = function(callback) {

        if (typeof callback === 'undefined') {
            console.error("_getXSRFToken requires a callback");
            return;
        }

        this._get('/api/' + this._releaseName, callback);
    };

    /**
    * Makes remote call to save
    * @param {Function} callback - Function to execute after load
    * @private
    */
    Record.prototype._save = function(callback) {
        this._post("/api/" + this._releaseName + '/records/', this._data, callback);
    };

    /**
    * Shortcut for GET requests
    * @param {string} url - What URL to call
    * @param {Function} callback - Function to execute after load
    * @private
    */
    Record.prototype._get = function(url, callback) {
        var r = new XMLHttpRequest();
        r.open("GET", url, true);
        r.setRequestHeader('Content-Type', 'application/json');
        r.addEventListener("load", function(e) {
            var data = null;

            try {
                data = JSON.parse(r.responseText);
            } catch(err) {}

            if (typeof callback !== 'undefined') {
                callback(data);
            }
        });
        r.addEventListener("error", function(e) {
            console.error("vault-js could not connect to server: " + e);
        });
        r.send(null);
    };

    /**
    * Shortcut for POST requests
    * @param {string} url - What URL to call
    * @param {Object} data - Supplied data to pass to POST call
    * @param {Function} callback - Function to execute after load
    * @private
    */
    Record.prototype._post = function(url, data, callback) {
        var r = new XMLHttpRequest();
        r.open("POST", url, true);
        r.setRequestHeader('Content-Type', 'application/json');
        r.setRequestHeader('X-XSRF-TOKEN', this._xsrfToken);
        r.addEventListener("load", function() {
            var data = null;

            try {
                data = JSON.parse(r.responseText);
            } catch(err) {}

            if (typeof callback !== 'undefined') {
                callback(data);
            }
        });
        r.addEventListener("error", function(e) {
            console.error("vault-js could not connect to server: " + e);
        });
        r.send(JSON.stringify(data));
    };

    /**
    * Getter for private data object
    */
    Record.prototype.data = function() {
        return this._data;
    };

    /**
    * Set invidiual properties of the data object
    * @param {string} key - Key for value to be set
    * @param {string|integer|Object|Array} value - Value to be stored
    */
    Record.prototype.set = function(key, value) {
        this._data[key] = value;
    };

    /**
    * Get invidiual properties of the data object
    * @param {string} key - Key for value to be retrieved
    */
    Record.prototype.get = function(key) {
        return this._data[key];
    };

    /**
    * Get the latest data stored in remote storage
    * @param {Function} callback - Function to execute after load
    */
    Record.prototype.refresh = function (callback) {
        this._get("/api/" + this._releaseName + "/records/", function(data) {
            var cleaned = data['data'];
            this._data = cleaned;
            if (typeof callback !== 'undefined') {
                callback(cleaned);
            }
        }.bind(this));
    };

    /**
    * Send the local data to remote storage
    * @param {Function} callback - Function to execute after load
    */
    Record.prototype.save = function (callback) {
        // Check for XSRF token
        if (this._xsrfToken === null) {
            this._getXSRFToken(function(data) {
                this._xsrfToken = data['xsrf'];
                this._save(callback);
            }.bind(this));
        } else {
            this._save(callback);
        }
    };

    global.Vault = {
        Record: Record
    };

})(this);
