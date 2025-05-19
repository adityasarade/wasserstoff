import React, { useState } from "react";
import {
  Box,
  TextField,
  Button,
  Paper,
  Typography
} from "@mui/material";
import SearchIcon from "@mui/icons-material/Search";

const SearchBar = ({ onSearch }) => {
  const [query, setQuery] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    const trimmed = query.trim();
    if (trimmed) {
      onSearch(trimmed);
      setQuery("");
    }
  };

  return (
    <Paper
      elevation={3}
      sx={{
        maxWidth: 600,
        width: "100%",
        mx: "auto",
        p: 4,
        mt: 4,
        backgroundColor: "rgba(255,255,255,0.85)"
      }}
    >
      <Typography variant="h4" align="center" gutterBottom>
        Enter your Query
      </Typography>
      <Typography
        variant="body1"
        align="center"
        color="text.secondary"
        sx={{ mb: 3 }}
      >
        Retrieve your relevant extracts and synthesized themes.
      </Typography>

      <Box
        component="form"
        onSubmit={handleSubmit}
        sx={{ display: "flex", gap: 2 }}
      >
        <TextField
          fullWidth
          label="Enter your query"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          disabled={false}
        />
        <Button
          type="submit"
          variant="contained"
          startIcon={<SearchIcon />}
        >
          Search
        </Button>
      </Box>
    </Paper>
  );
};

export default SearchBar;