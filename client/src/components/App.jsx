import { useState } from 'react'
import {Routes, Route} from 'react-router-dom'
import Login from './Login.jsx'
import Register from './Register.jsx'
import Projects from './Projects.jsx'
import ProtectedRoute from './ProtectedRoute.jsx'
import Home from './Home.jsx'
import NavBar from './NavBar.jsx'

import '../assets/css/App.css'

function App() {

  return (
    <>
    <NavBar/>
     <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route 
        path="/projects" 
        element={
          <ProtectedRoute>
              <Projects />
          </ProtectedRoute>
       
         
        } 
      />
    </Routes>
    </>
  )
}

export default App
