export default function MeetingList({ meetings, refresh }) {
  return (
    <div className="card">
      <div className="header">
        <h2>Upcoming Meets ({meetings.length})</h2>
        <button onClick={refresh}>Refresh</button>
      </div>

      {meetings.length === 0 ? (
        <p>No upcoming meetings.</p>
      ) : (
        <ul>
          {meetings.map((m, i) => (
            <li key={i}>
              <strong>{m.title}</strong><br />
              {new Date(m.start).toLocaleString()}<br />
              <a href={m.meet_link} target="_blank" rel="noopener">{m.meet_link}</a>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}