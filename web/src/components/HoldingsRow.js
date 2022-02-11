import React from "react";
import HoldingsRowDisplay from "./HoldingsRowDisplay";

function HoldingsRow({ item }) {
  const {
    id,
    account,
    symbol,
    quantity,
    average_cost_basis,
    average_cost_basis_ps,
    realized_pnl,
    dividends,
    latest_price,
    market_value,
    weight,
    unrealized_pnl,
    unrealized_pnl_percent,
  } = item;

  return (
    <tr className="border-y text-xs dark: border-slate-700 text-white">
      <td className="pl-2">{account}</td>
      <td className="pl-2">{symbol}</td>
      <HoldingsRowDisplay value={weight} digits={0} isPercent={true} />
      <HoldingsRowDisplay value={quantity} digits={0} />
      <HoldingsRowDisplay value={average_cost_basis_ps} digits={2} />
      <HoldingsRowDisplay value={latest_price} digits={2} />
      <HoldingsRowDisplay value={average_cost_basis} digits={0} />
      <HoldingsRowDisplay value={market_value} digits={0} />
      <HoldingsRowDisplay value={unrealized_pnl} digits={0} isColor={true} />
      <HoldingsRowDisplay
        value={unrealized_pnl_percent}
        digits={0}
        isPercent={true}
        isColor={true}
      />
      <HoldingsRowDisplay value={dividends} digits={0} />
      <HoldingsRowDisplay value={realized_pnl} digits={0} isColor={true} />
    </tr>
  );
}

export default HoldingsRow;
