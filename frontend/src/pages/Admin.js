import React from "react";
import { Admin, Resource } from "react-admin";
import dataProvider from "../admin/dataProvider";
import authProvider from "../admin/authProvider";
import UserList from "../admin/resources/users";
import WorkoutList from "../admin/resources/workouts";
import NutritionList from "../admin/resources/nutrition";

const AdminApp = () => (
    <Admin dataProvider={dataProvider} authProvider={authProvider}>
        <Resource name="users" list={UserList} />
        <Resource name="workouts" list={WorkoutList} />
        <Resource name="nutrition" list={NutritionList} />
    </Admin>
);

export default AdminApp;
