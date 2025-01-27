import React, { useState, useEffect } from "react";
import styled from "styled-components";
import { DataGrid } from "@mui/x-data-grid";
import { FaPlus, FaEdit, FaTrashAlt, FaPaperPlane } from "react-icons/fa";

const Container = styled.div`
  padding: 2rem;
  background-color: ${({ theme }) => theme.colors.background};
  color: ${({ theme }) => theme.colors.textPrimary};
`;

const Header = styled.h2`
  text-align: center;
  margin-bottom: 1.5rem;
  color: ${({ theme }) => theme.colors.primary};
`;

const ButtonContainer = styled.div`
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-bottom: 1.5rem;
`;

const ActionButton = styled.button`
  padding: 0.5rem 1rem;
  color: white;
  background-color: ${({ theme }) => theme.colors.primary};
  border: none;
  border-radius: ${({ theme }) => theme.borderRadius};
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;

  &:hover {
    background-color: ${({ theme }) => theme.colors.primaryHover};
  }

  &:disabled {
    background-color: ${({ theme }) => theme.colors.disabled};
    cursor: not-allowed;
  }
`;

const AdminEmail = () => {
  const [emails, setEmails] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Simulate fetching data from the backend
    setTimeout(() => {
      setEmails([
        {
          id: 1,
          subject: "January Promotion",
          type: "One-Time",
          status: "Scheduled",
          date: "2025-01-15",
        },
        {
          id: 2,
          subject: "Weekly Tips",
          type: "Recurring",
          status: "Active",
          date: "Every Monday",
        },
      ]);
      setLoading(false);
    }, 1000);
  }, []);

  const handleCreateEmail = () => {
    console.log("Create new email");
    // Redirect or open modal for creating email
  };

  const handleEditEmail = (id) => {
    console.log(`Edit email with ID: ${id}`);
    // Redirect or open modal for editing email
  };

  const handleDeleteEmail = (id) => {
    console.log(`Delete email with ID: ${id}`);
    // Trigger backend API call to delete email
  };

  const handleSendEmailNow = (id) => {
    console.log(`Send email with ID: ${id} now`);
    // Trigger backend API call to send email immediately
  };

  const columns = [
    { field: "id", headerName: "ID", width: 80 },
    { field: "subject", headerName: "Subject", width: 250 },
    { field: "type", headerName: "Type", width: 150 },
    { field: "status", headerName: "Status", width: 150 },
    { field: "date", headerName: "Schedule/Date", width: 200 },
    {
      field: "actions",
      headerName: "Actions",
      width: 350,
      renderCell: (params) => (
        <div style={{ display: "flex", gap: "0.5rem" }}>
          <ActionButton onClick={() => handleEditEmail(params.row.id)}>
            <FaEdit /> Edit
          </ActionButton>
          <ActionButton onClick={() => handleSendEmailNow(params.row.id)}>
            <FaPaperPlane /> Send Now
          </ActionButton>
          <ActionButton onClick={() => handleDeleteEmail(params.row.id)}>
            <FaTrashAlt /> Delete
          </ActionButton>
        </div>
      ),
    },
  ];

  return (
    <Container>
      <Header>Manage Emails</Header>
      <ButtonContainer>
        <ActionButton onClick={handleCreateEmail}>
          <FaPlus /> Create New Email
        </ActionButton>
      </ButtonContainer>
      <DataGrid
        rows={emails}
        columns={columns}
        pageSize={5}
        rowsPerPageOptions={[5, 10, 20]}
        autoHeight
        disableSelectionOnClick
        loading={loading}
      />
    </Container>
  );
};

export default AdminEmail;
