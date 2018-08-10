/* eslint-disable no-unused-vars */
import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import Clubs from './Clubs';
import LargeLogo from '../media/large-logo.png';
/* eslint-enable no-unused-vars */

class Home extends Component {
    constructor(props) {
        super(props);
        this.state = {};
    }

    render() {
        if (this.props.isSignedIn) {
            return <Clubs
                username={this.props.username}
                isNewAccount={this.props.isNewAccount}
            />;
        }
        return (
            <div className='container home'>
                <h1>Huddle: Find a club that matches you</h1>
                <p>
                    Find a club, get involved, and make new friends!
                    Find a club in less time.
                </p>

                <img src={LargeLogo} />
                <br />

                <Link to='/sign-in'>
                    <button className='btn btn-primary'>Explore Clubs</button>
                </Link>
                <Link to='/create-account'>
                    <button className='btn btn-secondary'>Create Account</button>
                </Link>
            </div>
        );
    }
}

export default Home;
