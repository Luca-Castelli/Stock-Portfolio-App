import React, { useEffect } from "react";
import { UseDataStore } from "../utils/store";

function ErrorMessage() {
  const errorMessage = UseDataStore((state) => state.errorMessage);
  const setErrorMessage = UseDataStore((state) => state.setErrorMessage);

  useEffect(() => {
    setTimeout(() => {
      setErrorMessage({ isError: false, msg: "" });
    }, 5000);
  }, [errorMessage]);

  return (
    <div className="h-1 mx-8">
      {errorMessage.isError && (
        <p className="text-red-500 animate-pulse">{errorMessage.msg}</p>
      )}
    </div>
  );
}

export default ErrorMessage;
