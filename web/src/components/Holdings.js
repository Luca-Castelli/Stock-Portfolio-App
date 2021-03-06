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
                onClick={() => requestSort("post_qty")}
                className="inline-flex text-left"
              >
                Quantity
                {getSortArrow("post_qty")}
              </button>
            </th>
            <th className="pl-2">
              <button
                onClick={() => requestSort("src_post_acb_ps")}
                className="inline-flex text-left"
              >
                Cost Base
                {getSortArrow("src_post_acb_ps")}
              </button>
            </th>
            <th className="pl-2">
              <button
                onClick={() => requestSort("price")}
                className="inline-flex text-left"
              >
                Last Price
                {getSortArrow("price")}
              </button>
            </th>
            <th className="pl-2">
              <button
                onClick={() => requestSort("src_post_acb")}
                className="inline-flex text-left"
              >
                Book Value
                {getSortArrow("src_post_acb")}
              </button>
            </th>
            <th className="pl-2">
              <button
                onClick={() => requestSort("src_market_value")}
                className="inline-flex text-left"
              >
                Market Value
                {getSortArrow("src_market_value")}
              </button>
            </th>
            <th className="pl-2">
              <button
                onClick={() => requestSort("cad_unrealized_gain")}
                className="inline-flex text-left"
              >
                Unrealized PnL
                {getSortArrow("cad_unrealized_gain")}
              </button>
            </th>
            <th className="pl-2">
              <button
                onClick={() => requestSort("cad_unrealized_gain_percent")}
                className="inline-flex text-left"
              >
                Unrealized PnL %{getSortArrow("cad_unrealized_gain_percent")}
              </button>
            </th>
            <th className="pl-2">
              <button
                onClick={() => requestSort("cad_realized_gain_dividend")}
                className="inline-flex text-left"
              >
                Dividends
                {getSortArrow("cad_realized_gain_dividend")}
              </button>
            </th>
            <th className="pl-2">
              <button
                onClick={() => requestSort("cad_realized_gain_sell")}
                className="inline-flex text-left"
              >
                Realized PnL
                {getSortArrow("cad_realized_gain_sell")}
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
