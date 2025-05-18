import React, { useState } from "react";
import { Box, TextField, Button } from "@mui/material";
import SearchIcon from "@mui/icons-material/Search";

const SearchBar = ({ onSearch }) => {
  const [query, setQuery] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (query.trim()) {
      onSearch(query.trim());
      setQuery(""); // clear the input after search
    }
  };

  return (
    <Box component="form" onSubmit={handleSubmit} sx={{ mt: 4, display: "flex", gap: 2 }}>
      <TextField
        fullWidth
        label="Enter your query"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />
      <Button type="submit" variant="contained" startIcon={<SearchIcon />}>
        Search
      </Button>
    </Box>
  );
};

export default SearchBar;