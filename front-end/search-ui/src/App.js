import "./App.css";
import SearchBar from "./components/SearchBar";
import FilterBar from "./components/FilterBar";
import SearchResults from "./components/SearchResults";
import React from "react";
import { createSearchUrl, searchRequest } from "./utils";

const initialState = {
  searchText: "",
  phraseSearch: false,
  filterDateFrom: "",
  filterDateTo: "",
};

function reducer(state, action) {
  switch (action.type) {
    case "setData":
      return { ...state, [action.field]: action.payload };
    case "resetData":
      return { ...state, [action.field]: initialState[action.field] };
    case "resetAllFilters":
      return {
        ...state,
        phraseSearch: false,
        filterDateFrom: "",
        filterDateTo: "",
      };
    case "resetAll":
      return { ...initialState };
    default:
      return state;
  }
}

const initialSearchResults = {
  documents: [],
  error: "",
};

function reducerSearchRes(state, action) {
  switch (action.type) {
    case "setResult":
      return { ...state, documents: action.payload, error: "" };
    case "setError":
      return {
        ...state,
        documents: initialSearchResults["documents"],
        error: action.payload,
      };
    case "reset":
      return { ...initialSearchResults };
    default:
      return state;
  }
}

function App() {
  const [state, dispatch] = React.useReducer(reducer, initialState);
  const [searchRes, dispatchSearchRes] = React.useReducer(
    reducerSearchRes,
    initialSearchResults
  );

  const onSuccess = (jsonRes) => {
    dispatchSearchRes({
      type: "setResult",
      field: "documents",
      payload: jsonRes,
    });
  };

  const onFail = (error) =>
    dispatchSearchRes({
      type: "setError",
      field: "error",
      payload: error,
    });

  function onSearch() {
    const url = createSearchUrl(
      state.searchText,
      state.phraseSearch,
      state.filterDateFrom,
      state.filterDateFrom,
      state.filterDateFrom
    );

    const res = searchRequest(url, onSuccess, onFail);
  }

  return (
    <div className="App">
      <SearchBar state={state} dispatch={dispatch} onSearch={onSearch} />
      <FilterBar state={state} dispatch={dispatch} />
      <SearchResults searchRes={searchRes} />
    </div>
  );
}

export default App;
