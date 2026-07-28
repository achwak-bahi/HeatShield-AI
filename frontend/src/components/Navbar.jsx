import { Link } from "react-router-dom";

function Navbar() {
  const token = localStorage.getItem("access_token");

  return (
    <nav>
      <Link to="/">HeatShield AI</Link>

      <div>
        <Link to="/">Home</Link>
        <Link to="/predict">Prediction</Link>
        <Link to="/methodology">Methodology</Link>

        {token ? (
          <>
            <Link to="/dashboard">Dashboard</Link>
            <Link to="/history">History</Link>
            <button
              onClick={() => {
                localStorage.removeItem("access_token");
                window.location.href = "/login";
              }}
            >
              Logout
            </button>
          </>
        ) : (
          <>
            <Link to="/login">Login</Link>
            <Link to="/register">Register</Link>
          </>
        )}
      </div>
    </nav>
  );
}

export default Navbar;