import React, { useEffect, useState } from "react";
import { IoArrowDown, IoArrowUp } from "react-icons/io5";
import { useSortableData } from "../utils/useSortableData";
import TradeLogRow from "./TradeLogRow";
import { UseDataStore } from "../utils/store";

function TradeLog() {
  const isTradeLogUpdated = UseDataStore((state) => state.isTradeLogUpdated);
  const setIsTradeLogUpdated = UseDataStore(
    (state) => state.setIsTradeLogUpdated
  );
  const [tradeLog, setTradeLog] = useState([]);
  const { items, requestSort, sortConfig } = useSortableData(tradeLog);

  const getTradeLog = async () => {
    try {
      const response = await fetch("/api/data/tradeLog", {
        method: "GET",
        credentials: "same-origin",
        headers: {
          "content-type": "application/json",
        },
      });
      const data = await response.json();
      setIsTradeLogUpdated(true);
      if (response.status === 200) {
        setTradeLog(JSON.parse(data));
      } else {
        setTradeLog([]);
      }
    } catch (error) {
      console.log(error);
      setTradeLog([]);
    }
  };

  const getSortArrow = (name) => {
    if (!sortConfig) {
      return null;
    }
    if (sortConfig.key === name && sortConfig.direction === "asc") {
      return <IoArrowUp />;
    } else if (sortConfig.key === name && sortConfig.direction === "desc") {
      return <IoArrowDown />;
    } else {
      return null;
    }
  };

  useEffect(() => {
    getTradeLog();
  }, [isTradeLogUpdated]);

  useEffect(() => {
    requestSort("date");
  }, []);

  return (
    <div className="mx-8 mb-8 max-w-5xl">
      <table className="table-fixed w-full">
        <thead className="text-left dark: bg-slate-700 text-white">
          <tr>
            <th className="pl-2 rounded-l-lg">
              <button
                onClick={() => requestSort("date")}
                className="inline-flex items-center"
              >
                Trade Date
                {getSortArrow("date")}
              </button>
            </th>
            <th className="pl-2">
              <button
                onClick={() => requestSort("account")}
                className="inline-flex items-center"
              >
                Account
                {getSortArrow("account")}
              </button>
            </th>
            <th className="pl-2">
              <button
                onClick={() => requestSort("transaction")}
                className="inline-flex items-center"
              >
                Transaction
                {getSortArrow("transaction")}
              </button>
            </th>
            <th className="pl-2">
              <button
                onClick={() => requestSort("ticker")}
                className="inline-flex items-center"
              >
                Ticker
                {getSortArrow("ticker")}
              </button>
            </th>
            <th className="pl-2">
              <button
                onClick={() => requestSort("quantity")}
                className="inline-flex items-center"
              >
                Quantity
                {getSortArrow("quantity")}
              </button>
            </th>
            <th className="pl-2">
              <button
                onClick={() => requestSort("price")}
                className="inline-flex items-center"
              >
                Price
                {getSortArrow("price")}
              </button>
            </th>
            <th className="pl-2">
              <button
                onClick={() => requestSort("commission")}
                className="inline-flex items-center"
              >
                Commission
                {getSortArrow("commission")}
              </button>
            </th>
            <th className="pl-2 rounded-r-lg w-8"></th>
          </tr>
        </thead>
        <tbody>
          {items.map((item, key) => {
            return <TradeLogRow key={key} item={item} />;
          })}
        </tbody>
      </table>
    </div>
  );
}

export default TradeLog;
