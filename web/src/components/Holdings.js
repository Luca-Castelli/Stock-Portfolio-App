import React, { useEffect, useState } from "react";
import { IoArrowDown, IoArrowUp } from "react-icons/io5";
import { useSortableData } from "../utils/useSortableData";
import HoldingsRow from "./HoldingsRow";
import { UseDataStore } from "../utils/store";

function Holdings() {
  const isTradeLogUpdated = UseDataStore((state) => state.isTradeLogUpdated);
  const [holdings, setHoldings] = useState([]);
  const { items, requestSort, sortConfig } = useSortableData(holdings);

  const getHoldings = async () => {
    try {
      const response = await fetch("/api/client_data/holdings", {
        method: "GET",
        credentials: "same-origin",
        headers: {
          "content-type": "application/json",
        },
      });
      const data = await response.json();
      if (response.status === 200) {
        setHoldings(data);
      } else {
        setHoldings([]);
      }
    } catch (error) {
      console.log(error);
      setHoldings([]);
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
    getHoldings();
  }, [isTradeLogUpdated]);

  useEffect(() => {
    requestSort("account");
  }, []);

  return (
    <div className="m-8 max-w-5xl">
      <div className="flex items-center">
        <h1 className="mb-2 font-bold dark: text-amber-400">Holdings</h1>
      </div>

      <table className="w-full">
        <thead className="text-sm dark: bg-slate-700 text-white">
          <tr>
            <th className="pl-2 rounded-l-lg">
              <button
                onClick={() => requestSort("account")}
                className="inline-flex text-left"
              >
                Account
                {getSortArrow("account")}
              </button>
            </th>
            <th className="pl-2">
              <button
                onClick={() => requestSort("symbol")}
                className="inline-flex text-left"
              >
                Ticker
                {getSortArrow("symbol")}
              </button>
            </th>
            <th className="pl-2">
              <button
                onClick={() => requestSort("weight")}
                className="inline-flex text-left"
              >
                Weight
                {getSortArrow("weight")}
              </button>
            </th>
            <th className="pl-2">
              <button
                onClick={() => requestSort("quantity")}
                className="inline-flex text-left"
              >
                Quantity
                {getSortArrow("quantity")}
              </button>
            </th>
            <th className="pl-2">
              <button
                onClick={() => requestSort("average_cost_basis_ps")}
                className="inline-flex text-left"
              >
                Cost Base
                {getSortArrow("average_cost_basis_ps")}
              </button>
            </th>
            <th className="pl-2">
              <button
                onClick={() => requestSort("latest_price")}
                className="inline-flex text-left"
              >
                Last Price
                {getSortArrow("latest_price")}
              </button>
            </th>
            <th className="pl-2">
              <button
                onClick={() => requestSort("average_cost_basis")}
                className="inline-flex text-left"
              >
                Book Value
                {getSortArrow("average_cost_basis")}
              </button>
            </th>
            <th className="pl-2">
              <button
                onClick={() => requestSort("market_value")}
                className="inline-flex text-left"
              >
                Market Value
                {getSortArrow("market_value")}
              </button>
            </th>
            <th className="pl-2">
              <button
                onClick={() => requestSort("unrealized_pnl")}
                className="inline-flex text-left"
              >
                Unrealized PnL
                {getSortArrow("unrealized_pnl")}
              </button>
            </th>
            <th className="pl-2">
              <button
                onClick={() => requestSort("unrealized_pnl_percent")}
                className="inline-flex text-left"
              >
                Unrealized PnL %{getSortArrow("unrealized_pnl_percent")}
              </button>
            </th>
            <th className="pl-2">
              <button
                onClick={() => requestSort("dividends")}
                className="inline-flex text-left"
              >
                Dividends
                {getSortArrow("dividends")}
              </button>
            </th>
            <th className="pl-2 rounded-r-lg">
              <button
                onClick={() => requestSort("realized_pnl")}
                className="inline-flex text-left"
              >
                Realized PnL
                {getSortArrow("realized_pnl")}
              </button>
            </th>
          </tr>
        </thead>
        <tbody>
          {items.map((item, key) => {
            return <HoldingsRow key={key} item={item} />;
          })}
        </tbody>
      </table>
    </div>
  );
}

export default Holdings;
