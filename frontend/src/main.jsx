import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import LoginPage from "./pages/login/page";
import "./styles/login.css";

import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <Router>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
      </Routes>
    </Router>
  </StrictMode>
);
