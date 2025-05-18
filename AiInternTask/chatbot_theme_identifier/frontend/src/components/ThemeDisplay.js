import React from "react";
import { Box, Typography, Paper } from "@mui/material";

const ThemeDisplay = ({ text }) => {
  return (
    <Paper sx={{ p: 2, mt: 4 }}>
      <Box p={2} bgcolor="grey.100">
      <Typography variant="h6" gutterBottom>
        Synthesized Themes
      </Typography>
      <Typography component="div" whiteSpace="pre-wrap">
        {text}
      </Typography>
      </Box>
    </Paper>
  );
};

export default ThemeDisplay;