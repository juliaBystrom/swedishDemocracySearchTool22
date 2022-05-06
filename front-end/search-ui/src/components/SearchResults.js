import * as React from "react";
import Box from "@mui/material/Box";
import Paper from "@mui/material/Paper";
import Container from "@mui/material/Container";
import { CardHeader } from "@mui/material";

import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import Typography from "@mui/material/Typography";
import { Button } from "@mui/material";
import { COLOURS, createDocumentByIdUrl, searchRequest } from "../utils";
import List from "@mui/material/List";
import ListItemButton from "@mui/material/ListItemButton";
import ListItemText from "@mui/material/ListItemText";
import Modal from "@mui/material/Modal";
import { getFormControlUnstyledUtilityClasses } from "@mui/base";

function crateTitle(doc) {
  const tType = `${doc._source.doktyp}`.toUpperCase();
  return `${tType} ${doc._source.nummer}`;
}

function reducerModal(state, action) {
  switch (action.type) {
    case "openModal":
      return { open: true, selectedDocId: action.payload };
    case "closeModal":
      return { open: false, selectedDocId: -1 };
    case "updateID":
      return { ...state, selectedDocId: action.payload };
    default:
      return state;
  }
}

export default function SearchResults({ searchRes }) {
  const [state, dispatch] = React.useReducer(reducerModal, {
    open: false,
    selectedDocId: -1,
  });

  const handleOpen = (docID) => {
    dispatch({
      type: "openModal",
      payload: docID,
    });
  };
  const handleClose = () => {
    dispatch({
      type: "closeModal",
    });
  };

  const handleChangeDocumentInModal = (docID) => {
    dispatch({
      type: "updateID",
      payload: docID,
    });
  };

  
  const searchResCards = searchRes.documents.map((doc, i) => {
    return (
      <Card
        sx={{
          textAlign: "left",
          marginBottom: 5,
          backgroundColor: COLOURS.base,
        }}
        key={doc._id}
      >
        <CardHeader
          sx={{ paddingBottom: 0 }}
          title={doc ? crateTitle(doc) : ""}
          subheader={doc._source.rm}
          action={
            <Button
              size="small"
              sx={{ backgroundColor: COLOURS.secondaryColour }}
              variant="contained"
              onClick={() => handleOpen(doc._id)}
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
              gridTemplateColumns: "2fr 3fr",
              backgroundColor: COLOURS.lightBase,
              padding: "5px",
            }}
          >
            <Box>
                <Typography variant="h6" component="div" sx={{ fontSize: 16 }}>
                  Sammanfattning
                </Typography>
              <Typography variant="body2" color={COLOURS.darkText}>
                {doc._source.summary}
              </Typography>
            </Box>
            <Box
              sx={{
                display: "grid",
                gap: 1,
                gridTemplateColumns: "repeat(2, 1fr)",
              }}
            >
              <Box
                sx={{
                  borderLeft: "2px solid " + COLOURS.base,
                  paddingLeft: "5px",
                }}
              >
                <Typography variant="h6" component="div" sx={{ fontSize: 16 }}>
                  Refererar till 
                </Typography>
                <List dense style={{maxHeight: 200, overflow: 'auto'}}>
                  {getRefListedItems(doc._source.ref_out_objects, handleOpen)}
                </List>
              </Box>

              <Box
                sx={{
                  borderLeft: "2px solid " + COLOURS.base,
                  paddingLeft: "5px",
                }}
              >
                <Typography variant="h6" component="div" sx={{ fontSize: 16 }}>
                  Refererad av
                </Typography>
                <List dense style={{maxHeight: 200, overflow: 'auto'}}>
                  {getRefListedItems(doc._source.ref_in_objects, handleOpen)}
                </List>
              </Box>
            </Box>
          </Box>
        </CardContent>
      </Card>
    );
  });

  return (
    <Container sx={{}}>
      <Paper>{searchResCards}</Paper>
      {state.selectedDocId != -1 && (
        <BasicModal
          open={state.open}
          handleClose={handleClose}
          docID={state.selectedDocId}
          handleChangeDocumentInModal={handleChangeDocumentInModal}
        />
      )}
    </Container>
  );
}

const style = {
  position: "absolute",
  top: "50%",
  left: "50%",
  transform: "translate(-50%, -50%)",
  width: "80%",
  bgcolor: "background.paper",
  border: "2px solid #000",
  boxShadow: 24,
  p: 4,
};
const LOADING_STATUS = {
  LOADING: 0,
  SUCCESS: 1,
  ERROR: 2,
};

export function BasicModal({
  open,
  handleClose,
  docID,
  handleChangeDocumentInModal,
}) {
  const [loadingStatus, setLoadingStatus] = React.useState(
    LOADING_STATUS.LOADING
  );
  const [doc, setDoc] = React.useState(null);

  const onSuccess = (data) => {
    setDoc(data);
    setLoadingStatus(LOADING_STATUS.SUCCESS);
  };

  const onError = (error) => {
    setLoadingStatus(LOADING_STATUS.ERROR);
  };

  
  React.useEffect(() => {
    if (docID) {
      setLoadingStatus(LOADING_STATUS.LOADING);
      const url = createDocumentByIdUrl(docID);
      const res = searchRequest(url, onSuccess, onError);
    }
  }, [docID]);

  return (
    doc && (
      <div>
        <Modal
          open={open}
          onClose={() => handleClose}
          aria-labelledby="Document display"
        >
          <Box sx={style}>
            <Box
              sx={{
                display: "grid",
                gridTemplateColumns: "repeat(2, 1fr)",
              }}
            >
              <Typography id="modal-modal-title" variant="h6" component="h2">
                {crateTitle(doc)}
              </Typography>
              <Button color="error" onClick={() => handleClose()}>
                Close
              </Button>
            </Box>

            <Box
              sx={{
                display: "grid",
                gap: 1,
                gridTemplateColumns: "2fr 3fr",
                backgroundColor: COLOURS.lightBase,
                padding: "5px",
              }}
            >
              <Box>
                  <Typography
                    variant="h6"
                    component="div"
                    sx={{ fontSize: 14 }}
                  >
                    Sammanfattning 
                  </Typography>
                <Typography variant="body2" color={COLOURS.darkText}>
                  {doc._source.summary}
                </Typography>
                <Button onClick={() => window.open(doc._source.pdf_url, '_blank')}>
                    Öppna PDF
                </Button>
              </Box>
              <Box
                sx={{
                  display: "grid",
                  gap: 1,
                  gridTemplateColumns: "repeat(2, 1fr)",
                }}
              >
                <Box
                  sx={{
                    borderLeft: "2px solid " + COLOURS.base,
                    paddingLeft: "5px",
                  }}
                >
                  <Typography
                    variant="h6"
                    component="div"
                    sx={{ fontSize: 14 }}
                  >
                    Refererar till
                  </Typography>
                  <List dense style={{maxHeight: 600, overflow: 'auto'}}>
                    {getRefListedItems(
                      doc._source.ref_out_objects,
                      handleChangeDocumentInModal
                    )}
                  </List>
                </Box>
                <Box
                  sx={{
                    borderLeft: "2px solid " + COLOURS.base,
                    paddingLeft: "5px",
                  }}
                >
                  <Typography
                    variant="h6"
                    component="div"
                    sx={{ fontSize: 14 }}>
                    Refererad av
                  </Typography>
                  <List dense style={{maxHeight: 600, overflow: 'auto'}}>
                    {getRefListedItems(
                      doc._source.ref_in_objects,
                      handleChangeDocumentInModal
                    )}
                  </List>
                </Box>
              </Box>
            </Box>
          </Box>
        </Modal>
      </div>
    )
  );
}

const getRefListedItems = (ref_objects_list, handleClickOnItem) =>
  ref_objects_list.map((ref, i) => {
    return (
      <ListItemButton
        sx={{ margin: 0, pading: 0 }}
        key={`${ref._id} ${i}`}
        onClick={() => handleClickOnItem(ref._id)}
      >
        <ListItemText
          primary={crateTitle(ref)}
          secondary={ref?._source.rm}
          dense={true}
        />

        <Typography
          sx={{
            margin: 0,
            pading: 0,
            color: COLOURS.primary,
            border: COLOURS.primary,
          }}
        >
          VISA
        </Typography>
      </ListItemButton>
    );
  });
