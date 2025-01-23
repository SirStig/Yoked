import React from "react";
import { Admin, Resource, CustomRoutes } from "react-admin";
import {HashRouter, Route} from "react-router-dom";
import authProvider from "./authProvider";
import dataProvider from "./dataProvider";
import customRoutes from "./customRoutes";
import AdminDashboard from "./dashboard/AdminDashboard";
import ManageUsers from "./users/ManageUsers";
import ManageSubscriptions from "./subscriptions/ManageSubscriptions";
import ManageContent from "./content/ManageContent";
import ManagePayments from "./payments/ManagePayments";
import AdminReports from "./reports/AdminReports";
import ModerateCommunity from "./community/ModerateCommunity";

// Admin App Component
const AdminApp = () => {
  return (
    <HashRouter>
        <Admin
          dashboard={AdminDashboard}
          dataProvider={dataProvider}
          authProvider={authProvider}
          customRoutes={
            <CustomRoutes>
              {customRoutes.map((route) => (
                <Route key={route.key} path={route.path} element={route.element} />
              ))}
            </CustomRoutes>
          }
        >
          {/* Define resources for React Admin */}
          <Resource name="users" options={{ label: "Users" }} />
          <Resource name="subscriptions" options={{ label: "Subscriptions" }} />
          <Resource name="content" options={{ label: "Content" }} />
          <Resource name="payments" options={{ label: "Payments" }} />
          <Resource name="reports" options={{ label: "Reports" }} />
          <Resource name="community" options={{ label: "Community" }} />
        </Admin>
    </HashRouter>
  );
};

export default AdminApp;
