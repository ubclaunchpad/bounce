/* eslint-disable no-undef */
/* eslint-disable no-unused-vars */
import React from 'react';
import ReactDOM from 'react-dom';

import App from './App';
import BounceClient from '../api';
/* eslint-enable no-unused-vars */

it('renders without crashing', () => {
    const div = document.createElement('div');
    const client = new BounceClient('http://localhost:8080');
    ReactDOM.render(<App client={client}/>, div);
    ReactDOM.unmountComponentAtNode(div);
});
