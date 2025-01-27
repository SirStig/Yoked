import React from "react";
import styled from "styled-components";
import {
  Line,
  Bar,
  Pie,
  Doughnut
} from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  PointElement,
  LineElement,
  ArcElement
} from "chart.js";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  PointElement,
  LineElement,
  ArcElement
);

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

const ChartContainer = styled.div`
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  gap: 2rem;
  margin-bottom: 2rem;
`;

const ChartWrapper = styled.div`
  flex: 1 1 calc(50% - 1rem);
  background-color: ${({ theme }) => theme.colors.cardBackground};
  border-radius: ${({ theme }) => theme.borderRadius};
  box-shadow: ${({ theme }) => theme.shadows.medium};
  padding: 1rem;
`;

const AdminReports = () => {
  // Example data
  const revenueData = {
    labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
    datasets: [
      {
        label: "Monthly Revenue ($)",
        data: [5000, 7000, 8000, 6000, 9000, 11000],
        backgroundColor: "rgba(75, 192, 192, 0.2)",
        borderColor: "rgba(75, 192, 192, 1)",
        borderWidth: 2,
      },
    ],
  };

  const userGrowthData = {
    labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
    datasets: [
      {
        label: "New Users",
        data: [200, 300, 400, 250, 450, 500],
        backgroundColor: "rgba(255, 99, 132, 0.2)",
        borderColor: "rgba(255, 99, 132, 1)",
        borderWidth: 2,
      },
    ],
  };

  const subscriptionPerformanceData = {
    labels: ["Basic", "Standard", "Premium"],
    datasets: [
      {
        label: "Active Subscriptions",
        data: [300, 500, 200],
        backgroundColor: ["#FF6384", "#36A2EB", "#FFCE56"],
      },
    ],
  };

  const refundData = {
    labels: ["Completed", "Refunded"],
    datasets: [
      {
        label: "Payment Status",
        data: [90, 10],
        backgroundColor: ["#4CAF50", "#F44336"],
      },
    ],
  };

  return (
    <Container>
      <Header>Admin Reports</Header>
      <ChartContainer>
        {/* Revenue Trend */}
        <ChartWrapper>
          <h3>Monthly Revenue</h3>
          <Line data={revenueData} options={{ responsive: true }} />
        </ChartWrapper>

        {/* User Growth Trend */}
        <ChartWrapper>
          <h3>New User Growth</h3>
          <Line data={userGrowthData} options={{ responsive: true }} />
        </ChartWrapper>

        {/* Subscription Performance */}
        <ChartWrapper>
          <h3>Subscription Performance</h3>
          <Pie data={subscriptionPerformanceData} options={{ responsive: true }} />
        </ChartWrapper>

        {/* Refund Breakdown */}
        <ChartWrapper>
          <h3>Refund Breakdown</h3>
          <Doughnut data={refundData} options={{ responsive: true }} />
        </ChartWrapper>
      </ChartContainer>

      {/* More Reports */}
      <ChartContainer>
        <ChartWrapper>
          <h3>Active vs Inactive Users</h3>
          <Bar
            data={{
              labels: ["Active", "Inactive"],
              datasets: [
                {
                  label: "User Status",
                  data: [1200, 300],
                  backgroundColor: ["#4CAF50", "#F44336"],
                },
              ],
            }}
            options={{ responsive: true }}
          />
        </ChartWrapper>

        <ChartWrapper>
          <h3>Failed Payments</h3>
          <Bar
            data={{
              labels: ["January", "February", "March", "April", "May"],
              datasets: [
                {
                  label: "Failed Payments",
                  data: [10, 5, 8, 3, 7],
                  backgroundColor: "rgba(255, 99, 132, 0.6)",
                },
              ],
            }}
            options={{ responsive: true }}
          />
        </ChartWrapper>
      </ChartContainer>
    </Container>
  );
};

export default AdminReports;