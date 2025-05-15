import React from "react";
import { Table, TableHead, TableBody, TableRow, TableCell, Paper, TableContainer } from "@mui/material";

const ResultsTable = ({ rows }) => (
  <TableContainer component={Paper} sx={{ mt: 4 }}>
    <Table>
      <TableHead>
        <TableRow>
          <TableCell>Document ID</TableCell>
          <TableCell>Extracted Answer</TableCell>
          <TableCell>Citation</TableCell>
        </TableRow>
      </TableHead>
      <TableBody>
        {rows.map((r, i) => (
          <TableRow key={i}>
            <TableCell>{r["Document ID"]}</TableCell>
            <TableCell>{r["Extracted Answer"]}</TableCell>
            <TableCell>{r["Citation"]}</TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  </TableContainer>
);

export default ResultsTable;