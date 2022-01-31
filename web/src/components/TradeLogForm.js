import React from "react";
import { UseAuthStore, UseDataStore } from "../utils/store";
import { useForm } from "../utils/useForm";
import ErrorMessage from "./ErrorMessage";

function TradeLogForm() {
  const csrfToken = UseAuthStore((state) => state.csrfToken);

  const setIsTradeLogUpdated = UseDataStore(
    (state) => state.setIsTradeLogUpdated
  );
  const setErrorMessage = UseDataStore((state) => state.setErrorMessage);

  const { handleSubmit, handleChange, formData, errors } = useForm({
    validations: {
      quantity: {
        pattern: {
          value: "^[0-9]*[1-9][0-9]*$",
          message: "Quantity needs to be a positive integer.",
        },
      },
      price: {
        pattern: {
          value: "^(\\d*\\.)?\\d+$",
          message: "Price needs to be a positive decimal.",
        },
      },
      commission: {
        pattern: {
          value: "^(\\d*\\.)?\\d+$",
          message: "Commission needs to be a positive decimal.",
        },
      },
    },
    onSubmit: () => {
      tradeLogInsert();
    },
    initialValues: {
      date: new Date().toISOString().split("T")[0],
      account: "Registered",
      transaction: "Buy",
    },
  });

  const tradeLogInsert = async () => {
    try {
      const payload = {
        date: formData.date,
        account: formData.account,
        transaction: formData.transaction,
        ticker: formData.ticker,
        quantity: formData.quantity,
        price: formData.price,
        commission: formData.commission,
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
        setErrorMessage({ isError: true, msg: "Server error: " + data });
      }
    } catch (error) {
      console.log(error);
      setErrorMessage({
        isError: true,
        msg: "Server error: Failed to reach server.",
      });
    }
  };

  console.log(formData);
  console.log(errors);

  return (
    <div className="mt-8 ml-8 mr-[68px] max-w-5xl">
      <h1 className="mb-2 font-bold dark: text-amber-400">Trade Log</h1>
      <div className="flex items-center">
        <button
          onClick={handleSubmit}
          className="w-24 h-8 p-1 mt-4 rounded-md dark: bg-green-700 hover:bg-green-600 text-white"
        >
          Add Trade
        </button>
        <ErrorMessage />
      </div>
      <form className="grid grid-rows-1 grid-cols-7 gap-4 py-4 rounded-lg text-sm dark: bg-black text-slate-600">
        <input
          type="date"
          value={formData.date || ""}
          onChange={handleChange("date")}
          className="rounded-lg pl-2"
          required
        />
        <select onChange={handleChange("account")} className="rounded-lg pl-2">
          <option value="Registered">Registered</option>
          <option value="Non-Registered">Non-Registered</option>
        </select>
        <select
          onChange={handleChange("transaction")}
          className="rounded-lg pl-2"
        >
          <option value="Buy">Buy</option>
          <option value="Sell">Sell</option>
        </select>
        <input
          type="text"
          value={formData.ticker || ""}
          onChange={handleChange("ticker")}
          placeholder="AAPL"
          className="rounded-lg pl-2"
          required
        />
        <input
          type="text"
          value={formData.quantity || ""}
          onChange={handleChange("quantity")}
          placeholder="100"
          className="rounded-lg pl-2"
          required
        />
        <input
          type="text"
          value={formData.price || ""}
          onChange={handleChange("price")}
          placeholder="25.55"
          className="rounded-lg pl-2"
          required
        />
        <input
          type="text"
          value={formData.commission || ""}
          onChange={handleChange("commission")}
          placeholder="9.99"
          className="rounded-lg pl-2"
          required
        />
      </form>
    </div>
  );
}

export default TradeLogForm;
