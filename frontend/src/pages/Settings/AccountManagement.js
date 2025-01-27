import React from 'react';
import { Box, Typography, Button } from '@mui/material';

const AccountManagement = () => {
  const handleResetPassword = () => {
    // Logic to reset the password
    console.log('Password reset initiated!');
  };

  const handleLogoutAllSessions = () => {
    // Logic to log out of all sessions
    console.log('Logged out of all sessions!');
  };

  const handleDeleteAccount = () => {
    // Logic to delete account
    console.log('Account deletion initiated!');
  };

  return (
    <Box>
      <Typography variant="h5" gutterBottom>
        Account Management
      </Typography>

      <Button variant="contained" color="primary" onClick={handleResetPassword} sx={{ mt: 2 }}>
        Reset Password
      </Button>

      <Button variant="contained" color="secondary" onClick={handleLogoutAllSessions} sx={{ mt: 2 }}>
        Logout of All Sessions
      </Button>

      <Button variant="contained" color="error" onClick={handleDeleteAccount} sx={{ mt: 2 }}>
        Delete Account
      </Button>
    </Box>
  );
};

export default AccountManagement;
