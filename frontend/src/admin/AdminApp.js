import React from "react";
import { Admin, Resource, CustomRoutes } from "react-admin";
import { Route } from "react-router-dom";
import authProvider from "./authProvider";
import dataProvider from "./dataProvider";
import AdminDashboard from "./dashboard/AdminDashboard";
import ManageUsers from "./users/ManageUsers"; // Import your components
import ManageSubscriptions from "./subscriptions/ManageSubscriptions";
import ManagePayments from "./payments/ManagePayments";
import ManageContent from "./content/ManageContent";
import AdminEmail from "./emails/AdminEmail";
import AdminReports from "./reports/AdminReports";
import AdminSettings from "./settings/AdminSettings";
import AdminSupport from "./support/AdminSupport";
import CustomAdminLayout from "./customAdminLayout";
import { ThemeProvider } from "styled-components";
import { adminTheme } from "./styles/adminTheme";
import AdminGlobalStyles from "./styles/adminStyles";

const AdminApp = () => {
  return (
    <ThemeProvider theme={adminTheme}>
      <AdminGlobalStyles />
      <Admin
        dashboard={AdminDashboard}
        dataProvider={dataProvider}
        authProvider={authProvider}
        layout={CustomAdminLayout}
      >
        {/* Resources for React-Admin */}
        <Resource
          name="users"
          list={ManageUsers}
          options={{ label: "Manage Users" }}
        />
        <Resource
          name="subscriptions"
          list={ManageSubscriptions}
          options={{ label: "Manage Subscriptions" }}
        />
        <Resource
          name="payments"
          list={ManagePayments}
          options={{ label: "Manage Payments" }}
        />
        <Resource
          name="reports"
          list={AdminReports}
          options={{ label: "Reports" }}
        />
        <Resource
          name="content"
          list={ManageContent}
          options={{ label: "Manage Content" }}
        />
        <Resource
          name="emails"
          list={AdminEmail}
          options={{ label: "Manage Emails" }}
        />
        <Resource
          name="settings"
          list={AdminSettings}
          options={{ label: "Admin Settings" }}
        />
        <Resource
          name="support"
          list={AdminSupport}
          options={{ label: "Manage User Support" }}
        />
        {/* Custom Routes */}
        <CustomRoutes>
          <Route path="/custom-settings" element={<div>Settings Page</div>} />
          {/* Add additional custom routes if needed */}
        </CustomRoutes>
      </Admin>
    </ThemeProvider>
  );
};

export default AdminApp;
