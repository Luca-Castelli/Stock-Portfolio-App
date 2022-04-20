import React from "react";

function NumberDisplay({ value, digits, isPercent = false, isColor = false }) {
  value = parseFloat(value);

  function DecimalDisplay(value, digits) {
    if (value === 0) {
      return "-";
    } else {
      return value.toLocaleString(navigator.language, {
        minimumFractionDigits: digits,
        maximumFractionDigits: digits,
      });
    }
  }

  function PercentageDisplay(value, digits) {
    if (!value) {
      value = 0;
    }
    if (value === 0) {
      return "-";
    } else {
      return (
        value.toLocaleString(navigator.language, {
          minimumFractionDigits: digits,
          maximumFractionDigits: digits,
        }) + "%"
      );
    }
  }

  if (isPercent && isColor) {
    return (
      <div
        className={`pl-2 ${value > 0 ? `text-green-500` : null} 
                         ${value < 0 ? `text-red-500` : null}
                         ${value === 0 ? `text-slate-500` : null}`}
      >
        {PercentageDisplay(value, digits)}
      </div>
    );
  }

  if (isPercent && !isColor) {
    return (
      <div className={`pl-2 ${value === 0 ? `text-slate-500` : null}`}>
        {PercentageDisplay(value, digits)}
      </div>
    );
  }

  if (!isPercent && isColor) {
    return (
      <div
        className={`pl-2 ${value > 0 ? `text-green-500` : null} 
                         ${value < 0 ? `text-red-500` : null}
                         ${value === 0 ? `text-slate-500` : null}`}
      >
        {DecimalDisplay(value, digits)}
      </div>
    );
  }

  if (!isPercent && !isColor) {
    return (
      <div className={`pl-2 ${value === 0 ? `text-slate-500` : null}`}>
        {DecimalDisplay(value, digits)}
      </div>
    );
  }
}

export default NumberDisplay;
