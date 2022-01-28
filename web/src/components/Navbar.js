import React from "react";
import { Navigate } from "react-router-dom";
import { useSettingsStore } from "../utils/store";

function Navbar() {
  const isLoggedIn = useSettingsStore((state) => state.isLoggedIn);
  const setIsLoggedIn = useSettingsStore((state) => state.setIsLoggedIn);

  const handleLogout = async () => {
    try {
      const response = await fetch("/api/auth/logout", {
        method: "GET",
        credentials: "same-origin",
        headers: {
          "content-type": "application/json",
        },
      });
      const data = await response.json();
      if (data.logout && response.status === 200) {
        setIsLoggedIn(false);
      }
    } catch (error) {
      console.log(error);
    }
  };

  function handleLogin() {
    return <Navigate to="/login" />;
  }

  return (
    <nav className="flex items-center p-10">
      <div>
        <h1 className="font-bold text-3xl dark: text-amber-400">Lucaberg</h1>
      </div>
      <div className="absolute right-10">
        {isLoggedIn ? (
          <button
            onClick={handleLogout}
            className="w-24 h-8 p-1 rounded-md dark: bg-red-500 hover:bg-red-600 text-white"
          >
            Logout
          </button>
        ) : (
          <button
            onClick={handleLogin}
            className="w-24 h-8 p-1 rounded-md dark: bg-red-500 hover:bg-red-600 text-white"
          >
            Login
          </button>
        )}
      </div>
    </nav>
  );
}

export default Navbar;
