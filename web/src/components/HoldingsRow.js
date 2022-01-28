import React from "react";
import { IoMdRemoveCircle } from "react-icons/io";
import { UseAuthStore } from "../utils/store";
import { NumberDisplay } from "../utils/NumberDisplay";

function HoldingsRow({ item }) {
  const csrfToken = UseAuthStore((state) => state.csrfToken);

  const {
    id,
    account,
    ticker,
    quantity,
    average_cost_basis,
    average_cost_basis_ps,
  } = item;

  return (
    <tr className="border-y dark: border-slate-700 text-white ">
      <td className="pl-2">{account}</td>
      <td className="pl-2">{ticker}</td>
      <td className="pl-2">{NumberDisplay(quantity, 0)}</td>
      <td className="pl-2">{NumberDisplay(average_cost_basis, 2)}</td>
      <td className="pl-2">{NumberDisplay(average_cost_basis_ps, 2)}</td>
    </tr>
  );
}

export default HoldingsRow;
