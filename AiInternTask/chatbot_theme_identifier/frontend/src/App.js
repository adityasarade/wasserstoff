import React, { useState } from "react";
import {
  Container,
  CssBaseline,
  Typography,
  Tab,
  Tabs,
  Box,
} from "@mui/material";
import UploadPage from "./components/UploadPage";
import DocumentList from "./components/DocumentList";
import SearchBar from "./components/SearchBar";
import ResultsTable from "./components/ResultsTable";
import ThemeDisplay from "./components/ThemeDisplay";
import api from "./api";

function App() {
  const [tab, setTab] = useState(0);
  const [results, setResults] = useState(null);
  const [selectedDocs, setSelectedDocs] = useState([]);
  const [docsVersion, setDocsVersion] = useState(0);

  const handleSearch = async (query) => {
    const params = { query, top_k: 5 };
    if (selectedDocs.length) params.doc_ids = selectedDocs.join(",");
    const resp = await api.get("/search/", { params });
    setResults(resp.data);
  };

  return (
    <>
      <CssBaseline />
      <Container maxWidth="md" sx={{ mt: 4 }}>
        <Typography variant="h4" align="center" gutterBottom>
          📄 Document Research Assistant
        </Typography>

        {/* 1. Tabs to switch modes */}
        <Tabs
          value={tab}
          onChange={(_, v) => setTab(v)}
          centered
          sx={{ mb: 3 }}
        >
          <Tab label="Upload Documents" />
          <Tab label="Search & Themes" />
        </Tabs>

        {/* 2. Upload Mode */}
        {tab === 0 && (
          <Box>
            <UploadPage onUploadSuccess={() => setDocsVersion(v => v + 1)} />
            <Box sx={{ mt: 4 }}>
              <DocumentList
                selected={selectedDocs}
                setSelected={setSelectedDocs}
                refreshTrigger={docsVersion}
              />
            </Box>
          </Box>
        )}

        {/* 3. Search Mode */}
        {tab === 1 && (
          <Box>
            <SearchBar onSearch={handleSearch} />
            {results?.individual_results && (
              <Box sx={{ mt: 4 }}>
                <ResultsTable rows={results.individual_results} />
              </Box>
            )}
            {results?.synthesized_summary && (
              <Box sx={{ mt: 4 }}>
                <ThemeDisplay text={results.synthesized_summary} />
              </Box>
            )}
          </Box>
        )}
      </Container>
    </>
  );
}

export default App;