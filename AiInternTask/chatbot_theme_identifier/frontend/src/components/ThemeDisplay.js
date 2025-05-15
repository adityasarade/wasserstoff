import React from "react";
import { Box, Typography, Paper } from "@mui/material";

const ThemeDisplay = ({ text }) => (
  <Paper sx={{ mt: 4, p: 2, whiteSpace: "pre-wrap" }}>
    <Typography variant="h6">Synthesized Themes</Typography>
    <Typography variant="body1" sx={{ mt: 1 }}>
      {text}
    </Typography>
  </Paper>
);

export default ThemeDisplay;