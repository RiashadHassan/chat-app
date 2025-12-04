import { useState } from "react";
import { useNavigate } from "react-router-dom";

const LoginBackdrop = () => {
  return <div className="login-bg-image"></div>;
};

const LoginPortal = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    console.log("LOGGING IN...");
    const url = "http://localhost/api/token/";
    try {
      const response = await fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email, password }),
      });

      const data = await response.json();
      console.log(response);
      if (response.ok) {
        localStorage.setItem("access_token", data.access);
        localStorage.setItem("refresh_token", data.refresh);
        navigate("/me");
      } else {
        alert("Login Failed!");
      }
    } catch (error) {
      alert("REDDD");
    }
  };

  return (
    <div className="login-portal-container">
      <section className="portal-header-section">
        <h1>Welcome back!</h1>
        <p>We're so excited to see you again!</p>
      </section>

      <form className="input-container" onSubmit={handleLogin}>
        <div className="input-block">
          <h3>
            Email <span>*</span>
          </h3>
          <div className="input-box">
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
        </div>

        <div className="input-block">
          <h3>
            Password <span>*</span>
          </h3>
          <div className="input-box">
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          <a href="#" target=" " className="forgot-password">
            Forgot your password?
          </a>
        </div>

        <div className="input-block">
          <button type="submit" className="input-box login-btn">
            Log In
          </button>
        </div>
      </form>
      <div className="register-section">
        <p>Need an account?</p>
        <a href="#" target=" ">
          Register
        </a>
      </div>
    </div>
  );
};

const LoginPage = () => {
  return (
    <div className="login-page">
      <LoginBackdrop />
      <LoginPortal />
    </div>
  );
};

export default LoginPage;
