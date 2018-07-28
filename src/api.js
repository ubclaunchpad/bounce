/* eslint-disable no-unused-vars */
import React from 'react';
/* eslint-enable no-unused-vars */
import 'whatwg-fetch';

export default class BounceClient {
    constructor(url) {
        this.url = url;
        this.token = null;
    }

    /**
     * Makes a request with the given method to the given endpoint with the
     * given body.
     * @param {String} method The HTTP method
     * @param {String} endpoint The URI to which the request will be made
     * @param {Object} body The body of the request (optional, may be undefined)
     */
    async _request(method, endpoint, body) {
        let requestData = {
            method: method,
            headers: {},
        };
        if (body) {
            requestData.body = JSON.stringify(body);
            requestData.headers['Content-Type'] = 'application/json';
        }
        if (this.token) {
            // The access token is available so put it in the request header
            requestData.headers['Authorization'] = this.token;
        }
        return await fetch(this.url + endpoint, requestData);
    }

    /**
     * Authenticates with the backend, retreiving a JSON web token for the
     * given user that can be used to make authenticated calls to the backend.
     * @param {String} username
     * @param {String} password
     */
    async authenticate(username, password) {
        return await this._request('POST', '/auth/login', {
            username: username,
            password: password,
        });
    }

    /**
     * Returns information about the user with the given username
     * @param {String} username
     */
    async getUser(username) {
        return await this._request('GET', '/users/' + username);
    }

    /**
     * Creates a new Bounce user and returns information about the user
     * @param {String} fullName The full name of the user
     * @param {String} username The username to give to the new user
     * @param {String} password The new user's password
     * @param {String} email The user's email
     */
    async createUser(fullName, username, password, email) {
        return await this._request('POST', '/users', {
            full_name: fullName,
            username: username,
            password: password,
            email: email,
        });
    }

    /**
     * Updates a user's information
     * @param {String} username
     * @param {String} fullName Optional, may be undefined
     * @param {String} email Optional, may be undefined
     */
    async updateUser(username, fullName, email) {
        let body = {};
        if (fullName) {
            body.full_name = fullName;
        }
        if (email) {
            body.email = email;
        }
        return await this._request('PUT', '/users/' + username, body);
    }

    /**
     * Deletes a user
     * @param {String} username
     */
    async deleteUser(username) {
        return await this._request('DELETE', '/users/' + username);
    }

    /**
     * Fetch information about a club
     * @param {String} name
     */
    async getClub(name) {
        return await this._request('GET', '/clubs/' + name);
    }

    /**
     * Create a new club with the given properties
     * @param {String} name
     * @param {String} description
     * @param {String} websiteUrl
     * @param {String} facebookUrl
     * @param {String} instagramUrl
     * @param {String} twitterUrl
     */
    async createClub(name, description, websiteUrl, facebookUrl, instagramUrl, twitterUrl) {
        return await this._request('POST', '/clubs', {
            name: name,
            description: description,
            websiteUrl: websiteUrl,
            facebookUrl: facebookUrl,
            instagramUrl: instagramUrl,
            twitterUrl: twitterUrl,
        });
    }

    /**
     * Update a club's information whatever new information is provided
     * @param {String} name The name of the club to update
     * @param {String} newName (optional) The club's new name
     * @param {String} description (optional) The club's new description
     * @param {String} websiteUrl (optional) The club's new websiteUrl
     * @param {String} facebookUrl (optional) The club's new facebookUrl
     * @param {String} instagramUrl (optional) The club's new instagramUrl
     * @param {String} twitterUrl (optional) The club's new twitterUrl
     */
    async updateClub(name, newName, description, websiteUrl, facebookUrl, instagramUrl, twitterUrl) {
        const props = {
            name: newName,
            description: description,
            websiteUrl: websiteUrl,
            facebookUrl: facebookUrl,
            instagramUrl: instagramUrl,
            twitterUrl: twitterUrl,
        };
        // Remove properties that were not set
        for (let prop in props) {
            if (!props[prop]) {
                delete props[prop];
            }
        }
        return await this._request('PUT', '/clubs/' + name, props);
    }

    /**
     * Delete the club with the given name
     * @param {String} name
     */
    async deleteClub(name) {
        return await this._request('DELETE', '/clubs/' + name);
    }
}
