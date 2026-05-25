import { useEffect, useState } from "react";
import { useAuth } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";

export default function Dashboard() {
  const [data, setData] = useState("");

  const { token, logout } = useAuth();

  const navigate = useNavigate();

  useEffect(() => {
    fetch("http://127.0.0.1:5000/dashboard", {
      method: "GET",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
      .then((res) => res.json())
      .then((data) => {
        setData(data.message);
      });
  }, []);

  const handleLogout = () => {
    logout();

    navigate("/login");
  };

  return (
    <div>
      <h1>Dashboard</h1>

      <p>{data}</p>

      <button onClick={handleLogout}>Logout</button>
    </div>
  );
}