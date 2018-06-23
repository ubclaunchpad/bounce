import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import './App.css';
<<<<<<< HEAD
import BounceClient from './Client';
=======
import { template } from 'handlebars';
import fetchAddClub from './utils/FetchAddClub';
>>>>>>> Add Club Fields to FetchAddClub

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      clubName: '',
      tags: '',
      about: '',
      meetingLocation: '',
      meetingTimes: '',
      website: '',
      events: '',
    };

<<<<<<< HEAD
        this.client = new BounceClient(this.props.url);

        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleInputChange = this.handleInputChange.bind(this);
    }
=======
    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleInputChange = this.handleInputChange.bind(this);
  }
>>>>>>> Add Club Fields to FetchAddClub

  handleSubmit(event) {
    event.preventDefault();
    fetchAddClub(this.state);
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
      <div className="App">
        <form onSubmit={this.handleSubmit} className="Form">
          <h1>Add Club</h1>
          <input type="text" name="clubName" placeholder="Club Name" className="Form-Input"
          value={this.state.clubName}
          onChange={this.handleInputChange}/>
          <button className="Form-Button Form-Buttom-Picture">Add pictures</button>
          <input type="text" name="tags" placeholder="Tags" className="Form-Input" />
          <textarea rows="4" cols="50" name="about" placeholder="About"
          className="Form-Input Form-Input-About"
          value={this.state.about} onChange={this.handleInputChange}></textarea>
          <div className="Social-Media">
            <span>Social media:</span>
            <div className="Social-Media-Type">
              <p>Fb</p>
              <button className="Form-Button">+</button>
            </div>
            <div className="Social-Media-Type">
              <p>Ins</p>
              <button className="Form-Button">+</button>
            </div>
            <div className="Social-Media-Type">
              <p>Twitter</p>
              <button className="Form-Button">+</button>
            </div>
          </div>
          <input type="text" name="meetingLocation" placeholder="Meeting location" className="Form-Input"/>
          <input type="text" name="meetingTimes" placeholder="Meeting times" className="Form-Input"/>
          <input type="text" name="website" placeholder="website URL" className="Form-Input"/>
          <input type="text" name="events" placeholder="Events" className="Form-Input"/>
          <button>
            submit
          </button>
        </form>
      </div>
    );
  }
}

export default App;
