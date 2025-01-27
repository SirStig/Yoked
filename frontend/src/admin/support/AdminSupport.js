import React, { useState, useEffect } from "react";
import styled from "styled-components";
import { DataGrid } from "@mui/x-data-grid";
import { FaReply, FaCheckCircle, FaTrashAlt } from "react-icons/fa";

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

const AdminSupport = () => {
  const [tickets, setTickets] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Simulate fetching data from the backend
    setTimeout(() => {
      setTickets([
        {
          id: 1,
          user: "John Doe",
          issue: "Cannot log in",
          status: "Open",
          createdAt: "2025-01-15",
        },
        {
          id: 2,
          user: "Jane Smith",
          issue: "Payment not processed",
          status: "Resolved",
          createdAt: "2025-01-14",
        },
      ]);
      setLoading(false);
    }, 1000);
  }, []);

  const handleReply = (id) => {
    console.log(`Reply to ticket ID: ${id}`);
    // Redirect or open modal for replying to the ticket
  };

  const handleResolve = (id) => {
    console.log(`Mark ticket ID: ${id} as resolved`);
    // Trigger backend API call to mark the ticket as resolved
  };

  const handleDelete = (id) => {
    console.log(`Delete ticket ID: ${id}`);
    // Trigger backend API call to delete the ticket
  };

  const columns = [
    { field: "id", headerName: "ID", width: 80 },
    { field: "user", headerName: "User", width: 200 },
    { field: "issue", headerName: "Issue", width: 300 },
    { field: "status", headerName: "Status", width: 150 },
    { field: "createdAt", headerName: "Created At", width: 200 },
    {
      field: "actions",
      headerName: "Actions",
      width: 350,
      renderCell: (params) => (
        <div style={{ display: "flex", gap: "0.5rem" }}>
          <ActionButton onClick={() => handleReply(params.row.id)}>
            <FaReply /> Reply
          </ActionButton>
          <ActionButton
            onClick={() => handleResolve(params.row.id)}
            disabled={params.row.status === "Resolved"}
          >
            <FaCheckCircle /> Resolve
          </ActionButton>
          <ActionButton onClick={() => handleDelete(params.row.id)}>
            <FaTrashAlt /> Delete
          </ActionButton>
        </div>
      ),
    },
  ];

  return (
    <Container>
      <Header>Support Tickets</Header>
      <ButtonContainer>
        {/* Future: Add filters or bulk actions */}
      </ButtonContainer>
      <DataGrid
        rows={tickets}
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

export default AdminSupport;
