import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'

export default function Home() {
  const [articles, setArticles] = useState([])
  
  useEffect(() => {
    fetch('/api/articles')
      .then(res => res.json())
      .then(data => setArticles(data.slice(-10).reverse()))
  }, [])

  return (
    <div>
      <h1>HomeNet Network</h1>
      <p>Welcome to the React-powered UI!</p>
      <div style={{display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: '1rem'}}>
        {articles.map(a => (
          <div key={a.id} className="card">
            <h3>{a.title}</h3>
            <p style={{color: '#888'}}>{a.type} • {a.views} views</p>
          </div>
        ))}
      </div>
    </div>
  )
}
