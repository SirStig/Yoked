import React, { useState } from 'react';
import { Box, Typography, Grid, List, ListItem, ListItemButton, ListItemIcon, ListItemText, Divider } from '@mui/material';
import { motion } from 'framer-motion';
import ProfileSettings from './ProfileSettings';
import SubscriptionManagement from './SubscriptionManagement';
import AccountManagement from './AccountManagement';
import SecurityNotifications from './SecurityNotifications';
import { FaUser, FaDollarSign, FaLock, FaBell } from 'react-icons/fa';

function Settings() {
  const [activeTab, setActiveTab] = useState(0);

  const tabs = [
    { label: 'Profile Settings', icon: <FaUser />, component: <ProfileSettings /> },
    { label: 'Subscription Management', icon: <FaDollarSign />, component: <SubscriptionManagement /> },
    { label: 'Account Management', icon: <FaLock />, component: <AccountManagement /> },
    { label: 'Security & Notifications', icon: <FaBell />, component: <SecurityNotifications /> },
  ];

  const handleTabChange = (index) => {
    setActiveTab(index);
  };

  return (
    <Box sx={{ display: 'flex', height: '100vh', p: 4, gap: 4 }}>
      {/* Sidebar Navigation */}
      <Box
        sx={{
          minWidth: 250,
          borderRadius: 3,
          p: 2,
        }}
      >
        <Typography variant="h6" gutterBottom>
          Settings
        </Typography>
        <Divider sx={{ mb: 2 }} />
        <List>
          {tabs.map((tab, index) => (
            <ListItem key={index} disablePadding>
              <ListItemButton
                selected={activeTab === index}
                onClick={() => handleTabChange(index)}
                sx={{
                  borderRadius: 2,
                  mb: 1,
                  '&.Mui-selected': {
                    color: 'primary.main',
                    fontWeight: 'bold',
                  },
                }}
              >
                <ListItemIcon sx={{ color: 'white' }}>
                  {tab.icon}
                </ListItemIcon>
                <ListItemText primary={tab.label} />
              </ListItemButton>
            </ListItem>
          ))}
        </List>
      </Box>

      {/* Content Area */}
      <Box
        sx={{
          flex: 1,
          borderRadius: 3,
          p: 3,
          overflowY: 'auto',
        }}
      >
        <motion.div
          key={activeTab}
          initial={{ opacity: 0, x: 50 }}
          animate={{ opacity: 1, x: 0 }}
          exit={{ opacity: 0, x: -50 }}
          transition={{ duration: 0.5 }}
        >
          {tabs[activeTab].component}
        </motion.div>
      </Box>
    </Box>
  );
}

export default Settings;
