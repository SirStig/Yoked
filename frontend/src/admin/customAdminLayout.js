import React from "react";
import { Layout } from "react-admin";
import AdminSidebar from "./components/AdminSidebar";
import AdminTopBar from "./components/AdminTopBar";

const CustomAdminLayout = (props) => (
  <Layout
    {...props}
    menu={AdminSidebar} // Custom sidebar
    appBar={AdminTopBar} // Custom top bar
  />
);

export default CustomAdminLayout;
