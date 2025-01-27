import React from 'react';
import { Box, Typography, Button, List, ListItem, ListItemText, Switch } from '@mui/material';

const SecurityNotifications = () => {
  const handleToggleMFA = (event) => {
    // Logic to toggle MFA
    console.log(`MFA toggled: ${event.target.checked}`);
  };

  return (
    <Box>
      <Typography variant="h5" gutterBottom>
        Security & Notifications
      </Typography>

      <List>
        <ListItem>
          <ListItemText primary="Enable Multi-Factor Authentication (MFA)" />
          <Switch onChange={handleToggleMFA} />
        </ListItem>
        <ListItem>
          <ListItemText primary="Receive Email Notifications" secondary="Subscription reminders, promotions, etc." />
          <Switch defaultChecked />
        </ListItem>
      </List>

      <Typography variant="h6" gutterBottom sx={{ mt: 3 }}>
        Recent Security Events
      </Typography>

      <List>
        <ListItem>
          <ListItemText primary="Login from new device" secondary="2025-01-24 14:23" />
        </ListItem>
        <ListItem>
          <ListItemText primary="Password changed" secondary="2025-01-22 09:47" />
        </ListItem>
      </List>
    </Box>
  );
};

export default SecurityNotifications;
