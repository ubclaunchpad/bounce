/* eslint-disable-next-line no-unused-vars */
import React from 'react';
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
        const response = await fetch(this.url + endpoint, requestData);
        return await response.json();
    }

    /**
     * Authenticates with the backend, retreiving a JSON web token for the
     * given user that can be used to make authenticated calls to the backend.
     * @param {String} username
     * @param {String} password
     */
    async authenticate(username, password) {
        const response = await this._request('POST', '/auth/login', {
            username: username,
            password: password,
        });
        this.token = response.token;
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
}
