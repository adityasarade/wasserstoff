import React, { useState } from "react";
import { Container, CssBaseline, Typography } from "@mui/material";
import UploadPage from "./components/UploadPage";
import SearchBar from "./components/SearchBar";
import ResultsTable from "./components/ResultsTable";
import ThemeDisplay from "./components/ThemeDisplay";
import api from "./api";

function App() {
  const [results, setResults] = useState(null);

  const handleSearch = async (query) => {
    try {
      const resp = await api.get("/search/", { params: { query, top_k: 5 } });
      setResults(resp.data);
    } catch (err) {
      console.error("Search failed", err);
      setResults(null);
    }
  };

  return (
    <>
      <CssBaseline />
      <Container maxWidth="md" sx={{ mt: 4 }}>
        <Typography variant="h4" align="center" gutterBottom>
          📄 Document Upload & Research Assistant
        </Typography>

        <UploadPage />

        <SearchBar onSearch={handleSearch} />

        {results?.individual_results && (
          <ResultsTable rows={results.individual_results} />
        )}

        {results?.synthesized_summary && (
          <ThemeDisplay text={results.synthesized_summary} />
        )}
      </Container>
    </>
  );
}

export default App;