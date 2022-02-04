import React, { useState, useRef, useEffect, useMemo } from "react";
import AutoCompleteTickerRow from "./AutoCompleteTickerRow";
import { AiOutlineSearch } from "react-icons/ai";

const AutoCompleteTicker = ({ data, onSelect }) => {
  const [isVisbile, setVisiblity] = useState(false);
  const [search, setSearch] = useState("");
  const [cursor, setCursor] = useState(-1);

  const searchContainer = useRef(null);
  const searchResultRef = useRef(null);

  useEffect(() => {
    window.addEventListener("mousedown", handleClickOutside);

    return () => {
      window.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);

  const scrollIntoView = (position) => {
    searchResultRef.current.parentNode.scrollTo({
      top: position,
      behavior: "smooth",
    });
  };

  useEffect(() => {
    if (cursor < 0 || cursor > suggestions.length || !searchResultRef) {
      return () => {};
    }

    let listItems = Array.from(searchResultRef.current.children);
    listItems[cursor] && scrollIntoView(listItems[cursor].offsetTop);
  }, [cursor]);

  const suggestions = useMemo(() => {
    if (!search) {
      return data.slice(0, 5);
    }
    setCursor(-1);
    let suggestionSpace = data.filter((item) =>
      item.symbol.toLowerCase().includes(search.toLowerCase())
    );
    return suggestionSpace.slice(0, 5);
  }, [data, search]);

  const handleClickOutside = (event) => {
    if (
      searchContainer.current &&
      !searchContainer.current.contains(event.target)
    ) {
      hideSuggestion();
    }
  };

  const showSuggestion = () => setVisiblity(true);

  const hideSuggestion = () => setVisiblity(false);

  const keyboardNavigation = (e) => {
    if (e.key === "ArrowDown") {
      isVisbile
        ? setCursor((c) => (c < suggestions.length - 1 ? c + 1 : c))
        : showSuggestion();
    }

    if (e.key === "ArrowUp") {
      setCursor((c) => (c > 0 ? c - 1 : 0));
    }

    if (e.key === "Escape") {
      hideSuggestion();
    }

    if (e.key === "Enter" && cursor > 0) {
      setSearch(suggestions[cursor].symbol);
      hideSuggestion();
      onSelect(suggestions[cursor]);
    }
  };

  return (
    <div ref={searchContainer}>
      <div className="flex flex-row pl-2 items-center rounded-lg box-border w-full h-full bg-white">
        <AiOutlineSearch color="black" />
        <input
          type="text"
          name="search"
          id="autoCompleteInput"
          autoComplete="off"
          value={search}
          onClick={showSuggestion}
          onChange={(e) => setSearch(e.target.value)}
          onKeyDown={(e) => keyboardNavigation(e)}
          className="pl-2 rounded-lg box-border w-full h-full outline-none"
          placeholder="Search..."
        />
      </div>

      {isVisbile ? (
        <div className="sticky text-black bg-white">
          <ul ref={searchResultRef}>
            {suggestions.map((item, idx) => (
              <AutoCompleteTickerRow
                key={item.symbol}
                onSelectItem={() => {
                  hideSuggestion();
                  setSearch(item.symbol);
                  onSelect(item);
                }}
                isHighlighted={cursor === idx ? true : false}
                item={item}
              />
            ))}
          </ul>
        </div>
      ) : null}
    </div>
  );
};

export default AutoCompleteTicker;
