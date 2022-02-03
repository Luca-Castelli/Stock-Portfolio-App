import React from "react";
import { IoMdRemoveCircle } from "react-icons/io";
import { UseAuthStore } from "../utils/store";
import { NumberDisplay } from "../utils/NumberDisplay";

function HoldingsRow({ item }) {
  const csrfToken = UseAuthStore((state) => state.csrfToken);

  const {
    id,
    account,
    symbol,
    quantity,
    average_cost_basis,
    average_cost_basis_ps,
    realized_gain,
    latest_price,
  } = item;

  return (
    <tr className="border-y text-sm dark: border-slate-700 text-white">
      <td className="pl-2">{account}</td>
      <td className="pl-2">{symbol}</td>
      <td className="pl-2">{quantity}</td>
      <td className="pl-2">{average_cost_basis_ps}</td>
      <td className="pl-2">{latest_price}</td>
      <td className="pl-2">{average_cost_basis}</td>
      <td className="pl-2">{NumberDisplay(0, 2)}</td>
      <td className="pl-2">{realized_gain}</td>
    </tr>
  );
}

export default HoldingsRow;
