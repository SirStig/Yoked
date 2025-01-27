import React, { useState } from "react";
import styled from "styled-components";
import { DataGrid } from "@mui/x-data-grid";
import { FaEdit, FaTrash, FaToggleOn, FaToggleOff } from "react-icons/fa";

const Container = styled.div`
  padding: 2rem;
  background-color: ${({ theme }) => theme.colors.background};
  color: ${({ theme }) => theme.colors.textPrimary};
`;

const Header = styled.h2`
  margin-bottom: 1.5rem;
  color: ${({ theme }) => theme.colors.primary};
  text-align: center;
`;

const FilterContainer = styled.div`
  display: flex;
  justify-content: space-between;
  margin-bottom: 1.5rem;
`;

const FilterButton = styled.button`
  margin: 0 0.5rem;
  padding: 0.4rem 1rem;
  color: white;
  background-color: ${({ theme }) => theme.colors.primary};
  border: none;
  border-radius: ${({ theme }) => theme.borderRadius};
  cursor: pointer;
  font-size: 0.9rem;

  &:hover {
    background-color: ${({ theme }) => theme.colors.primaryHover};
  }

  &:disabled {
    background-color: ${({ theme }) => theme.colors.disabled};
    cursor: not-allowed;
  }
`;

const ActionsContainer = styled.div`
  display: flex;
  justify-content: center;
  gap: 0.5rem;
`;

const ActionButton = styled.button`
  padding: 0.3rem 0.7rem;
  color: white;
  background-color: ${({ theme }) => theme.colors.primary};
  border: none;
  border-radius: ${({ theme }) => theme.borderRadius};
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.3rem;
  font-size: 0.8rem;

  &:hover {
    background-color: ${({ theme }) => theme.colors.primaryHover};
  }

  &:disabled {
    background-color: ${({ theme }) => theme.colors.disabled};
    cursor: not-allowed;
  }
`;

const ManageSubscriptions = () => {
  const [filter, setFilter] = useState("All");

  const columns = [
    { field: "id", headerName: "ID", width: 80 },
    { field: "name", headerName: "Name", width: 200 },
    { field: "price", headerName: "Price", width: 120 },
    { field: "status", headerName: "Status", width: 150 },
    { field: "createdAt", headerName: "Created At", width: 180 },
    {
      field: "actions",
      headerName: "Actions",
      width: 320,
      renderCell: (params) => (
        <ActionsContainer>
          <ActionButton onClick={() => handleEdit(params.row.id)}>
            <FaEdit /> Edit
          </ActionButton>
          {params.row.status === "Active" ? (
            <ActionButton onClick={() => handleDeactivate(params.row.id)}>
              <FaToggleOff /> Deactivate
            </ActionButton>
          ) : (
            <ActionButton onClick={() => handleActivate(params.row.id)}>
              <FaToggleOn /> Activate
            </ActionButton>
          )}
          <ActionButton onClick={() => handleDelete(params.row.id)}>
            <FaTrash /> Delete
          </ActionButton>
        </ActionsContainer>
      ),
    },
  ];

  const rows = [
    {
      id: 1,
      name: "Basic Plan",
      price: "$9.99",
      status: "Active",
      createdAt: "2025-01-01",
    },
    {
      id: 2,
      name: "Premium Plan",
      price: "$19.99",
      status: "Inactive",
      createdAt: "2025-01-02",
    },
  ];

  const handleEdit = (id) => {
    console.log(`Edit subscription with ID: ${id}`);
    // Redirect to subscription edit page or open modal
  };

  const handleDeactivate = (id) => {
    console.log(`Deactivate subscription with ID: ${id}`);
    // Trigger backend API call to deactivate the subscription
  };

  const handleActivate = (id) => {
    console.log(`Activate subscription with ID: ${id}`);
    // Trigger backend API call to activate the subscription
  };

  const handleDelete = (id) => {
    console.log(`Delete subscription with ID: ${id}`);
    // Trigger backend API call to delete the subscription
  };

  const handleFilterChange = (status) => {
    setFilter(status);
    console.log(`Filter set to: ${status}`);
    // Apply backend filtering or adjust frontend display
  };

  const filteredRows = rows.filter((row) => {
    if (filter === "All") return true;
    return row.status === filter;
  });

  return (
    <Container>
      <Header>Manage Subscriptions</Header>
      <FilterContainer>
        <div>
          <FilterButton onClick={() => handleFilterChange("All")}>All</FilterButton>
          <FilterButton onClick={() => handleFilterChange("Active")}>Active</FilterButton>
          <FilterButton onClick={() => handleFilterChange("Inactive")}>Inactive</FilterButton>
        </div>
      </FilterContainer>
      <DataGrid
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

export default ManageSubscriptions;
