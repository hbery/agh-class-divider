import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [message, setMessage] = useState();

  useEffect(() => {
    fetch('http://localhost:8000/')
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => setMessage(data.Hello))
      .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
      });
  }, []);


  return (
    <div className="App">
      <header className="App-header">
        {message ? message : 'Ładowanie...'}
      </header>
    </div>
  );
}

export default App;

