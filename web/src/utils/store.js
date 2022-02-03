import create from "zustand";
import { devtools, persist } from "zustand/middleware";

let settingsStore = (set) => ({
  isDarkMode: true,
  setIsDarkMode: () => set((state) => ({ isDarkMode: !state.isDarkMode })),
});

let authStore = (set) => ({
  csrfToken: null,
  setCsrfToken: (val) => set((state) => ({ csrfToken: val })),
  isLoggedIn: false,
  setIsLoggedIn: (val) => set((state) => ({ isLoggedIn: val })),
});

let dataStore = (set) => ({
  isTradeLogUpdated: true,
  setIsTradeLogUpdated: (val) => set((state) => ({ isTradeLogUpdated: val })),
  errorMessage: { isError: false, msg: "" },
  setErrorMessage: (val) => set((state) => ({ errorMessage: val })),
  symbol: "",
  setSymbol: (val) => set((state) => ({ symbol: val })),
});

settingsStore = devtools(settingsStore);
settingsStore = persist(settingsStore, { name: "user_settings" });

authStore = devtools(authStore);

dataStore = devtools(dataStore);

export const useSettingsStore = create(settingsStore);
export const UseAuthStore = create(authStore);
export const UseDataStore = create(dataStore);
