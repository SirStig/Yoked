import React, { useState, useEffect } from "react";
import {
  Box,
  Typography,
  List,
  ListItem,
  ListItemText,
  Switch,
  Button,
  CircularProgress,
  TextField,
} from "@mui/material";
import { toast } from "react-toastify";
import {
  getNotificationPreferences,
  updateNotificationPreferences,
  updateSecuritySettings,
} from "../../api/settingsApi";

const SecurityNotifications = () => {
  const [loading, setLoading] = useState(true);
  const [mfaEnabled, setMfaEnabled] = useState(false);
  const [password, setPassword] = useState("");
  const [notificationPreferences, setNotificationPreferences] = useState({
    likes: true,
    comments: true,
    follows: true,
    direct_messages: true,
    subscriptions: true,
    marketing: true,
    reels_notifications: true,
    community_notifications: true,
    nutrition_notifications: true,
    workout_notifications: true,
  });

  useEffect(() => {
    const fetchSettings = async () => {
      try {
        const data = await getNotificationPreferences();
        setNotificationPreferences(data);
        setMfaEnabled(data.mfa_enabled);
      } catch (error) {
        toast.error("Failed to load security settings.");
      } finally {
        setLoading(false);
      }
    };

    fetchSettings();
  }, []);

  const handleToggleMFA = async (event) => {
    const newValue = event.target.checked;
    setMfaEnabled(newValue);
    try {
      await updateSecuritySettings({ mfa_enabled: newValue });
      toast.success(`MFA ${newValue ? "enabled" : "disabled"} successfully.`);
    } catch (error) {
      toast.error("Failed to update MFA settings.");
    }
  };

  const handleUpdatePassword = async () => {
    if (!password) return toast.error("Enter a new password.");
    try {
      await updateSecuritySettings({ password });
      toast.success("Password updated successfully.");
      setPassword("");
    } catch (error) {
      toast.error("Failed to update password.");
    }
  };

  const handleToggleNotification = async (event) => {
    const { name, checked } = event.target;
    setNotificationPreferences((prev) => ({ ...prev, [name]: checked }));

    try {
      await updateNotificationPreferences({ ...notificationPreferences, [name]: checked });
      toast.success("Notification preferences updated.");
    } catch (error) {
      toast.error("Failed to update notifications.");
    }
  };

  const formatNotificationLabel = (key) => {
    return key
      .replace(/_/g, " ") // Replace underscores with spaces
      .replace(/\b\w/g, (char) => char.toUpperCase()); // Capitalize first letter of each word
  };

  return (
    <Box>
      <Typography variant="h5" gutterBottom sx={{ color: "white" }}>
        Security & Notifications
      </Typography>

      {loading ? (
        <CircularProgress color="primary" />
      ) : (
        <>
          {/* Security Settings */}
          <Typography variant="h6" gutterBottom sx={{ mt: 3, color: "white" }}>
            Security Settings
          </Typography>
          <List>
            <ListItem>
              <ListItemText
                primary={<Typography sx={{ color: "white" }}>Enable Multi-Factor Authentication (MFA)</Typography>}
              />
              <Switch checked={mfaEnabled} onChange={handleToggleMFA} />
            </ListItem>

            <ListItem>
              <ListItemText
                primary={<Typography sx={{ color: "white" }}>Change Password</Typography>}
                secondary={<Typography sx={{ color: "white" }}>Enter a new password below</Typography>}
              />
            </ListItem>

            <ListItem>
              <TextField
                fullWidth
                type="password"
                variant="outlined"
                label="New Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                sx={{
                  "& .MuiInputBase-input": { color: "white" },
                  "& .MuiInputLabel-root": { color: "white" },
                  "& .MuiOutlinedInput-root": {
                    "& fieldset": { borderColor: "white" },
                    "&:hover fieldset": { borderColor: "primary.main" },
                    "&.Mui-focused fieldset": { borderColor: "primary.main" },
                  },
                }}
              />
            </ListItem>

            <ListItem>
              <Button variant="contained" color="primary" onClick={handleUpdatePassword} sx={{ mt: 2 }}>
                Update Password
              </Button>
            </ListItem>
          </List>

          {/* Notification Settings */}
          <Typography variant="h6" gutterBottom sx={{ mt: 3, color: "white" }}>
            Notification Settings
          </Typography>
          <List>
            {Object.keys(notificationPreferences).map((key) => (
              <ListItem key={key}>
                <ListItemText
                  primary={<Typography sx={{ color: "white" }}>{formatNotificationLabel(key)}</Typography>}
                />
                <Switch name={key} checked={notificationPreferences[key]} onChange={handleToggleNotification} />
              </ListItem>
            ))}
          </List>
        </>
      )}
    </Box>
  );
};

export default SecurityNotifications;
