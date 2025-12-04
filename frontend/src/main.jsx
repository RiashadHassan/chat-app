import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import LoginPage from "./pages/login/LoginPage";
import HomePage from "./pages/home/HomePage";
import ServersPage from "./components/sidebar/ServerSidebar";

import "./styles/login.css";
import "./styles/home.css"

import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <Router>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/me" element={<HomePage />} />
        <Route path="/servers" element={<ServersPage />} />

      </Routes>
    </Router>
  </StrictMode>
);
