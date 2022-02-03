import React, { useEffect } from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";

import { useSettingsStore, UseAuthStore } from "./utils/store";

import Login from "./pages/Login";
import Home from "./pages/Home";
import Error from "./pages/Error";
import TestPage from "./pages/TestPage";

function App() {
  const isDarkMode = useSettingsStore((state) => state.isDarkMode);
  const setIsLoggedIn = UseAuthStore((state) => state.setIsLoggedIn);
  const setCsrfToken = UseAuthStore((state) => state.setCsrfToken);

  const getCsrf = async () => {
    try {
      const response = await fetch("/api/auth/getCsrf", {
        method: "GET",
        credentials: "same-origin",
      });
      const data = response.headers.get(["X-CSRFToken"]);
      if (response.status === 200) {
        setCsrfToken(data);
      } else {
        setCsrfToken("");
      }
    } catch (error) {
      console.log(error);
      setCsrfToken("");
    }
  };

  const getSession = async () => {
    try {
      const response = await fetch("/api/auth/getSession", {
        method: "GET",
        credentials: "same-origin",
      });
      const data = await response.json();
      if (response.status === 200) {
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
    getCsrf();
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
        <Route exact path="/test" element={<TestPage />}></Route>
        <Route exact path="*" element={<Error />}></Route>
      </Routes>
    </Router>
  );
}

export default App;
