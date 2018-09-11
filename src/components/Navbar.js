/* eslint-disable no-unused-vars */
import React, { Component } from 'react';
import { NavLink, BrowserRouter, Redirect } from 'react-router-dom';
import {
    Navbar,
    Nav,
    NavItem,
    FormControl,
    FormGroup,
    Button,
    Glyphicon,
    Image
} from 'react-bootstrap';
import SmallLogo from '../media/small-logo.png';
import '../css/Navbar.css';
/* eslint-enable no-unused-vars */

class BounceNavbar extends Component {
    constructor(props) {
        super(props);
        this.state = {
            goToHome: false,
        };

        this.handleHomeClick = this.handleHomeClick.bind(this);
    }

    componentDidUpdate() {
        if (this.state.goToHome) {
            this.setState({ goToHome: false });
        }
    }

    handleHomeClick() {
        this.setState({ goToHome: true });
    }

    render() {
        let homeRedirect;
        if (this.state.goToHome) {
            homeRedirect = <Redirect to='/'></Redirect>;
        }
        return (
            <Navbar id='navbar' toggleNavKey={1} fluid>
                <Navbar.Header>
                    <BrowserRouter>
                        <NavLink to='/' onClick={this.handleHomeClick}>
                            <Navbar.Brand>
                                <Image src={SmallLogo}></Image>
                            </Navbar.Brand>
                        </NavLink>
                    </BrowserRouter>
                    <Navbar.Toggle />
                </Navbar.Header>
                <Navbar.Collapse>
                    <Navbar.Form>
                        <FormGroup>
                            <FormControl type='text' placeholder='Search' />
                        </FormGroup>
                        <Button type='submit'>
                            <Glyphicon glyph='search'></Glyphicon>
                        </Button>
                    </Navbar.Form>
                    {/* <Nav pullRight>
                        <NavItem eventKey={1}>
                            Test
                        </NavItem>
                        <NavItem eventKey={2}>
                            Test2
                        </NavItem>
                    </Nav> */}
                </Navbar.Collapse>
                {homeRedirect}
            </Navbar>
        );
    }
}

export default BounceNavbar;
