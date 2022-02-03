import React from "react";
import Flags from "country-flag-icons/react/3x2";

const AutoCompleteTickerRow = ({ onSelectItem, isHighlighted, item }) => {
  const { symbol, name, region } = item;
  return (
    <li
      className={`${isHighlighted ? "bg-slate-300" : ""}`}
      onClick={onSelectItem}
    >
      <div className="border-y border-slate-200 text-xs">
        <div className="px-2 flex flex-row">
          {region === "US" ? (
            <Flags.US className="w-4" />
          ) : (
            <Flags.CA className="w-4" />
          )}
          <p className="px-2 font-bold">{symbol}</p>
        </div>

        <p className="px-2 border-t">{name}</p>
      </div>
    </li>
  );
};

export default AutoCompleteTickerRow;
