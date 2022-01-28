import React from "react";
import { Navigate } from "react-router-dom";
import { useSettingsStore } from "../utils/store";
import LoginForm from "../components/LoginForm";
import Navbar from "../components/Navbar";

function Login() {
  const isLoggedIn = useSettingsStore((state) => state.isLoggedIn);

  if (isLoggedIn) {
    return <Navigate to="/" />;
  }

  return (
    <main className="h-screen">
      <Navbar />
      <LoginForm />
    </main>
  );
}

export default Login;
