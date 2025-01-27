import React, { useState } from "react";
import styled from "styled-components";
import { DataGrid } from "@mui/x-data-grid";
import { FaEnvelope, FaUserEdit, FaFlag, FaBan, FaSearch } from "react-icons/fa";

const Container = styled.div`
  padding: 1.5rem;
  background-color: ${({ theme }) => theme.colors.background};
  color: ${({ theme }) => theme.colors.textPrimary};
`;

const Header = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  color: ${({ theme }) => theme.colors.primary};
`;

const Title = styled.h2`
  margin: 0;
`;

const SearchBar = styled.div`
  display: flex;
  align-items: center;
  background-color: ${({ theme }) => theme.colors.cardBackground};
  padding: 0.5rem;
  border-radius: ${({ theme }) => theme.borderRadius};
  box-shadow: ${({ theme }) => theme.shadows.small};
`;

const SearchInput = styled.input`
  border: none;
  outline: none;
  font-size: 1rem;
  margin-left: 0.5rem;
  background: transparent;
  color: ${({ theme }) => theme.colors.textPrimary};
  flex: 1;

  &::placeholder {
    color: ${({ theme }) => theme.colors.textSecondary};
  }
`;

const ActionButton = styled.button`
  margin: 0.25rem;
  padding: 0.3rem 0.5rem;
  color: white;
  background-color: ${({ theme }) => theme.colors.primary};
  border: none;
  border-radius: ${({ theme }) => theme.borderRadius};
  cursor: pointer;
  font-size: 0.8rem;
  display: inline-flex;
  align-items: center;
  gap: 0.3rem;

  &:hover {
    background-color: ${({ theme }) => theme.colors.primaryHover};
  }

  &:disabled {
    background-color: ${({ theme }) => theme.colors.disabled};
    cursor: not-allowed;
  }
`;

const StyledDataGrid = styled(DataGrid)`
  & .MuiDataGrid-columnHeaders {
    background-color: ${({ theme }) => theme.colors.cardBackground};
    color: ${({ theme }) => theme.colors.textPrimary};
    font-weight: bold;
  }

  & .MuiDataGrid-row:hover {
    background-color: ${({ theme }) => theme.colors.hoverBackground};
  }
`;

const ManageUsers = () => {
  const [search, setSearch] = useState("");
  const [rows, setRows] = useState([
    {
      id: 1,
      username: "johndoe",
      email: "johndoe@example.com",
      status: "Active",
      createdAt: "2025-01-01",
    },
    {
      id: 2,
      username: "janedoe",
      email: "janedoe@example.com",
      status: "Inactive",
      createdAt: "2025-01-02",
    },
    {
      id: 3,
      username: "richardroe",
      email: "richardroe@example.com",
      status: "Flagged",
      createdAt: "2025-01-03",
    },
  ]);

  const handleEdit = (id) => {
    console.log(`Edit user with ID: ${id}`);
    // Redirect to user edit page or open modal
  };

  const handleSendReset = (id) => {
    console.log(`Send password reset email to user ID: ${id}`);
    // Trigger backend API call for password reset
  };

  const handleFlag = (id) => {
    console.log(`Flag user with ID: ${id}`);
    // Trigger backend API call to flag the user
  };

  const handleDisable = (id) => {
    console.log(`Disable user with ID: ${id}`);
    // Trigger backend API call to disable the user
  };

  const filteredRows = rows.filter(
    (row) =>
      row.username.toLowerCase().includes(search.toLowerCase()) ||
      row.email.toLowerCase().includes(search.toLowerCase())
  );

  const columns = [
    { field: "id", headerName: "ID", width: 60 },
    { field: "username", headerName: "Username", width: 150 },
    { field: "email", headerName: "Email", width: 200 },
    { field: "status", headerName: "Status", width: 120 },
    { field: "createdAt", headerName: "Created At", width: 150 },
    {
      field: "actions",
      headerName: "Actions",
      width: 300,
      renderCell: (params) => (
        <div>
          <ActionButton onClick={() => handleEdit(params.row.id)}>
            <FaUserEdit /> Edit
          </ActionButton>
          <ActionButton onClick={() => handleSendReset(params.row.id)}>
            <FaEnvelope /> Reset Password
          </ActionButton>
          <ActionButton onClick={() => handleFlag(params.row.id)}>
            <FaFlag /> Flag
          </ActionButton>
          <ActionButton onClick={() => handleDisable(params.row.id)}>
            <FaBan /> Disable
          </ActionButton>
        </div>
      ),
    },
  ];

  return (
    <Container>
      <Header>
        <Title>Manage Users</Title>
        <SearchBar>
          <FaSearch />
          <SearchInput
            type="text"
            placeholder="Search by username or email"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </SearchBar>
      </Header>
      <StyledDataGrid
        rows={filteredRows}
        columns={columns}
        pageSize={5}
        rowsPerPageOptions={[5, 10, 20]}
        autoHeight
        disableSelectionOnClick
      />
    </Container>
  );
};

export default ManageUsers;
