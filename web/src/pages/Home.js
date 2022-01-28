import React from "react";
import { Navigate } from "react-router-dom";
import { useSettingsStore } from "../utils/store";

import Navbar from "../components/Navbar";
import TradeLogForm from "../components/TradeLogForm";
import TradeLog from "../components/TradeLog";

function Home() {
  const isLoggedIn = useSettingsStore((state) => state.isLoggedIn);

  if (!isLoggedIn) {
    return <Navigate to="/login" />;
  }

  return (
    <main className="h-screen dark:bg-black">
      <Navbar />
      <TradeLogForm />
      <TradeLog />
    </main>
  );
}

export default Home;
