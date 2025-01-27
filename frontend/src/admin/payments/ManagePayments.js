import React, { useState } from "react";
import styled from "styled-components";
import { DataGrid } from "@mui/x-data-grid";
import { FaSearch, FaSyncAlt, FaReceipt, FaUndoAlt } from "react-icons/fa";

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
  flex-wrap: wrap;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
`;

const SearchContainer = styled.div`
  display: flex;
  gap: 0.5rem;
  align-items: center;
`;

const SearchInput = styled.input`
  padding: 0.5rem;
  border: 1px solid ${({ theme }) => theme.colors.border};
  border-radius: ${({ theme }) => theme.borderRadius};
  width: 250px;
  font-size: 1rem;

  &:focus {
    outline: none;
    border-color: ${({ theme }) => theme.colors.primary};
  }
`;

const ActionButton = styled.button`
  margin: 0.2rem;
  padding: 0.5rem 1rem;
  color: white;
  background-color: ${({ theme }) => theme.colors.primary};
  border: none;
  border-radius: ${({ theme }) => theme.borderRadius};
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.3rem;
  font-size: 0.9rem;
  white-space: nowrap;

  &:hover {
    background-color: ${({ theme }) => theme.colors.primaryHover};
  }

  &:disabled {
    background-color: ${({ theme }) => theme.colors.disabled};
    cursor: not-allowed;
  }
`;

const ManagePayments = () => {
  const [searchQuery, setSearchQuery] = useState("");
  const [refreshing, setRefreshing] = useState(false);
  const [filter, setFilter] = useState("All");

  const columns = [
    { field: "id", headerName: "ID", width: 80 },
    { field: "user", headerName: "User", width: 180 },
    { field: "amount", headerName: "Amount", width: 100 },
    { field: "status", headerName: "Status", width: 140 },
    { field: "date", headerName: "Date", width: 180 },
    {
      field: "actions",
      headerName: "Actions",
      width: 300,
      renderCell: (params) => (
        <div style={{ display: "flex", justifyContent: "space-between", width: "100%" }}>
          <ActionButton onClick={() => handleRefund(params.row.id)}>
            <FaUndoAlt /> Refund
          </ActionButton>
          <ActionButton onClick={() => handleViewReceipt(params.row.id)}>
            <FaReceipt /> View Receipt
          </ActionButton>
        </div>
      ),
    },
  ];

  const rows = [
    {
      id: 1,
      user: "John Doe",
      amount: "$99.99",
      status: "Completed",
      date: "2025-01-01",
    },
    {
      id: 2,
      user: "Jane Smith",
      amount: "$49.99",
      status: "Pending",
      date: "2025-01-02",
    },
  ];

  const handleRefund = (id) => {
    console.log(`Refund payment with ID: ${id}`);
    // Trigger backend API call for refund
  };

  const handleViewReceipt = (id) => {
    console.log(`View receipt for payment ID: ${id}`);
    // Redirect to or open a modal with receipt details
  };

  const handleSearch = (e) => {
    setSearchQuery(e.target.value);
  };

  const handleRefresh = () => {
    setRefreshing(true);
    console.log("Refreshing payment data...");
    // Trigger backend API call to refresh data
    setTimeout(() => setRefreshing(false), 1000); // Simulate refresh delay
  };

  const handleFilterChange = (status) => {
    setFilter(status);
    console.log(`Filter set to: ${status}`);
  };

  const filteredRows = rows
    .filter((row) => {
      if (filter === "All") return true;
      return row.status === filter;
    })
    .filter((row) => row.user.toLowerCase().includes(searchQuery.toLowerCase()));

  return (
    <Container>
      <Header>Manage Payments</Header>
      <FilterContainer>
        <div>
          <ActionButton onClick={() => handleFilterChange("All")}>All</ActionButton>
          <ActionButton onClick={() => handleFilterChange("Completed")}>Completed</ActionButton>
          <ActionButton onClick={() => handleFilterChange("Pending")}>Pending</ActionButton>
        </div>
        <SearchContainer>
          <SearchInput
            type="text"
            placeholder="Search by user..."
            value={searchQuery}
            onChange={handleSearch}
          />
          <ActionButton onClick={handleRefresh} disabled={refreshing}>
            <FaSyncAlt /> {refreshing ? "Refreshing..." : "Refresh"}
          </ActionButton>
        </SearchContainer>
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

export default ManagePayments;
