import React from "react";
import ManageUsers from "./users/ManageUsers";
import ManageSubscriptions from "./subscriptions/ManageSubscriptions";
import ManagePayments from "./payments/ManagePayments";
import AdminReports from "./reports/AdminReports";
import AdminEmail from "./emails/AdminEmail";
import AdminSettings from "./settings/AdminSettings";
import AdminSupport from "./support/AdminSupport";


// Define custom routes with `/admin` prefix
const customRoutes = [
  {
    key: "manage-users",
    path: "/admin/users",
    element: <ManageUsers />,
  },
  {
    key: "manage-subscriptions",
    path: "/admin/subscriptions",
    element: <ManageSubscriptions />,
  },
  {
    key: "manage-payments",
    path: "/admin/payments",
    element: <ManagePayments />,
  },
  {
    key: "admin-reports",
    path: "/admin/reports",
    element: <AdminReports />,
  },
  {
    key: "admin-email",
    path: "/admin/emails",
    element: <AdminEmail />,
  },
  {
    key: "admin-settings",
    path: "/admin/settings",
    element: <AdminSettings />,
  },
  {
    key: "admin-support",
    path: "/admin/support",
    element: <AdminSupport />,
  },
];

export default customRoutes;
