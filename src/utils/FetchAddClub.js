const URL = 'http://localhost:8080/clubs';

const fetchAddClub = addClubInfo => (
    fetch(URL, {
        method: 'post',
        mode: 'no-cors',
        headers: {
            'Content-Type': 'application/json; charset=UTF-8',
        },
        body: JSON.stringify(addClubInfo)
    })
    // .then(json)
        .then(function (data){
            console.log('Request succeeded with JSON response', data);
        })
        .catch (function (error) {
            console.log('Request failed', error);
        })
);

export default fetchAddClub;