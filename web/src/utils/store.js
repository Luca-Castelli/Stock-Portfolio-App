import create from "zustand";
import { devtools, persist } from "zustand/middleware";

let settingsStore = (set) => ({
  isDarkMode: true,
  setIsDarkMode: () => set((state) => ({ isDarkMode: !state.isDarkMode })),
  isLoggedIn: false,
  setIsLoggedIn: (val) => set((state) => ({ isLoggedIn: val })),
});

let authStore = (set) => ({
  csrfToken: null,
  setCsrfToken: (val) => set((state) => ({ csrfToken: val })),
});

let dataStore = (set) => ({
  isTradeLogUpdated: true,
  setIsTradeLogUpdated: (val) => set((state) => ({ isTradeLogUpdated: val })),
});

settingsStore = devtools(settingsStore);
settingsStore = persist(settingsStore, { name: "user_settings" });

authStore = devtools(authStore);

dataStore = devtools(dataStore);

export const useSettingsStore = create(settingsStore);
export const UseAuthStore = create(authStore);
export const UseDataStore = create(dataStore);
