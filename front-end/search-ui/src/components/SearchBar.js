import * as React from "react";
import Paper from "@mui/material/Paper";
import InputBase from "@mui/material/InputBase";
import Divider from "@mui/material/Divider";
import IconButton from "@mui/material/IconButton";
import SearchIcon from "@mui/icons-material/Search";
import Container from "@mui/material/Container";

export default function SearchBar({ state, dispatch, onSearch }) {
  const handleChange = (event) => {
    dispatch({
      type: "setData",
      field: "searchText",
      payload: event.target.value,
    });
  };

  return (
    <Container>
      <Paper
        component="form"
        sx={{
          p: "2px 4px",
          display: "flex",
          alignItems: "center",
          width: "100%",
          margin: "10px 0",
        }}
      >
        <InputBase
          sx={{ ml: 1, flex: 1 }}
          placeholder="Search"
          inputProps={{ "aria-label": "search" }}
          onChange={handleChange}
          value={state.searchText}
        />
        <Divider sx={{ height: 28, m: 0.5 }} orientation="vertical" />

        <IconButton
          sx={{ p: "10px" }}
          aria-label="search"
          onClick={() => onSearch(0)}
        >
          <SearchIcon />
        </IconButton>
      </Paper>
    </Container>
  );
}
