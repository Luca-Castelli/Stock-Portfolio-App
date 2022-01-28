export function NumberDisplay(value, digits) {
  return value.toLocaleString(navigator.language, {
    minimumFractionDigits: digits,
  });
}
