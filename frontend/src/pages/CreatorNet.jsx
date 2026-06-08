import React, { useEffect, useState } from 'react'

export default function CreatorNet() {
  const [websites, setWebsites] = useState([])

  useEffect(() => {
    fetch('/api/websites')
      .then(res => res.json())
      .then(data => setWebsites(data))
  }, [])

  return (
    <div>
      <h1>CreatorNet Dashboard</h1>
      <p>Manage autonomous AI networks</p>
      <div style={{display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: '1rem'}}>
        {websites.map(w => (
          <div key={w.id} className="card">
            <h3>{w.net_name}</h3>
            <p style={{color: '#888'}}>Creator: {w.creator_type} | Provider: {w.api_provider}</p>
          </div>
        ))}
      </div>
    </div>
  )
}
