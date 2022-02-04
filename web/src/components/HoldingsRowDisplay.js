import React from "react";
import { NumberDisplay, PercentageDisplay } from "../utils/NumberDisplay";

function HoldingsRowDisplay({
  value,
  digits,
  isPercent = false,
  isColor = false,
}) {
  value = parseFloat(value);

  if (isPercent && isColor) {
    return (
      <td
        className={`pl-2 ${value > 0 ? `text-green-500` : null} 
                         ${value < 0 ? `text-red-500` : null}
                         ${value === 0 ? `text-slate-500` : null}`}
      >
        {PercentageDisplay(value, digits)}
      </td>
    );
  }

  if (isPercent && !isColor) {
    return (
      <td className={`pl-2 ${value === 0 ? `text-slate-500` : null}`}>
        {PercentageDisplay(value, digits)}
      </td>
    );
  }

  if (!isPercent && isColor) {
    return (
      <td
        className={`pl-2 ${value > 0 ? `text-green-500` : null} 
                         ${value < 0 ? `text-red-500` : null}
                         ${value === 0 ? `text-slate-500` : null}`}
      >
        {NumberDisplay(value, digits)}
      </td>
    );
  }

  if (!isPercent && !isColor) {
    return (
      <td className={`pl-2 ${value === 0 ? `text-slate-500` : null}`}>
        {NumberDisplay(value, digits)}
      </td>
    );
  }
}

export default HoldingsRowDisplay;
