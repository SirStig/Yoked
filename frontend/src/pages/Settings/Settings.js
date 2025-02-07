import React, { useState, useEffect } from "react";
import {
  Box,
  Typography,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Divider,
  CircularProgress,
} from "@mui/material";
import { motion } from "framer-motion";
import ProfileSettings from "./ProfileSettings";
import SubscriptionManagement from "./SubscriptionManagement";
import AccountManagement from "./AccountManagement";
import SecurityNotifications from "./SecurityNotifications";
import { FaUser, FaDollarSign, FaLock, FaBell, FaVideo, FaDumbbell } from "react-icons/fa";
import { getNotificationPreferences, getSubscriptionDetails } from "../../api/settingsApi";
import { toast } from "react-toastify";

function Settings() {
  const [activeTab, setActiveTab] = useState(0);
  const [loading, setLoading] = useState(true);
  const [profile, setProfile] = useState({});
  const [security, setSecurity] = useState({});
  const [notifications, setNotifications] = useState({});
  const [subscription, setSubscription] = useState({});

  useEffect(() => {
    async function fetchSettings() {
      try {
        const notificationData = await getNotificationPreferences();
        const subscriptionData = await getSubscriptionDetails();

        setNotifications(notificationData);
        setSubscription(subscriptionData);
      } catch (error) {
        toast.error("Failed to load settings.");
      } finally {
        setLoading(false);
      }
    }

    fetchSettings();
  }, []);

  const tabs = [
    { label: "Profile Settings", icon: <FaUser />, component: <ProfileSettings profile={profile} setProfile={setProfile} /> },
    { label: "Subscription Management", icon: <FaDollarSign />, component: <SubscriptionManagement subscription={subscription} setSubscription={setSubscription} /> },
    { label: "Account Management", icon: <FaLock />, component: <AccountManagement /> },
    { label: "Security & Notifications", icon: <FaBell />, component: <SecurityNotifications security={security} setSecurity={setSecurity} notifications={notifications} setNotifications={setNotifications} /> },
  ];

  const handleTabChange = (index) => {
    setActiveTab(index);
  };

  return (
    <Box sx={{ display: "flex", height: "100vh", p: 4, gap: 4 }}>
      {/* Sidebar Navigation */}
      <Box sx={{ minWidth: 250, borderRadius: 3, p: 2 }}>
        <Typography variant="h6" gutterBottom sx={{ color: "white" }}>
          Settings
        </Typography>
        <Divider sx={{ mb: 2, backgroundColor: "white" }} />
        <List>
          {tabs.map((tab, index) => (
            <ListItem key={index} disablePadding>
              <ListItemButton
                selected={activeTab === index}
                onClick={() => handleTabChange(index)}
                sx={{
                  borderRadius: 2,
                  mb: 1,
                  color: "white",
                  "&.Mui-selected": {
                    backgroundColor: "rgba(255, 255, 255, 0.1)",
                    fontWeight: "bold",
                  },
                }}
              >
                <ListItemIcon sx={{ color: "white" }}>{tab.icon}</ListItemIcon>
                <ListItemText primary={tab.label} sx={{ color: "white" }} />
              </ListItemButton>
            </ListItem>
          ))}
        </List>
      </Box>

      {/* Content Area */}
      <Box sx={{ flex: 1, borderRadius: 3, p: 3, overflowY: "auto", color: "white" }}>
        {loading ? (
          <CircularProgress color="primary" />
        ) : (
          <motion.div
            key={activeTab}
            initial={{ opacity: 0, x: 50 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -50 }}
            transition={{ duration: 0.5 }}
          >
            {tabs[activeTab].component}
          </motion.div>
        )}
      </Box>
    </Box>
  );
}

export default Settings;
