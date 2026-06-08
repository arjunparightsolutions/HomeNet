import React, { useState } from 'react'

export default function Search() {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState([])
  const [summary, setSummary] = useState('')

  const handleSearch = async () => {
    const res = await fetch(`/api/search?q=${encodeURIComponent(query)}`)
    const data = await res.json()
    setResults(data)

    if (query && data.length > 0) {
        const sumRes = await fetch('/api/ai_summarize', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({query, articles: data.slice(0, 3)})
        })
        const sumData = await sumRes.json()
        setSummary(sumData.summary)
    }
  }

  return (
    <div>
      <h1>Search</h1>
      <div style={{display: 'flex', gap: '10px', marginBottom: '20px'}}>
        <input 
          value={query} 
          onChange={e => setQuery(e.target.value)} 
          placeholder="Search articles..." 
          style={{padding: '10px', flex: 1, background: '#222', color: 'white', border: 'none', borderRadius: '4px'}}
        />
        <button onClick={handleSearch} style={{padding: '10px 20px', background: '#3b82f6', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer'}}>Search</button>
      </div>

      {summary && (
          <div className="card" style={{borderLeft: '4px solid #3b82f6'}}>
            <h4>AI Summary</h4>
            <p>{summary}</p>
          </div>
      )}

      <div style={{display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: '1rem'}}>
        {results.map(a => (
          <div key={a.id} className="card">
            <h3>{a.title}</h3>
            <p style={{color: '#888'}}>{a.type} • {a.views} views</p>
          </div>
        ))}
      </div>
    </div>
  )
}
