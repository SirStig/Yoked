import React from "react";
import styled from "styled-components";

// Styled Components
const TableContainer = styled.div`
  width: 100%;
  overflow-x: auto;
  background-color: ${({ theme }) => theme.colors.cardBackground};
  padding: 1rem;
  border-radius: ${({ theme }) => theme.borderRadius};
  box-shadow: ${({ theme }) => theme.shadows.medium};
`;

const Table = styled.table`
  width: 100%;
  border-collapse: collapse;

  th,
  td {
    padding: 0.75rem;
    text-align: left;
    border-bottom: 1px solid ${({ theme }) => theme.colors.border};
  }

  th {
    background-color: ${({ theme }) => theme.colors.primary};
    color: ${({ theme }) => theme.colors.textSecondary};
    font-weight: bold;
  }

  tr:hover {
    background-color: ${({ theme }) => theme.colors.hoverBackground};
  }
`;

const ActionsContainer = styled.div`
  display: flex;
  gap: 0.5rem;

  button {
    background-color: ${({ theme }) => theme.colors.primary};
    color: ${({ theme }) => theme.colors.textSecondary};
    border: none;
    padding: 0.5rem 1rem;
    border-radius: ${({ theme }) => theme.borderRadius};
    cursor: pointer;
    transition: background-color 0.3s ease;

    &:hover {
      background-color: ${({ theme }) => theme.colors.primaryHover};
    }
  }
`;

// AdminTable Component
const AdminTable = ({ columns, data, actions }) => {
  return (
    <TableContainer>
      <Table>
        <thead>
          <tr>
            {columns.map((column) => (
              <th key={column.key}>{column.title}</th>
            ))}
            {actions && <th>Actions</th>}
          </tr>
        </thead>
        <tbody>
          {data.map((row, index) => (
            <tr key={index}>
              {columns.map((column) => (
                <td key={column.key}>{row[column.key]}</td>
              ))}
              {actions && (
                <td>
                  <ActionsContainer>
                    {actions.map((action, i) => (
                      <button key={i} onClick={() => action.onClick(row)}>
                        {action.label}
                      </button>
                    ))}
                  </ActionsContainer>
                </td>
              )}
            </tr>
          ))}
        </tbody>
      </Table>
    </TableContainer>
  );
};

export default AdminTable;
