import React from 'react'
import { Routes, Route, Link } from 'react-router-dom'
import Home from './pages/Home'
import Search from './pages/Search'
import NetworkView from './pages/NetworkView'
import CreatorNet from './pages/CreatorNet'

function App() {
  return (
    <div>
      <nav style={{padding: '1rem', background: '#111', display: 'flex', gap: '1rem'}}>
        <Link to="/" style={{color: 'white', textDecoration: 'none'}}>Home</Link>
        <Link to="/search" style={{color: 'white', textDecoration: 'none'}}>Search</Link>
        <Link to="/creatornet" style={{color: 'white', textDecoration: 'none'}}>CreatorNet</Link>
      </nav>
      <div style={{padding: '2rem'}}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/search" element={<Search />} />
          <Route path="/creatornet" element={<CreatorNet />} />
          <Route path="/:net" element={<NetworkView />} />
        </Routes>
      </div>
    </div>
  )
}

export default App
