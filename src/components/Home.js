/* eslint-disable no-unused-vars */
import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import {
    Button, Row, Col
} from 'react-bootstrap';

import Clubs from './Clubs';
import LargeLogo from '../media/large-logo.png';
import '../css/Home.css';
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
                <Row>
                    <Col>
                        <h1>Huddle</h1>
                        <h2>Find a club that matches your interests.</h2>
                        <p>Find a club, get involved, and make new friends!</p>
                    </Col>

                    <Col>
                        <img src={LargeLogo} alt='logo' className='large-logo' />
                    </Col>
                </Row>
                <Link to='/sign-in'>
                    <Button bsStyle='primary'>
                        Explore Clubs
                    </Button>
                </Link>
                <Link to='/create-account'>
                    <Button bsClass='btn btn-secondary'>
                        Create Account
                    </Button>
                </Link>
            </div>
        );
    }
}

export default Home;
