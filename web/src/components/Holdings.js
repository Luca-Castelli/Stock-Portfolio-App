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
      <h1 className="mb-2 font-bold dark: text-amber-400">Holdings</h1>
      <table className="table-fixed w-full">
        <thead className="text-left dark: bg-slate-700 text-white">
          <tr>
            <th className="pl-2 rounded-l-lg">
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
                onClick={() => requestSort("symbol")}
                className="inline-flex items-center"
              >
                Ticker
                {getSortArrow("symbol")}
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
                onClick={() => requestSort("average_cost_basis_ps")}
                className="inline-flex items-center"
              >
                Buy Price
                {getSortArrow("average_cost_basis_ps")}
              </button>
            </th>
            <th className="pl-2">
              <button
                onClick={() => requestSort("live_price")}
                className="inline-flex items-center"
              >
                Live Price
                {getSortArrow("live_price")}
              </button>
            </th>
            <th className="pl-2">
              <button
                onClick={() => requestSort("average_cost_basis")}
                className="inline-flex items-center"
              >
                Book Value
                {getSortArrow("average_cost_basis")}
              </button>
            </th>
            <th className="pl-2">
              <button
                onClick={() => requestSort("market_value")}
                className="inline-flex items-center"
              >
                Market Value
                {getSortArrow("market_value")}
              </button>
            </th>
            <th className="pl-2">
              <button
                onClick={() => requestSort("realized_gain")}
                className="inline-flex items-center"
              >
                Realized Gain
                {getSortArrow("realized_gain")}
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
