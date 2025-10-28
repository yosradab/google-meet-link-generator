import { useState, useEffect } from 'react';
import axios from 'axios';
import CreateMeeting from './components/CreateMeeting';
import MeetingList from './components/MeetingList';
import './App.css';

function App() {
  const [meetings, setMeetings] = useState([]);

  const fetchMeetings = async () => {
    try {
      const res = await axios.get('/api/upcoming');
      setMeetings(res.data);
    } catch (err) {
      console.error('Failed to load meetings:', err);
    }
  };

  useEffect(() => {
    fetchMeetings();
  }, []);

  return (
    <div className="app">
      <header>
        <h1>Google Meet Link Generator</h1>
        <p>Create instant Meet links — no UI clicking!</p>
      </header>

      <main>
        <CreateMeeting onCreated={fetchMeetings} />
        <MeetingList meetings={meetings} refresh={fetchMeetings} />
      </main>

      <footer>
        <p>Powered by Google Calendar API</p>
      </footer>
    </div>
  );
}

export default App;