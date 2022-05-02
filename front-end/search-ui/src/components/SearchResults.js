import * as React from "react";
import Box from "@mui/material/Box";
import Paper from "@mui/material/Paper";
import Container from "@mui/material/Container";
import { CardHeader } from "@mui/material";

import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import Typography from "@mui/material/Typography";
import { Button } from "@mui/material";
import { COLOURS } from "../utils";
export default function SearchResults({ searchRes }) {
  const searchResCards = searchRes.documents.map((doc, i) => {
    return (
      <Card
        sx={{
          textAlign: "left",
          marginBottom: 5,
          backgroundColor: COLOURS.base,
        }}
      >
        <CardHeader
          title={doc._id}
          subheader={doc._source.rm}
          action={
            <Button
              size="small"
              sx={{ backgroundColor: COLOURS.secondaryColour }}
              variant="contained"
            >
              Visa dokument
            </Button>
          }
        />
        <CardContent>
          <Box
            sx={{
              display: "grid",
              gap: 1,
              gridTemplateColumns: "repeat(2, 1fr)",
            }}
          >
            <Box>
              <Typography variant="body2" color={COLOURS.darkText}>
                {doc._source.summary}
              </Typography>
            </Box>
            <Box>
              <Typography variant="body2" color={COLOURS.darkText}>
                TODO references TODO references TODO references TODO references
              </Typography>
            </Box>
          </Box>
        </CardContent>
      </Card>
    );
  });

  return (
    <Container sx={{}}>
      <Paper>{searchResCards}</Paper>
    </Container>
  );
}
