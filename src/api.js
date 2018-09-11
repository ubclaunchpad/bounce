import 'whatwg-fetch';
import jwtDecode from 'jwt-decode';

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
     * @param {Object} params The request parameters (optional, may be undefined)
     */
    async _request(method, endpoint, body, params) {
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
        if (params) {
            // Append request params if necessary
            endpoint += '?';
            for (let key in params) {
                const value = encodeURIComponent(params[key]);
                endpoint += `${key}=${value}&`;
            }
        }
        return await fetch(this.url + endpoint, requestData);
    }

    /**
     * Returns true if the user is signed in and false otherwise.
     */
    isSignedIn() {
        return !!this.token;
    }

    /**
     * Returns the user ID in the JWT we were given on sign-in.
     */
    getUserIdFromToken() {
        if (!this.token) {
            return null;
        }
        return jwtDecode(this.token).id;
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
        if (response.ok) {
            this.token = (await response.json())['token'];
        }
        return Promise.resolve(response);
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
     * Returns a list of clubs that match the given query.
     * @param {String} query
     */
    async searchClubs(query) {
        return await this._request('GET', `/clubs/search?query=${query}`);
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
            website_url: websiteUrl,
            facebook_url: facebookUrl,
            instagram_url: instagramUrl,
            twitter_url: twitterUrl,
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
        const attrs = {
            name: newName,
            description: description,
            website_url: websiteUrl,
            facebook_url: facebookUrl,
            instagram_url: instagramUrl,
            twitter_url: twitterUrl,
        };
        // Remove properties that were not set
        for (let attr in attrs) {
            if (!attrs[attr]) {
                delete attrs[attr];
            }
        }
        return await this._request('PUT', '/clubs/' + name, attrs);
    }

    /**
     * Delete the club with the given name
     * @param {String} name
     */
    async deleteClub(name) {
        return await this._request('DELETE', '/clubs/' + name);
    }

    /**
     * Fetches the memberships for the given club. If a userId is provided only
     * the membership for that user will be returned.
     * @param {String} clubName
     * @param {String} userId (optional, may be undefined)
     */
    async getMemberships(clubName, userId) {
        const params = userId ? { user_id: userId } : undefined;
        return await this._request('GET', `/memberships/${clubName}`,
            undefined, params);
    }

    /**
     * Deletes the memberships for the given club. If a userId is provided only
     * the membership for that user will be deleted.
     * @param {String} clubName
     * @param {String} userId (optional, may be undefined)
     */
    async deleteMemberships(clubName, userId) {
        const params = userId ? { user_id: userId } : undefined;
        return await this._request('DELETE', `/memberships/${clubName}`,
            undefined, params);
    }
}
