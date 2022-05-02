import * as React from "react";
import Paper from "@mui/material/Paper";

import Container from "@mui/material/Container";
import Checkbox from "@mui/material/Checkbox";
import Select from "@mui/material/Select";
import MenuItem from "@mui/material/MenuItem";
import { YEAR_VECTOR } from "../utils";

import InputLabel from "@mui/material/InputLabel";

export default function FilterBar({ state, dispatch }) {
  const handleDateChange = (event, field) => {
    dispatch({
      type: "setData",
      field: field,
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
        <InputLabel id="phraseSearch">Phrase search</InputLabel>
        <Checkbox
          id="phraseSearch"
          checked={state.phraseSearch}
          onChange={() =>
            dispatch({
              type: "setData",
              field: "phraseSearch",
              payload: !state.phraseSearch,
            })
          }
          inputProps={{ "aria-label": "controlled" }}
        />

        <InputLabel id="selectFrom">Year from</InputLabel>
        <Select
          labelId="yearFrom"
          id="selectFrom"
          value={state.filterDateFrom}
          label="From"
          onChange={(event) => handleDateChange(event, "filterDateFrom")}
        >
          {YEAR_VECTOR.map((option) => (
            <MenuItem key={option} value={option}>
              {option}
            </MenuItem>
          ))}
        </Select>
        <InputLabel id="selectTo">Year to</InputLabel>
        <Select
          labelId="yearTo"
          id="selectTo"
          value={state.filterDateTo}
          label="To"
          onChange={(event) => handleDateChange(event, "filterDateTo")}
        >
          {YEAR_VECTOR.map((option) => (
            <MenuItem key={option} value={option}>
              {option}
            </MenuItem>
          ))}
        </Select>
      </Paper>
    </Container>
  );
}
