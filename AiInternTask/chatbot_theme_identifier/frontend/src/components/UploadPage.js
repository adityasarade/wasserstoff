import React, { useState } from "react";
import { Box, Button, Typography, LinearProgress } from "@mui/material";
import CloudUploadIcon from "@mui/icons-material/CloudUpload";
import api from "../api";

const UploadPage = () => {
  const [selectedFiles, setSelectedFiles] = useState([]);
  const [uploading, setUploading] = useState(false);
  const [uploadMessage, setUploadMessage] = useState("");

  const handleFileChange = (e) => {
    setSelectedFiles([...e.target.files]);
    setUploadMessage("");
  };

  const handleUpload = async () => {
    if (selectedFiles.length === 0) {
      setUploadMessage("Please select files first.");
      return;
    }

    const formData = new FormData();
    selectedFiles.forEach((file) => {
      formData.append("files", file);
    });

    try {
      setUploading(true);
      const response = await api.post("/upload/", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setUploadMessage("✅ Files uploaded and processed successfully!");
      console.log(response.data);
    } catch (error) {
      setUploadMessage("❌ Upload failed. Check console for details.");
      console.error(error);
    } finally {
      setUploading(false);
    }
  };

  return (
    <Box p={4}>
      <Typography variant="h4" gutterBottom>
        Document Upload
      </Typography>

      <input
        type="file"
        multiple
        accept=".pdf,.png,.jpg,.jpeg"
        onChange={handleFileChange}
        style={{ marginBottom: "16px" }}
      />

      <Box>
        <Button
          variant="contained"
          color="primary"
          startIcon={<CloudUploadIcon />}
          onClick={handleUpload}
          disabled={uploading}
        >
          Upload
        </Button>
      </Box>

      {uploading && <LinearProgress sx={{ marginTop: 2 }} />}
      {uploadMessage && (
        <Typography mt={2} color={uploadMessage.includes("✅") ? "green" : "red"}>
          {uploadMessage}
        </Typography>
      )}
    </Box>
  );
};

export default UploadPage;