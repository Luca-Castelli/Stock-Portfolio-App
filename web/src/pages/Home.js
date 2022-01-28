import React from "react";
import { Navigate } from "react-router-dom";
import { UseAuthStore } from "../utils/store";

import Navbar from "../components/Navbar";
import Holdings from "../components/Holdings";
import TradeLogForm from "../components/TradeLogForm";
import TradeLog from "../components/TradeLog";

function Home() {
  const isLoggedIn = UseAuthStore((state) => state.isLoggedIn);

  if (!isLoggedIn) {
    return <Navigate to="/login" />;
  }

  return (
    <main className="h-screen dark:bg-black">
      <Navbar />
      <Holdings />
      <TradeLogForm />
      <TradeLog />
    </main>
  );
}

export default Home;
