/* eslint-disable no-unused-vars */
import React from 'react';
import 'whatwg-fetch';
/* eslint-enable no-unused-vars */

export default class BounceClub {
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
     * Creates a new Bounce user and returns information about the user
     * @param {String} clubName The name of club
     * @param {String} tags The description tag of club
     * @param {String} about The description of the club
     * @param {String} meetingLocation The meeting location of club
     * @param {String} meetingTime The club's meeting time
     * @param {String} website The club's own website
     * @param {String} events The club's events
     */
    async createClub(clubName, tags, about, meetingLocation, meetingTime, website, events) {
        return await this._request('POST', '/clubs', {
            club_name: clubName,
            tags: tags,
            about: about,
            meeting_location: meetingLocation,
            meeting_time: meetingTime,
            website: website,
            events: events,
        });
    }
}