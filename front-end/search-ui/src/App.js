import "./App.css";
import SearchBar from "./components/SearchBar";
import FilterBar from "./components/FilterBar";
import SearchResults from "./components/SearchResults";
import React from "react";
import { createSearchUrl, searchRequest } from "./utils";
import ChevronRightIcon from "@mui/icons-material/ChevronRight";
import KeyboardArrowLeftIcon from "@mui/icons-material/KeyboardArrowLeft";
import Paper from "@mui/material/Paper";
import BottomNavigation from "@mui/material/BottomNavigation";
import BottomNavigationAction from "@mui/material/BottomNavigationAction";
import Typography from "@mui/material/Typography";

const initialState = {
  searchText: "",
  phraseSearch: false,
  filterDateFrom: "",
  filterDateTo: "",
  pageNumber: 0,
  pageShifted: false

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
    case "editPageNumber":
      const newPage = state.pageNumber + action.payload
      return { ...state, pageNumber: newPage, pageShifted: true };
    default:
      return state;
  }
}

const initialSearchResults = {
  documents: [],
  numberOfDocs: null,
  error: "",
};

function reducerSearchRes(state, action) {
  switch (action.type) {
    case "setResult":
      return { ...state, documents: action.payload.documents, error: "", numberOfDocs: action.payload.foundDocuments };
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

  function onSearch(pageNum ) {
    const url = createSearchUrl(
      state.searchText,
      state.phraseSearch,
      state.filterDateFrom,
      state.filterDateFrom,
      pageNum
    );

    const res = searchRequest(url, onSuccess, onFail);
  }

  React.useEffect(() => {
    if (state.pageShifted) {

      onSearch(state.pageNumber);
    }
  }, [state.pageNumber]);

  return (
    <div className="App">
      <SearchBar state={state} dispatch={dispatch} onSearch={onSearch} />
      <FilterBar state={state} dispatch={dispatch} />
      {searchRes.numberOfDocs && <p>Found { searchRes.numberOfDocs} documents.</p>}
      <SearchResults searchRes={searchRes} />
      <Paper
        sx={{ position: "fixed", bottom: 0, left: 0, right: 0 }}
        elevation={3}
      >
        <BottomNavigation
          showLabels
          onChange={(event, newValue) => {
            // If newValue is 0 then prev button
            // If newValue is 2 then next button
            const edit = newValue === 0 ? -1 : 1;
            dispatch({
              type: "editPageNumber",
              payload: edit,
            });
          }}
        >
          <BottomNavigationAction
            label="Recents"
            icon={<KeyboardArrowLeftIcon />}
            disabled={state.pageNumber === 0}
          />

          <div
            style={{
              height: "100%",
              width: "50px",
              top: "50%",
              bottom: "50%",
              padding: "5px",
              boxSizing: "border-box",
              display: "flex",
              justifyContent: "center",
              paddingTop: "10px",
            }}
          >
            <Typography variant="h6" sx={{ fontSize: 16 }}>
              {state.pageNumber}
            </Typography>
          </div>
          <BottomNavigationAction
            label="Next Page"
            icon={<ChevronRightIcon />}
          />
        </BottomNavigation>
      </Paper>
    </div>
  );
}

export default App;
