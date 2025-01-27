import React from 'react';
import { Box, Typography, Button, List, ListItem, ListItemText } from '@mui/material';

const SubscriptionManagement = () => {
  const handleCancelSubscription = () => {
    // Logic to cancel subscription
    console.log('Subscription canceled!');
  };

  return (
    <Box>
      <Typography variant="h5" gutterBottom>
        Subscription Management
      </Typography>

      <List>
        <ListItem>
          <ListItemText primary="Current Plan" secondary="Elite Plan ($29.99/month)" />
        </ListItem>
        <ListItem>
          <ListItemText primary="Next Billing Date" secondary="2025-02-15" />
        </ListItem>
      </List>

      <Button variant="contained" color="error" onClick={handleCancelSubscription} sx={{ mt: 2 }}>
        Cancel Subscription
      </Button>
    </Box>
  );
};

export default SubscriptionManagement;
