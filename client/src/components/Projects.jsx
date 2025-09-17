// components/Projects.jsx
import { useEffect, useState } from 'react'
import axios from 'axios'

export default function Projects() {
  const [projects, setProjects] = useState([])

  useEffect(() => {
    const fetchProjects = async () => {
      const token = localStorage.getItem('token')
      const res = await axios.get('http://localhost:5555/projects', {
        headers: { Authorization: `Bearer ${token}` },
      })
      setProjects(res.data)
    }
    fetchProjects()
  }, [])

  return (
    <div>
      <h1>Projects</h1>
      <ul>
        {projects.map((p) => (
          <li key={p.id}>{p.name}</li>
        ))}
      </ul>
    </div>
  )
}
