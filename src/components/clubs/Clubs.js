/* eslint-disable no-unused-vars */
import React, { Component } from 'react';
import { Alert, PageHeader } from 'react-bootstrap';

import { UNEXPECTED_ERROR, NO_CLUBS_FOUND } from '../../constants';
import Cards from '../util/Cards';
/* eslint-enable no-unused-vars */

class Clubs extends Component {
    constructor(props) {
        super(props);
        this.state = {
            clubs: [],
            searchQuery: props.searchQuery,
            errorMsg: undefined,
        };

        this.search = this.search.bind(this);
    }

    /**
     * Updates component state when new props are received from the parent.
     * @param {Object} props
     */
    componentWillReceiveProps(props) {
        this.setState({ searchQuery: props.searchQuery });
        this.search();
    }

    /**
     * Searches for clubs that match the current query and updates the
     * component state with the results.
     */
    search() {
        // Do nothing if there is no query
        if (!this.state.searchQuery) return;

        this.props.client.searchClubs(this.state.searchQuery)
            .then(result => {
                if (result.ok) {
                    // Display results
                    result.json().then(body => {
                        this.setState({ clubs: body, errorMsg: undefined });
                    });
                } else if (result.status === 404) {
                    this.setState({ errorMsg: NO_CLUBS_FOUND });
                } else {
                    this.setState({ errorMsg: UNEXPECTED_ERROR });
                }
            }).catch(() => {
                this.setState({ errorMsg: UNEXPECTED_ERROR });
            });
    }

    render() {
        return (
            <div className='container'>
                {this.props.isNewAccount &&
                    <Alert bsStyle='success'>
                        Welcome, {this.props.client.getUsername()}!
                    </Alert>
                }
                {this.state.errorMsg &&
                    <Alert bsStyle='warning'> {this.state.errorMsg} </Alert>
                }
                <PageHeader>Explore Clubs</PageHeader>
                <Cards items={this.state.clubs} />
            </div>
        );
    }
}

export default Clubs;
