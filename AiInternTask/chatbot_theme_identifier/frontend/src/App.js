import React, { useEffect, useState } from 'react';
import {
  Box,
  CssBaseline,
  Container,
  Typography,
  IconButton,
  Drawer,
  Divider,
  Tooltip,
} from "@mui/material";
import ChevronLeftIcon from "@mui/icons-material/ChevronLeft";
import ChevronRightIcon from "@mui/icons-material/ChevronRight";
import UploadPage from "./components/UploadPage";
import DocumentList from "./components/DocumentList";
import SearchBar from "./components/SearchBar";
import ResultsTable from "./components/ResultsTable";
import ThemeDisplay from "./components/ThemeDisplay";
import api from "./api";

const BACKGROUND_IMAGE = process.env.PUBLIC_URL + "/bg.jpg";

function App() {
  const [results, setResults] = useState(null);
  const [selectedDocs, setSelectedDocs] = useState([]);
  const [docsVersion, setDocsVersion] = useState(0);
  const [drawerOpen, setDrawerOpen] = useState(true);

  // Clear backend knowledge base on every full page load
  useEffect(() => {
    api.post("/clear/").catch(console.error);
  }, []);

  useEffect(() => {
  fetch("https://adityasarade-wasserstoff.hf.space/reset/", { method: "POST" })
    .then(res => console.log("Reset done"))
    .catch(console.error);
}, []);

  const handleSearch = async (query) => {
    try {
      const params = { query, top_k: 5 };
      if (selectedDocs.length) params.doc_ids = selectedDocs.join(",");
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
      <Box
        sx={{
          position: "relative",
          minHeight: "100vh",
          backgroundImage: `url(${BACKGROUND_IMAGE})`,
          backgroundSize: "cover",
          backgroundPosition: "center",
        }}
      >


        <Box
          sx={{
            display: "flex",
            position: "relative",
            zIndex: 2,
            height: "100%",
          }}
        >
          {/* Toggle button */}
          <Tooltip title={drawerOpen ? "Close Knowledge Base" : "Open Knowledge Base"}>
            <IconButton
              onClick={() => setDrawerOpen(!drawerOpen)}
              sx={{
                position: "fixed",
                right: drawerOpen ? 300 : 0,
                top: "50%",
                overflowY:"auto",
                overflowX:"hidden",
                transform: "translateY(0%)",
                bgcolor: "primary.main",
                color: "white",
                "&:hover": { bgcolor: "primary.dark" },
                zIndex: 1100,
                width: 48,
                height: 48,
              }}
            >
              {drawerOpen ? <ChevronRightIcon /> : <ChevronLeftIcon />}
            </IconButton>
          </Tooltip>

          {/* Knowledge Base Drawer */}
          <Drawer
            variant="persistent"
            anchor="right"
            open={drawerOpen}
            sx={{
              width: 300,
              flexShrink: 0,
              "& .MuiDrawer-paper": {
                width: 300,
                boxSizing: "border-box",
                overflowY:"auto",
                overflowX:"hidden",
                p: 2,
                pt: 1,
                backgroundColor: "#fafafa",
              },
            }}
          >
            <Divider sx={{ mb: 1 }} />
            <DocumentList
              selected={selectedDocs}
              setSelected={setSelectedDocs}
              refreshTrigger={docsVersion}
            />
          </Drawer>

          {/* Main Content Centered */}
          <Box
            component="main"
            sx={{
              position: "absolute",
              top: "55%",
              left: drawerOpen
                ? `calc(50% - ${300 / 2}px)`
                : "50%",
              transform: "translate(-50%, 0%)",
              width: drawerOpen
                ? `calc(100% - 300px - 40px)`  // 40px buffer for toggle button
                : "90%",
              maxWidth: "md",
              p: 2,
            }}
          >
            <Container
              maxWidth="md"
              sx={{
                position: "relative",
                backgroundColor: "rgba(255,255,255,0.9)",
                borderRadius: 3,
                boxShadow: 3,
                py: 4,
              }}
            >
              {/* Header */}
              <Box sx={{ textAlign: "center", mb: 3 }}>
                <Typography variant="h4" gutterBottom>
                  Document Research & Theme Identification Chatbot
                </Typography>
                <Typography variant="subtitle1" color="textSecondary">
                  Upload your documents, ask any question in natural language, and let us find your answers and comprehensive themes along with precise citations.
                </Typography>
              </Box>

              {/* Actions & Results */}
              <Box display="flex" flexDirection="column" gap={3}>
                <UploadPage onUploadSuccess={() => setDocsVersion((v) => v + 1)} />
                <SearchBar onSearch={handleSearch} />
                {results?.individual_results && (
                  <ResultsTable rows={results.individual_results} />
                )}
                {results?.synthesized_summary && (
                  <ThemeDisplay text={results.synthesized_summary} />
                )}
              </Box>
            </Container>
          </Box>
        </Box>
      </Box>
    </>
  );
}

export default App;