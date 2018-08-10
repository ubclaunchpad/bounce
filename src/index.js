/* eslint-disable no-unused-vars */
import 'bootstrap/dist/css/bootstrap.min.css';
import React from 'react';
import ReactDOM from 'react-dom';
import App from './components/App';
import BounceClient from './api';
/* eslint-enable no-unused-vars */

const client = new BounceClient('http://localhost:8080');
ReactDOM.render(<App client={client}/>, document.getElementById('root'));
