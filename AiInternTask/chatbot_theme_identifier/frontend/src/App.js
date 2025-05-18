import React, { useState } from "react";
import { Container, CssBaseline, Typography } from "@mui/material";
import UploadPage from "./components/UploadPage";
import DocumentList from "./components/DocumentList";
import SearchBar from "./components/SearchBar";
import ResultsTable from "./components/ResultsTable";
import ThemeDisplay from "./components/ThemeDisplay";
import api from "./api";

function App() {
  const [results, setResults] = useState(null);
  const [selectedDocs, setSelectedDocs] = useState([]);
  const [docsVersion, setDocsVersion] = useState(0);

  const handleSearch = async (query) => {
    try {
      // Build the params object
      const params = { query, top_k: 5 };
      if (selectedDocs.length > 0) {
        params.doc_ids = selectedDocs.join(",");
      }

      const resp = await api.get("/search/", { params });
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

        {/* Pass a callback so UploadPage can signal a refresh */}
        <UploadPage onUploadSuccess={() => setDocsVersion(v => v + 1)} />

        {/* Show list of loaded documents and allow selection */}
       <DocumentList
         selected={selectedDocs}
         setSelected={setSelectedDocs}
         refreshTrigger={docsVersion}     
       />

        {/* Query input */}
        <SearchBar onSearch={handleSearch} />

        {/* Results table */}
        {results?.individual_results && (
          <ResultsTable rows={results.individual_results} />
        )}

        {/* Synthesized themes */}
        {results?.synthesized_summary && (
          <ThemeDisplay text={results.synthesized_summary} />
        )}
      </Container>
    </>
  );
}

export default App;