export function NumberDisplay(value, digits) {
  if (value === 0) {
    return "-";
  } else {
    return value.toLocaleString(navigator.language, {
      minimumFractionDigits: digits,
      maximumFractionDigits: digits,
    });
  }
}

export function PercentageDisplay(value, digits) {
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
