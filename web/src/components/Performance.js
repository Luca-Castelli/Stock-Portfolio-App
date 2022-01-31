import React from "react";

function Performance() {
  return (
    <div className="m-8 max-w-5xl">
      <div className="grid grid-rows-1 grid-cols-3 gap-8 dark: text-white">
        <div className="grid grid-rows-2 cols-1 p-2 rounded-lg dark: bg-slate-700 ">
          <div>YTD Performance</div>
          <div className="ml-4 text-green-500">+15.45 %</div>
        </div>
        <div className="grid grid-rows-2 cols-1 p-2 rounded-lg dark: bg-slate-700 ">
          <div>MTD Performance</div>
          <div className="ml-4 text-green-500">+4.42 %</div>
        </div>
        <div className="grid grid-rows-2 cols-1 p-2 rounded-lg dark: bg-slate-700 ">
          <div>Daily Performance</div>
          <div className="ml-4 text-red-500">-1.45 %</div>
        </div>
      </div>
    </div>
  );
}

export default Performance;
