import React, { useState, useEffect, useContext } from "react";
import {
  Box,
  Typography,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  List,
  ListItem,
  ListItemText,
  IconButton,
  CircularProgress,
  MenuItem,
  Select,
} from "@mui/material";
import { logoutAllSessions } from "../../api/authApi";
import { deleteAccount } from "../../api/userApi";
import { getUserSessions, revokeSession } from "../../api/settingsApi";
import { AuthContext } from "../../contexts/AuthContext";
import { toast } from "react-toastify";
import { MdLogout } from "react-icons/md";

const AccountManagement = () => {
  const [openDeleteConfirm, setOpenDeleteConfirm] = useState(false);
  const [password, setPassword] = useState("");
  const [sessions, setSessions] = useState([]);
  const [loadingSessions, setLoadingSessions] = useState(true);
  const [filter, setFilter] = useState("all"); // Default filter
  const { logout } = useContext(AuthContext);

  const currentSessionToken = localStorage.getItem("token");

  useEffect(() => {
    const fetchSessions = async () => {
      try {
        const sessionData = await getUserSessions();

        // Convert timestamps and check if it's the current device
        const processedSessions = sessionData
          .map((session) => ({
            ...session,
            last_activity: convertToUserTime(session.last_activity),
            expires_at: convertToUserTime(session.expires_at),
            isCurrentDevice: session.token === currentSessionToken,
          }))
          .sort((a, b) => new Date(b.last_activity) - new Date(a.last_activity)); // Sort by most recent first

        setSessions(processedSessions);
      } catch (error) {
        toast.error("Failed to load sessions.");
      } finally {
        setLoadingSessions(false);
      }
    };

    fetchSessions();
  }, []);

  const convertToUserTime = (utcTimestamp) => {
    if (!utcTimestamp) return "Unknown";
    const date = new Date(utcTimestamp + "Z");
    return date.toLocaleString();
  };

  const handleLogoutAllSessions = async () => {
    try {
      await logoutAllSessions();
      setSessions([]);
      toast.success("Logged out from all devices successfully.");
    } catch (error) {
      toast.error("Failed to log out from all devices.");
    }
  };

  const handleLogoutSession = async (sessionId) => {
    try {
      await revokeSession(sessionId);
      setSessions(sessions.filter((session) => session.session_id !== sessionId));
      toast.success("Session logged out successfully.");
    } catch (error) {
      toast.error("Failed to log out session.");
    }
  };

  const handleDeleteAccount = async () => {
    try {
      await deleteAccount(password);
      logout();
      toast.success("Account deleted successfully.");
    } catch (error) {
      toast.error("Failed to delete account.");
    } finally {
      setOpenDeleteConfirm(false);
    }
  };

  const filteredSessions = sessions.filter((session) => {
    if (filter === "all") return true;
    if (filter === "active") return session.is_active;
    if (filter === "mobile") return session.device_type === "Mobile";
    if (filter === "desktop") return session.device_type === "Desktop";
    return true;
  });

  return (
    <Box>
      <Typography variant="h4" gutterBottom sx={{ color: "white" }}>
        Account Management
      </Typography>

      {/* Session Filters */}
      <Box sx={{ display: "flex", alignItems: "center", mb: 2 }}>
        <Typography sx={{ color: "white", mr: 2 }}>Filter Sessions:</Typography>
        <Select
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
          sx={{
            color: "white",
            backgroundColor: "rgba(255, 255, 255, 0.1)",
            "& .MuiInputBase-input": { color: "white" },
          }}
        >
          <MenuItem value="all">All Sessions</MenuItem>
          <MenuItem value="active">Active Sessions</MenuItem>
          <MenuItem value="mobile">Mobile Devices</MenuItem>
          <MenuItem value="desktop">Desktop Devices</MenuItem>
        </Select>
      </Box>

      {/* List of Active Sessions */}
      <Typography variant="h6" gutterBottom sx={{ mt: 2, color: "white" }}>
        Active Sessions
      </Typography>
      {loadingSessions ? (
        <CircularProgress color="primary" />
      ) : filteredSessions.length > 0 ? (
        <List>
          {filteredSessions.map((session) => (
            <ListItem
              key={session.session_id}
              sx={{
                backgroundColor: session.isCurrentDevice
                  ? "rgba(0, 255, 0, 0.2)"
                  : "rgba(255, 255, 255, 0.1)",
                borderRadius: 2,
                mb: 1,
              }}
            >
              <ListItemText
                primary={`${session.device_type} (${session.browser}) ${
                  session.isCurrentDevice ? "(Current Device)" : ""
                }`}
                secondary={`IP: ${session.ip_address} - Location: ${session.location} - Last Active: ${session.last_activity} - Expires: ${session.expires_at}`}
                sx={{ color: "white" }}
              />
              {!session.isCurrentDevice && (
                <IconButton
                  onClick={() => handleLogoutSession(session.session_id)}
                  color="error"
                >
                  <MdLogout />
                </IconButton>
              )}
            </ListItem>
          ))}
        </List>
      ) : (
        <Typography sx={{ color: "white" }}>No active sessions found.</Typography>
      )}

      {/* Logout All Sessions Button */}
      <Button
        variant="contained"
        color="secondary"
        onClick={handleLogoutAllSessions}
        sx={{
          mt: 2,
          backgroundColor: "secondary.main",
          color: "white",
          "&:hover": { backgroundColor: "secondary.dark" },
        }}
      >
        Logout of All Sessions
      </Button>

      {/* Delete Account Button */}
      <Button
        variant="contained"
        color="error"
        onClick={() => setOpenDeleteConfirm(true)}
        sx={{
          mt: 2,
          ml: 2,
          backgroundColor: "error.main",
          color: "white",
          "&:hover": { backgroundColor: "error.dark" },
        }}
      >
        Delete Account
      </Button>

      {/* Confirm Account Deletion Dialog */}
      <Dialog
        open={openDeleteConfirm}
        onClose={() => setOpenDeleteConfirm(false)}
        PaperProps={{ style: { backgroundColor: "rgba(0,0,0,0.9)", color: "white" } }}
      >
        <DialogTitle sx={{ color: "white" }}>Confirm Account Deletion</DialogTitle>
        <DialogContent>
          <TextField
            fullWidth
            type="password"
            label="Enter Password"
            variant="outlined"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            sx={{
              "& .MuiInputBase-input": { color: "white" },
              "& .MuiInputLabel-root": { color: "white" },
              "& .MuiOutlinedInput-root": {
                "& fieldset": { borderColor: "white" },
              },
            }}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenDeleteConfirm(false)} sx={{ color: "white" }}>
            Cancel
          </Button>
          <Button onClick={handleDeleteAccount} color="error" sx={{ color: "white" }}>
            Delete
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default AccountManagement;
