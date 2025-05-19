import React, { useState, useRef } from "react";
import {
  Box,
  Button,
  Typography,
  LinearProgress,
  Paper,
  List,
  ListItem,
  ListItemText
} from "@mui/material";
import CloudUploadIcon from "@mui/icons-material/CloudUpload";
import api from "../api";

const UploadPage = ({ onUploadSuccess }) => {
  const [selectedFiles, setSelectedFiles] = useState([]);
  const [uploading, setUploading] = useState(false);
  const [uploadMessage, setUploadMessage] = useState("");
  const fileInputRef = useRef();

  const handleFileChange = (e) => {
    setSelectedFiles(Array.from(e.target.files));
    setUploadMessage("");
  };

  const handleChooseClick = () => {
    fileInputRef.current.click();
  };

  const handleUpload = async () => {
    if (selectedFiles.length === 0) {
      setUploadMessage("⚠️ Please choose at least one file.");
      return;
    }

    const formData = new FormData();
    selectedFiles.forEach((file) => formData.append("files", file));

    try {
      setUploading(true);
      const response = await api.post("/upload/", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setUploadMessage("✅ Files uploaded and processed successfully!");
      if (onUploadSuccess) onUploadSuccess();
      console.log(response.data);
      setSelectedFiles([]); // reset after success
    } catch (error) {
      setUploadMessage("❌ Upload failed. Check console for details.");
      console.error(error);
    } finally {
      setUploading(false);
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
         Upload Document
      </Typography>

      <Typography
        variant="body1"
        align="center"
        sx={{ mb: 3, color: "text.secondary" }}
      >
        Please upload your PDFs or scanned images here.
      </Typography>

      {/* Hidden native file input */}
      <input
        type="file"
        multiple
        accept=".pdf,.png,.jpg,.jpeg"
        ref={fileInputRef}
        onChange={handleFileChange}
        style={{ display: "none" }}
      />

      {/* Styled controls */}
      <Box
        sx={{ display: "flex", gap: 2, justifyContent: "center", mb: 2 }}
      >
        <Button
          variant="outlined"
          onClick={handleChooseClick}
          disabled={uploading}
        >
          Choose Files
        </Button>
        <Button
          variant="contained"
          startIcon={<CloudUploadIcon />}
          onClick={handleUpload}
          disabled={uploading}
        >
          Upload
        </Button>
      </Box>

      {/* Selected files list */}
      {selectedFiles.length > 0 && (
        <List dense sx={{ maxHeight: 120, overflowY: "auto", mb: 2 }}>
          {selectedFiles.map((file, idx) => (
            <ListItem key={idx}>
              <ListItemText
                primary={file.name}
                secondary={`${(file.size / 1024).toFixed(1)} KB`}
              />
            </ListItem>
          ))}
        </List>
      )}

      {uploading && <LinearProgress />}

      {uploadMessage && (
        <Typography
          mt={2}
          align="center"
          color={uploadMessage.includes("✅") ? "success.main" : "error.main"}
        >
          {uploadMessage}
        </Typography>
      )}
    </Paper>
  );
};

export default UploadPage;