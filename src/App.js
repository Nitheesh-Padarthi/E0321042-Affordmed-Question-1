import React, { useState } from 'react';
import './App.css';

function App() {
  const [numberId, setNumberId] = useState('');
  const [response, setResponse] = useState(null);

  const handleSubmit = async (event) => {
    event.preventDefault();

    if (!['p', 'f', 'e', 'r'].includes(numberId)) {
      alert("Invalid number ID. Use 'p', 'f', 'e', or 'r'.");
      return;
    }

    try {
      const res = await fetch(`http://localhost:9876/numbers/${numberId}`);
      const data = await res.json();
      setResponse(data);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Average Calculator</h1>
        <form onSubmit={handleSubmit}>
          <label>
            Number ID:
            <input
              type="text"
              value={numberId}
              onChange={(e) => setNumberId(e.target.value)}
              placeholder="Enter 'p', 'f', 'e', or 'r'"
            />
          </label>
          <button type="submit">Get Numbers</button>
        </form>
        {response && (
          <div>
            <h2>Response</h2>
            <pre>{JSON.stringify(response, null, 2)}</pre>
          </div>
        )}
      </header>
    </div>
  );
}

export default App;
