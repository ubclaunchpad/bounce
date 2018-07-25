/* eslint-disable no-unused-vars */
import React, { Component } from 'react';
import './sign-in-page.css';
// import { template } from 'handlebars';
/* eslint-enable no-unused-vars */

class SignInPage extends Component {
    constructor(props) {
        super(props);
        this.state = {
            userNameEmail: ""
        };

        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleInputChange = this.handleInputChange.bind(this);
    }

    handleSubmit(event) {
        event.preventDefault();
        console.log('here');
    }

    handleInputChange(event) {
        const target = event.target;
        const name = target.name;
        const value = target.value;

        this.setState({
            [name]: value
        });
    }

    render() {
        return (
            <div className="UserSignIn">
                <form onSubmit={this.handleSubmit}>
                    <h1 className="signinComponent">Sign In</h1>

                    <input type="text" name="userName" 
                        placeholder="Username or Email"
                        className="signinComponent"
                        id="userName"
                        value={this.state.userName}
                        onChange={this.handleInputChange} />

                    <input type="password" name="userPassword"
                        placeholder="Password"
                        className="signinComponent"
                        id="userPassword"
                        value={this.state.userPassword}
                        onChange={this.handleInputChange} />

                    <button>Sign In</button>
                </form>

                <div className="signinComponent optionBreak">
                    <span>or</span>
                    <div className="lineBreak"></div>
                </div>

                <div className="signinComponent signinOption">
                    <span>FACEBOOK</span>
                </div>

                <div className="signinComponent signinOption">
                    <span>GOOGLE</span>
                </div>

            </div>
        );
    }
}

export default SignInPage;
