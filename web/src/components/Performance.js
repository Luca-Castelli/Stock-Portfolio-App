import React, { useState, useEffect } from "react";
import { UseDataStore } from "../utils/store";
import NumberDisplay from "./NumberDisplay";

function Performance() {
  const isTradeLogUpdated = UseDataStore((state) => state.isTradeLogUpdated);
  const [returns, setReturns] = useState([]);

  const getReturns = async () => {
    try {
      const response = await fetch("/api/client_data/returns", {
        method: "GET",
        credentials: "same-origin",
        headers: {
          "content-type": "application/json",
        },
      });
      const data = await response.json();
      if (response.status === 200) {
        setReturns(data);
      } else {
        setReturns([]);
      }
    } catch (error) {
      console.log(error);
      setReturns([]);
    }
  };

  useEffect(() => {
    getReturns();
  }, [isTradeLogUpdated]);

  console.log(returns);
  return (
    <div className="m-8 max-w-5xl">
      <div className="grid grid-rows-1 grid-cols-3 gap-8 dark: text-white">
        <div className="grid grid-rows-2 cols-1 p-2 rounded-lg dark: bg-slate-700 ">
          <div>YTD Performance</div>
          {returns.ytd_percent && (
            <NumberDisplay
              value={returns.ytd_percent}
              digits={1}
              isPercent={true}
              isColor={true}
            />
          )}
        </div>
        <div className="grid grid-rows-2 cols-1 p-2 rounded-lg dark: bg-slate-700 ">
          <div>MTD Performance</div>
          {returns.mtd_percent && (
            <NumberDisplay
              value={returns.mtd_percent}
              digits={1}
              isPercent={true}
              isColor={true}
            />
          )}
        </div>
        <div className="grid grid-rows-2 cols-1 p-2 rounded-lg dark: bg-slate-700 ">
          <div>Daily Performance</div>
          {returns.dtd_percent && (
            <NumberDisplay
              value={returns.dtd_percent}
              digits={1}
              isPercent={true}
              isColor={true}
            />
          )}
        </div>
      </div>
    </div>
  );
}

export default Performance;
