import React from "react";
import { IoMdRemoveCircle } from "react-icons/io";
import { UseAuthStore, UseDataStore } from "../utils/store";
import { NumberDisplay } from "../utils/NumberDisplay";

function TradeLogRow({ item }) {
  const csrfToken = UseAuthStore((state) => state.csrfToken);
  const setIsTradeLogUpdated = UseDataStore(
    (state) => state.setIsTradeLogUpdated
  );
  const setErrorMessage = UseDataStore((state) => state.setErrorMessage);

  const {
    id,
    date,
    account,
    transaction,
    symbol,
    quantity,
    price,
    commission,
  } = item;

  const removeTradeLog = async () => {
    try {
      const payload = {
        trade_id: id,
      };
      const response = await fetch("/api/client_data/tradeLogRemove", {
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
  };

  function handleRemoveTrade(e) {
    e.preventDefault();
    removeTradeLog();
  }

  return (
    <tr className="border-y text-sm dark: border-slate-700 text-white">
      <td className="pl-2">{date}</td>
      <td className="pl-2">{account}</td>
      <td className="pl-2">{transaction}</td>
      <td className="pl-2">{symbol}</td>
      <td className="pl-2">{NumberDisplay(quantity, 0)}</td>
      <td className="pl-2">{NumberDisplay(price, 2)}</td>
      <td className="pl-2">{NumberDisplay(commission, 2)}</td>
      <td>
        <button onClick={handleRemoveTrade} className="align-middle">
          <IoMdRemoveCircle style={{ color: "red" }} />
        </button>
      </td>
    </tr>
  );
}

export default TradeLogRow;
