import React from "react";
import NumberDisplay from "./NumberDisplay";

function HoldingsRow({ item }) {
  const {
    id,
    account,
    symbol,
    weight,
    post_qty,
    src_post_acb_ps,
    price,
    src_post_acb,
    src_market_value,
    cad_unrealized_gain,
    cad_unrealized_gain_fx,
    cad_unrealized_gain_percent,
    cad_realized_gain_dividend,
    cad_realized_gain_sell,
    cad_realized_gain_sell_fx,
  } = item;

  return (
    <tr className="border-y text-xs dark: border-slate-700 text-white">
      <td className="pl-2">{account}</td>
      <td className="pl-2">{symbol}</td>
      <td>
        <NumberDisplay value={weight} digits={0} isPercent={true} />
      </td>
      <td>
        <NumberDisplay value={post_qty} digits={0} />
      </td>
      <td>
        <NumberDisplay value={src_post_acb_ps} digits={2} />
      </td>
      <td>
        <NumberDisplay value={price} digits={2} />
      </td>
      <td>
        <NumberDisplay value={src_post_acb} digits={0} />
      </td>
      <td>
        <NumberDisplay value={src_market_value} digits={0} />
      </td>
      <td>
        <NumberDisplay value={cad_unrealized_gain} digits={0} isColor={true} />
      </td>
      <td>
        <NumberDisplay
          value={cad_unrealized_gain_percent}
          digits={0}
          isPercent={true}
          isColor={true}
        />
      </td>
      <td>
        <NumberDisplay value={cad_realized_gain_dividend} digits={0} />
      </td>
      <td>
        <NumberDisplay
          value={cad_realized_gain_sell}
          digits={0}
          isColor={true}
        />
      </td>
    </tr>
  );
}

export default HoldingsRow;
