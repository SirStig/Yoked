import React from "react";
import AdminDashboard from "./dashboard/AdminDashboard";
import ManageUsers from "./users/ManageUsers";
import ManageSubscriptions from "./subscriptions/ManageSubscriptions";
import ManageContent from "./content/ManageContent";
import ManagePayments from "./payments/ManagePayments";
import AdminReports from "./reports/AdminReports";
import ModerateCommunity from "./community/ModerateCommunity";

// Define custom routes
const customRoutes = [
  {
    key: "admin-dashboard",
    path: "/dashboard",
    element: <AdminDashboard />,
  },
  {
    key: "manage-users",
    path: "/users",
    element: <ManageUsers />,
  },
  {
    key: "manage-subscriptions",
    path: "/subscriptions",
    element: <ManageSubscriptions />,
  },
  {
    key: "manage-content",
    path: "/content",
    element: <ManageContent />,
  },
  {
    key: "manage-payments",
    path: "/payments",
    element: <ManagePayments />,
  },
  {
    key: "admin-reports",
    path: "/reports",
    element: <AdminReports />,
  },
  {
    key: "moderate-community",
    path: "/community",
    element: <ModerateCommunity />,
  },
];

export default customRoutes;
