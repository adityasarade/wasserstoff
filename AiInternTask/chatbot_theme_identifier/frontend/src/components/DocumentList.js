import React, { useEffect, useState } from "react";
import {
  Box,
  Checkbox,
  List,
  ListItem,
  ListItemText,
  Typography,
} from "@mui/material";
import api from "../api";

const DocumentList = ({ selected, setSelected, refreshTrigger }) => {
  const [docs, setDocs] = useState([]);

  useEffect(() => {
    (async () => {
      try {
        const { data } = await api.get("/documents/");
        setDocs(data.documents);
        // select all by default whenever docs reload
        setSelected(data.documents.map((d) => d.doc_id));
      } catch (err) {
        console.error("Failed to fetch documents:", err);
      }
    })();
    // Re-run on mount and whenever refreshTrigger changes
  }, [refreshTrigger, setSelected]);

  const toggle = (id) => {
    setSelected((curr) =>
      curr.includes(id) ? curr.filter((x) => x !== id) : [...curr, id]
    );
  };

  return (
    <Box sx={{ mt: 4 }}>
      <Typography variant="h6" gutterBottom>
        Knowledge Base
      </Typography>
      <List>
        {docs.map((d) => (
          <ListItem
            key={d.doc_id}
            dense
            button
            onClick={() => toggle(d.doc_id)}
          >
            <Checkbox
              edge="start"
              checked={selected.includes(d.doc_id)}
              tabIndex={-1}
              disableRipple
            />
            <ListItemText primary={d.filename} secondary={d.doc_id} />
          </ListItem>
        ))}
      </List>
    </Box>
  );
};

export default DocumentList;