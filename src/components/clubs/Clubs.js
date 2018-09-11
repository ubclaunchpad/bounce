/* eslint-disable no-unused-vars */
import React, { Component } from 'react';
import { Alert, PageHeader } from 'react-bootstrap';
/* eslint-enable no-unused-vars */

class Clubs extends Component {
    constructor(props) {
        super(props);
        this.state = {
            clubs: [],
        };
    }

    /**
     * Fetches clubs to display
     */
    componentDidMount() {
        // TODO
    }

    render() {
        // Display a welcome message if the user just signed up
        let welcomeMsg;
        if (this.props.isNewAccount) {
            welcomeMsg = (
                <Alert bsStyle='primary'>
                    Welcome, {this.props.username}!
                </Alert>
            );
        }

        // Collect clubs to display
        const clubs = this.state.clubs.map(club => {
            return (
                <div>
                    <b>{club.name}</b>
                    <p>{club.description}</p>
                </div>
            );
        });
        return (
            <div>
                {welcomeMsg}
                <PageHeader>Explore Clubs</PageHeader>
                {clubs}
            </div>
        );
    }
}

export default Clubs;
