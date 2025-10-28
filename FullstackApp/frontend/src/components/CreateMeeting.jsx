import { useState } from 'react';
import axios from 'axios';

export default function CreateMeeting({ onCreated }) {
  const [title, setTitle] = useState('Team Sync');
  const [minutes, setMinutes] = useState(5);
  const [duration, setDuration] = useState(30);
  const [attendees, setAttendees] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResult(null);

    const attendeeList = attendees.split(',').map(e => e.trim()).filter(Boolean);

    try {
      const res = await axios.post('/api/create', {
        title,
        start_in_minutes: Number(minutes),
        duration: Number(duration),
        attendees: attendeeList
      });
      setResult(res.data);
      onCreated();
    } catch (err) {
      alert('Error: ' + (err.response?.data?.detail || err.message));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card">
      <h2>Create New Meet</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Meeting title"
          value={title}
          onChange={e => setTitle(e.target.value)}
          required
        />
        <div className="row">
          <input
            type="number"
            placeholder="Start in minutes"
            value={minutes}
            onChange={e => setMinutes(e.target.value)}
            min="1"
          />
          <input
            type="number"
            placeholder="Duration (min)"
            value={duration}
            onChange={e => setDuration(e.target.value)}
            min="5"
          />
        </div>
        <textarea
          placeholder="Attendees (comma-separated emails)"
          value={attendees}
          onChange={e => setAttendees(e.target.value)}
          rows="2"
        />
        <button type="submit" disabled={loading}>
          {loading ? 'Creating…' : 'Create Meet Link'}
        </button>
      </form>

      {result && (
        <div className="result">
          <h3>Meeting Created!</h3>
          <p><strong>{result.title}</strong></p>
          <p>Starts: {new Date(result.start).toLocaleString()}</p>
          <div className="link">
            <a href={result.meet_link} target="_blank" rel="noopener">{result.meet_link}</a>
            <button onClick={() => navigator.clipboard.writeText(result.meet_link)}>
              Copy
            </button>
          </div>
          <a href={result.html_link} target="_blank" rel="noopener">Open in Calendar</a>
        </div>
      )}
    </div>
  );
}