import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import LoginPage from './pages/login/page'
import "./styles/login.css"

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <LoginPage />
  </StrictMode>,
)
