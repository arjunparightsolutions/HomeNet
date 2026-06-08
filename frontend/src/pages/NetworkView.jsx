import React, { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'

export default function NetworkView() {
  const { net } = useParams()
  const [articles, setArticles] = useState([])

  useEffect(() => {
    fetch('/api/articles')
      .then(res => res.json())
      .then(data => setArticles(data.filter(a => a.type === net).reverse()))
  }, [net])

  return (
    <div>
      <h1 style={{textTransform: 'capitalize'}}>{net}</h1>
      <div style={{display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: '1rem'}}>
        {articles.map(a => (
          <div key={a.id} className="card">
            <h3>{a.title}</h3>
            <p style={{color: '#888'}}>{a.views} views</p>
            <div dangerouslySetInnerHTML={{__html: a.body.substring(0, 200) + '...'}} />
          </div>
        ))}
      </div>
    </div>
  )
}
