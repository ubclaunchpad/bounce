/* eslint-disable no-unused-vars */
import React, { Component } from 'react';
import '../css/Navbar.css';
import {
    Nav,
    NavItem,
    Button
} from 'react-bootstrap';
/* eslint-enable no-unused-vars */

class NavbarLoggedOut extends Component {
    render() {
        return (
            <Nav pullRight>
                <NavItem eventKey={1} href="#">
                    <Button
                        bsClass='btn btn-secondary'
                        onClick={this.props.handleSignInClick}>
                        Sign In
                    </Button>
                </NavItem>
            </Nav>
        );
    }
}

export default NavbarLoggedOut;