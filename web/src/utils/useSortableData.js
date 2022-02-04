import { useState, useMemo } from "react";

export const useSortableData = (items = [], config = null) => {
  const [sortConfig, setSortConfig] = useState(config);

  const sortedItems = useMemo(() => {
    let sortableItems = [...items];
    if (sortConfig !== null) {
      sortableItems.sort((a, b) => {
        if (
          a[sortConfig.key].localeCompare(b[sortConfig.key], undefined, {
            numeric: true,
          }) === -1
        ) {
          return sortConfig.direction === "asc" ? -1 : 1;
        }
        if (
          a[sortConfig.key].localeCompare(b[sortConfig.key], undefined, {
            numeric: true,
          }) === 1
        ) {
          return sortConfig.direction === "asc" ? 1 : -1;
        }
        return 0;
      });
    }
    return sortableItems;
  }, [items, sortConfig]);

  const requestSort = (key) => {
    let direction = "asc";
    if (
      sortConfig !== null &&
      sortConfig.key === key &&
      sortConfig.direction === "asc"
    ) {
      direction = "desc";
    }
    setSortConfig({ key, direction });
  };

  return { items: sortedItems, requestSort, sortConfig };
};
