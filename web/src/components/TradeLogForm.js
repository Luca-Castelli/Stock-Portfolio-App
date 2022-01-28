import React, { useRef } from "react";
import { UseAuthStore, UseDataStore } from "../utils/store";

function TradeLogForm() {
  const csrfToken = UseAuthStore((state) => state.csrfToken);
  const setIsTradeLogUpdated = UseDataStore(
    (state) => state.setIsTradeLogUpdated
  );

  const dateRef = useRef("");
  const accountRef = useRef("");
  const transactionRef = useRef("");
  const tickerRef = useRef("");
  const quantityRef = useRef("");
  const priceRef = useRef("");
  const commissionRef = useRef("");

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
      if (response.status === 200) {
        console.log("added trade!");
      } else {
        console.log("failed to add trade!");
      }
    } catch (error) {
      console.log(error);
    }
  };

  function handleAddTrade(e) {
    e.preventDefault();
    postTradeLog();
  }

  return (
    <div className="m-8 max-w-4xl">
      <div className=" grid grid-rows-2 grid-cols-7 gap-4 p-4 rounded-lg dark: bg-slate-700 text-slate-600">
        <div className="dark: text-white font-bold">Trade Date</div>
        <div className="dark: text-white font-bold">Account</div>
        <div className="dark: text-white font-bold">Transaction</div>
        <div className="dark: text-white font-bold">Ticker</div>
        <div className="dark: text-white font-bold">Quantity</div>
        <div className="dark: text-white font-bold">Price</div>
        <div className="dark: text-white font-bold">Commission</div>
        <input
          type="date"
          id="date"
          name="date"
          ref={dateRef}
          required
          className="rounded-lg pl-2"
        />
        <select name="account" id="account" ref={accountRef}>
          <option value="Non-Registered">Non-Registered</option>
          <option value="Registered">Registered</option>
        </select>
        <select name="transaction" id="transaction" ref={transactionRef}>
          <option value="Buy">Buy</option>
          <option value="Sell">Sell</option>
        </select>
        <input
          type="text"
          type="ticker"
          id="ticker"
          name="ticker"
          ref={tickerRef}
          required
          placeholder="AAPL"
          className="rounded-lg pl-2"
        />
        <input
          type="text"
          type="quantity"
          id="quantity"
          name="quantity"
          ref={quantityRef}
          placeholder="10"
          className="rounded-lg pl-2"
        />
        <input
          type="text"
          type="price"
          id="price"
          name="price"
          ref={priceRef}
          placeholder="100.00"
          className="rounded-lg pl-2"
        />
        <input
          type="text"
          type="commission"
          id="commission"
          name="commission"
          ref={commissionRef}
          placeholder="9.99"
          className="rounded-lg pl-2"
        />
      </div>
      <button
        onClick={handleAddTrade}
        className="w-24 h-8 p-1 mt-4 rounded-md dark: bg-green-700 hover:bg-green-600 text-white"
      >
        Add Trade
      </button>
    </div>
  );
}

export default TradeLogForm;
