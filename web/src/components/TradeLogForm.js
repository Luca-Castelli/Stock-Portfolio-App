import React, { useEffect, useState } from "react";
import { UseAuthStore, UseDataStore } from "../utils/store";
import { useForm } from "../utils/useForm";
import ErrorMessage from "./ErrorMessage";
import AutoCompleteTicker from "./AutoCompleteTicker";

function TradeLogForm() {
  const csrfToken = UseAuthStore((state) => state.csrfToken);

  const setIsTradeLogUpdated = UseDataStore(
    (state) => state.setIsTradeLogUpdated
  );

  const setErrorMessage = UseDataStore((state) => state.setErrorMessage);

  const [autoCompleteField, setAutoCompleteField] = useState("");

  const [symbols, setSymbols] = useState([]);

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
      clearForm();
    },
    initialValues: {
      date: new Date().toISOString().split("T")[0],
      account: "Registered",
      transaction: "Buy",
      quantity: "",
      price: "",
      commission: "",
    },
  });

  function validateAutoCompleteField() {
    if (autoCompleteField) {
      return true;
    } else {
      setErrorMessage({
        isError: true,
        msg: "Front-end error: Failed to validate symbol.",
      });
      return false;
    }
  }

  const tradeLogInsert = async () => {
    if (validateAutoCompleteField()) {
      try {
        const payload = {
          date: formData.date,
          account: formData.account,
          transaction: formData.transaction,
          symbol: autoCompleteField.symbol,
          quantity: formData.quantity,
          price: formData.price,
          commission: formData.commission,
        };
        const response = await fetch("/api/client_data/tradeLogInsert", {
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
    }
    clearForm();
  };

  function clearForm() {
    formData.date = new Date().toISOString().split("T")[0];
    formData.account = "Registered";
    formData.transaction = "Buy";
    setAutoCompleteField("");
    document.getElementById("autoCompleteInput").value = "";
    formData.quantity = "";
    formData.price = "";
    formData.commission = "";
  }

  const getSymbols = async () => {
    try {
      const response = await fetch("/api/market_data/symbols", {
        method: "GET",
        credentials: "same-origin",
        headers: {
          "content-type": "application/json",
        },
      });
      const data = await response.json();
      if (response.status === 200) {
        setSymbols(data);
      } else {
        setSymbols([]);
        setErrorMessage({
          isError: true,
          msg: "Server error: Server returned no symbols.",
        });
      }
    } catch (error) {
      console.log(error);
      setSymbols([]);
      setErrorMessage({
        isError: true,
        msg: "Server error: Failed to reach server.",
      });
    }
  };

  useEffect(() => {
    getSymbols();
  }, []);

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
      <form className="grid grid-rows-1 grid-cols-7 gap-4 py-4 h-14 text-sm dark: bg-black text-slate-600">
        <input
          type="date"
          value={formData.date || ""}
          onChange={handleChange("date")}
          className="rounded-lg pl-2"
          required
        />
        <select
          onChange={handleChange("account")}
          value={formData.account || "Registered"}
          className="rounded-lg pl-2"
        >
          <option value="Registered">Registered</option>
          <option value="Non-Registered">Non-Registered</option>
        </select>
        <select
          onChange={handleChange("transaction")}
          value={formData.transaction || "Buy"}
          className="rounded-lg pl-2"
        >
          <option value="Buy">Buy</option>
          <option value="Sell">Sell</option>
          <option value="Dividend">Dividend</option>
        </select>
        <AutoCompleteTicker
          data={symbols}
          onSelect={(AutoCompleteField) =>
            setAutoCompleteField(AutoCompleteField)
          }
        />
        <input
          type="text"
          value={formData.quantity || ""}
          onChange={handleChange("quantity")}
          placeholder="Quantity"
          className="pl-2 rounded-lg"
          required
        />
        <input
          type="text"
          value={formData.price || ""}
          onChange={handleChange("price")}
          placeholder="Price"
          className="rounded-lg pl-2"
          required
        />
        <input
          type="text"
          value={formData.commission || ""}
          onChange={handleChange("commission")}
          placeholder="Commission"
          className="rounded-lg pl-2"
          required
        />
      </form>
    </div>
  );
}

export default TradeLogForm;
