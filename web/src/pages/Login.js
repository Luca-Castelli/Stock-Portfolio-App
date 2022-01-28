import React from "react";
import { Navigate } from "react-router-dom";
import { UseAuthStore } from "../utils/store";
import LoginForm from "../components/LoginForm";
import Navbar from "../components/Navbar";

function Login() {
  const isLoggedIn = UseAuthStore((state) => state.isLoggedIn);

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
