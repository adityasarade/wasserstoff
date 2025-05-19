import React, { useEffect, useState } from "react";
import {
  Box,
  Checkbox,
  List,
  ListItem,
  ListItemText,
  TextField,
  Typography,
  Toolbar,
} from "@mui/material";
import api from "../api";

const DocumentList = ({
  selected,
  setSelected,
  refreshTrigger,
  showFilter = true,      // always show filter in Drawer
}) => {
  const [docs, setDocs] = useState([]);
  const [filter, setFilter] = useState("");

  // Fetch docs whenever upload triggers a refresh
  useEffect(() => {
    (async () => {
      try {
        const { data } = await api.get("/documents/");
        setDocs(data.documents);
        // by default select all
        setSelected(data.documents.map((d) => d.doc_id));
      } catch (err) {
        console.error("Failed to fetch documents:", err);
      }
    })();
  }, [refreshTrigger, setSelected]);

  const toggle = (id) =>
    setSelected((prev) =>
      prev.includes(id) ? prev.filter((x) => x !== id) : [...prev, id]
    );

  // apply filter to filename or doc_id
  const displayed = docs.filter(
    (d) =>
      d.filename.toLowerCase().includes(filter.toLowerCase()) ||
      d.doc_id.toLowerCase().includes(filter.toLowerCase())
  );

  return (
    <Box
      sx={{
        width: 300,                  // Drawer width
        p: 2,                        // inner padding
        overflowY: "auto",
        height: "calc(100vh - 64px)" // full viewport minus AppBar (64px)
      }}
    >
      {/* pushes content below your AppBar */}
      <Toolbar />

      {showFilter && (
        <>
        <Typography
          variant="h6"
          sx={{ mb: 1, fontWeight: "bold", textAlign: "center" }}
          >
            Document List
        </Typography>
        <TextField
          fullWidth
          size="small"
          placeholder="Search documents…"
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
          sx={{ mb: 2 }}
        />
        </>
      )}

      <List dense>
        {displayed.map((d) => (
          <ListItem
            key={d.doc_id}
            button
            onClick={() => toggle(d.doc_id)}
          >
            <Checkbox
              edge="start"
              checked={selected.includes(d.doc_id)}
              tabIndex={-1}
            />
            <ListItemText primary={d.filename} secondary={d.doc_id} />
          </ListItem>
        ))}
        {displayed.length === 0 && (
          <Typography variant="body2" color="text.secondary">
            No documents match.
          </Typography>
        )}
      </List>
    </Box>
  );
};

export default DocumentList;
