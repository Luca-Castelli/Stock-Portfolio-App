import { useState, useMemo } from "react";

export const useSortableData = (items = [], config = null) => {
  const [sortConfig, setSortConfig] = useState(config);

  const sortedItems = useMemo(() => {
    let sortableItems = [...items];
    if (sortConfig !== null) {
      sortableItems.sort((a, b) => {
        if (
          String(a[sortConfig.key]).localeCompare(
            String(b[sortConfig.key]),
            undefined,
            {
              numeric: true,
            }
          ) === -1
        ) {
          return sortConfig.direction === "asc" ? -1 : 1;
        }
        if (
          String(a[sortConfig.key]).localeCompare(
            String(b[sortConfig.key]),
            undefined,
            {
              numeric: true,
            }
          ) === 1
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
