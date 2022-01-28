import React, { useRef } from "react";
import { UseAuthStore, UseDataStore } from "../utils/store";
import ErrorMessage from "./ErrorMessage";

function TradeLogForm() {
  const csrfToken = UseAuthStore((state) => state.csrfToken);
  const setIsTradeLogUpdated = UseDataStore(
    (state) => state.setIsTradeLogUpdated
  );
  const setErrorMessage = UseDataStore((state) => state.setErrorMessage);

  const dateRef = useRef("");
  const accountRef = useRef("");
  const transactionRef = useRef("");
  const tickerRef = useRef("");
  const quantityRef = useRef("");
  const priceRef = useRef("");
  const commissionRef = useRef("");

  // function validateInput() {
  //   if (dateRef.current.value === "") {
  //     setError({ isError: true, msg: "Date can't be empty." });
  //     return null;
  //   }
  //   if (tickerRef.current.value === "") {
  //     setError({ isError: true, msg: "Ticker can't be empty." });
  //     return null;
  //   }
  //   if (quantityRef.current.value === "") {
  //     setError({ isError: true, msg: "Quantity can't be empty." });
  //     return null;
  //   }
  //   if (priceRef.current.value === "") {
  //     setError({ isError: true, msg: "Price can't be empty." });
  //     return null;
  //   }
  //   if (commissionRef.current.value === "") {
  //     commissionRef.current.value = 0;
  //   }
  // }

  const postTradeLog = async () => {
    try {
      const payload = {
        date: dateRef.current.value,
        account: accountRef.current.value,
        transaction: transactionRef.current.value,
        ticker: tickerRef.current.value.toUpperCase(),
        quantity: quantityRef.current.value,
        price: priceRef.current.value,
        commission: commissionRef.current.value,
      };
      const response = await fetch("/api/data/tradeLogInsert", {
        method: "POST",
        credentials: "same-origin",
        headers: {
          "content-type": "application/json",
          "X-CSRFToken": csrfToken,
        },
        body: JSON.stringify(payload),
      });
      const data = await response.json();
      setIsTradeLogUpdated(false);
      if (response.status !== 200) {
        setErrorMessage({ isError: true, msg: data });
      }
    } catch (error) {
      console.log(error);
      setErrorMessage({ isError: true, msg: "Error reaching server." });
    }
    clearInputs();
  };

  function clearInputs() {
    dateRef.current.value = "";
    accountRef.current.value = "";
    transactionRef.current.value = "";
    tickerRef.current.value = "";
    quantityRef.current.value = "";
    priceRef.current.value = "";
    commissionRef.current.value = "";
  }

  function handleAddTrade(e) {
    e.preventDefault();
    postTradeLog();
  }

  return (
    <div className="mx-8 mt-8 max-w-5xl">
      <h1 className="mb-2 font-bold dark: text-amber-400">Trade Log</h1>
      <div className="flex items-center">
        <button
          onClick={handleAddTrade}
          className="w-24 h-8 p-1 mt-4 rounded-md dark: bg-green-700 hover:bg-green-600 text-white"
        >
          Add Trade
        </button>
        <ErrorMessage />
      </div>
      <div className="grid grid-rows-1 grid-cols-7 gap-4 py-4 rounded-lg text-sm dark: bg-black text-slate-600">
        <input
          type="date"
          id="date"
          name="date"
          ref={dateRef}
          className="rounded-lg pl-2"
        />
        <select
          id="account"
          name="account"
          ref={accountRef}
          className="rounded-lg pl-2"
        >
          <option value="Registered">Registered</option>
          <option value="Non-Registered">Non-Registered</option>
        </select>
        <select
          id="transaction"
          name="transaction"
          ref={transactionRef}
          className="rounded-lg pl-2"
        >
          <option value="Buy">Buy</option>
          <option value="Sell">Sell</option>
        </select>
        <input
          type="text"
          id="ticker"
          name="ticker"
          ref={tickerRef}
          placeholder="AAPL"
          className="rounded-lg pl-2"
        />
        <input
          type="text"
          id="quantity"
          name="quantity"
          ref={quantityRef}
          placeholder="10"
          className="rounded-lg pl-2"
        />
        <input
          type="text"
          id="price"
          name="price"
          ref={priceRef}
          placeholder="100.00"
          className="rounded-lg pl-2"
        />
        <input
          type="text"
          id="commission"
          name="commission"
          ref={commissionRef}
          placeholder="9.99"
          className="rounded-lg pl-2"
        />
      </div>
    </div>
  );
}

export default TradeLogForm;
