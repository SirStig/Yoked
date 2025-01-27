import React from "react";
import styled from "styled-components";
import { Bar, Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  Tooltip,
  Legend,
} from "chart.js";

// Register chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  Tooltip,
  Legend
);

const DashboardContainer = styled.div`
  padding: 2rem;
  background-color: ${({ theme }) => theme.colors.background};
  color: ${({ theme }) => theme.colors.textPrimary};
`;

const SectionHeader = styled.h2`
  margin: 2rem 0 1rem;
  font-size: 1.5rem;
  color: ${({ theme }) => theme.colors.primary};
`;

const Grid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
`;

const Card = styled.div`
  background-color: ${({ theme }) => theme.colors.cardBackground};
  border-radius: ${({ theme }) => theme.borderRadius};
  padding: 1rem;
  box-shadow: ${({ theme }) => theme.shadows.medium};
`;

const ChartContainer = styled.div`
  margin-top: 2rem;
  background-color: ${({ theme }) => theme.colors.cardBackground};
  padding: 2rem;
  border-radius: ${({ theme }) => theme.borderRadius};
  box-shadow: ${({ theme }) => theme.shadows.medium};
`;

const QuickActions = styled.div`
  margin-top: 2rem;
`;

const QuickActionButton = styled.button`
  padding: 1rem;
  margin-right: 1rem;
  font-size: 1rem;
  color: white;
  background-color: ${({ theme }) => theme.colors.primary};
  border: none;
  border-radius: ${({ theme }) => theme.borderRadius};
  cursor: pointer;

  &:hover {
    background-color: ${({ theme }) => theme.colors.primaryHover};
  }
`;

const AdminDashboard = () => {
  // Mock data for charts and metrics
  const userGrowthData = {
    labels: ["Jan", "Feb", "Mar", "Apr", "May"],
    datasets: [
      {
        label: "User Growth",
        data: [200, 300, 500, 700, 1000],
        backgroundColor: "#4CAF50",
      },
    ],
  };

  const revenueTrendData = {
    labels: ["Jan", "Feb", "Mar", "Apr", "May"],
    datasets: [
      {
        label: "Revenue",
        data: [5000, 7000, 8000, 10000, 12000],
        borderColor: "#4CAF50",
        borderWidth: 2,
        fill: false,
      },
    ],
  };

  return (
    <DashboardContainer>
      <SectionHeader>Admin Dashboard</SectionHeader>

      {/* Summary Metrics */}
      <Grid>
        <Card>
          <h3>Total Users</h3>
          <p>1,200</p>
        </Card>
        <Card>
          <h3>Active Users</h3>
          <p>950</p>
        </Card>
        <Card>
          <h3>Inactive Users</h3>
          <p>250</p>
        </Card>
        <Card>
          <h3>New Users (Last 7 Days)</h3>
          <p>50</p>
        </Card>
        <Card>
          <h3>Active Subscriptions</h3>
          <p>850</p>
        </Card>
        <Card>
          <h3>Pending Payments</h3>
          <p>10</p>
        </Card>
      </Grid>

      {/* Charts Section */}
      <SectionHeader>Trends</SectionHeader>
      <ChartContainer>
        <h3>User Growth Trend</h3>
        <Line data={userGrowthData} />
      </ChartContainer>
      <ChartContainer>
        <h3>Revenue Trend</h3>
        <Line data={revenueTrendData} />
      </ChartContainer>

      {/* Quick Actions */}
      <SectionHeader>Quick Actions</SectionHeader>
      <QuickActions>
        <QuickActionButton>Create New Subscription</QuickActionButton>
        <QuickActionButton>Send Bulk Emails</QuickActionButton>
        <QuickActionButton>View Recent Payments</QuickActionButton>
      </QuickActions>
    </DashboardContainer>
  );
};

export default AdminDashboard;
