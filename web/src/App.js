import React, { useEffect } from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";

import { useSettingsStore, UseAuthStore } from "./utils/store";

import Login from "./pages/Login";
import Home from "./pages/Home";
import Error from "./pages/Error";

function App() {
  const isDarkMode = useSettingsStore((state) => state.isDarkMode);
  const setIsLoggedIn = UseAuthStore((state) => state.setIsLoggedIn);
  const setCsrfToken = UseAuthStore((state) => state.setCsrfToken);

  const csrf = async () => {
    try {
      const response = await fetch("/api/auth/csrf", {
        method: "GET",
        credentials: "same-origin",
      });
      const data = response.headers.get(["X-CSRFToken"]);
      setCsrfToken(data);
    } catch (error) {
      console.log(error);
    }
  };

  const getSession = async () => {
    try {
      const response = await fetch("/api/auth/getSession", {
        method: "GET",
        credentials: "same-origin",
      });
      const data = await response.json();
      if (data.login && response.status === 200) {
        setIsLoggedIn(true);
      } else {
        setIsLoggedIn(false);
      }
    } catch (error) {
      console.log(error);
      setIsLoggedIn(false);
    }
  };

  useEffect(() => {
    getSession();
    csrf();
  }, []);

  useEffect(() => {
    if (isDarkMode) {
      document.documentElement.classList.add("dark");
    } else {
      document.documentElement.classList.remove("dark");
    }
  }, [isDarkMode]);

  return (
    <Router>
      <Routes>
        <Route exact path="/" element={<Home />}></Route>
        <Route exact path="/login" element={<Login />}></Route>
        <Route exact path="*" element={<Error />}></Route>
      </Routes>
    </Router>
  );
}

export default App;
