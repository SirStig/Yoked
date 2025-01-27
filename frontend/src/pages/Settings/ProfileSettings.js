import React, { useState, useEffect } from "react";
import {
  Box,
  Typography,
  TextField,
  Button,
  Grid,
  Avatar,
  CircularProgress,
  Alert,
  MenuItem,
} from "@mui/material";
import { getProfile, updateProfile } from "../../api/userApi";

const ProfileSettings = () => {
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    name: "",
    age: "",
    weight: "",
    weight_unit: "kg",
    height_ft: "",
    height_in: "",
    height_cm: "",
    height_unit: "cm",
    avatar: "",
  });
  const [loading, setLoading] = useState(false);
  const [successMessage, setSuccessMessage] = useState("");
  const [errorMessage, setErrorMessage] = useState("");

  useEffect(() => {
    const fetchProfile = async () => {
      setLoading(true);
      try {
        const profile = await getProfile();
        setFormData({
          username: profile.username || "",
          email: profile.email || "",
          name: profile.full_name || "",
          age: profile.age || "",
          weight: profile.weight || "",
          weight_unit: profile.weight_unit || "kg",
          height_ft: profile.height_unit === "ft/in" ? Math.floor(profile.height / 30.48) : "",
          height_in: profile.height_unit === "ft/in" ? Math.round((profile.height % 30.48) / 2.54) : "",
          height_cm: profile.height_unit === "cm" ? profile.height : "",
          height_unit: profile.height_unit || "cm",
          avatar: profile.avatar || "/assets/default-avatar.png",
        });
      } catch (error) {
        setErrorMessage("Failed to load profile data.");
      } finally {
        setLoading(false);
      }
    };

    fetchProfile();
  }, []);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleAvatarUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      console.log("Selected avatar file:", file);
    }
  };

  const handleSaveChanges = async () => {
    setLoading(true);
    setSuccessMessage("");
    setErrorMessage("");
    try {
      const convertedFormData = { ...formData };
      if (formData.weight_unit === "lbs") {
        convertedFormData.weight = (formData.weight / 2.20462).toFixed(2);
      }
      if (formData.height_unit === "ft/in") {
        convertedFormData.height = (
          formData.height_ft * 30.48 +
          formData.height_in * 2.54
        ).toFixed(2);
      } else {
        convertedFormData.height = formData.height_cm;
      }

      await updateProfile(convertedFormData);
      setSuccessMessage("Profile updated successfully!");
    } catch (error) {
      setErrorMessage("Failed to save changes. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box sx={{ color: "white", mt: 4 }}>
      <Typography variant="h4" gutterBottom sx={{ fontWeight: "bold" }}>
        Profile Settings
      </Typography>

      {loading && <CircularProgress color="primary" />}
      {successMessage && <Alert severity="success">{successMessage}</Alert>}
      {errorMessage && <Alert severity="error">{errorMessage}</Alert>}

      <Box component="form" noValidate autoComplete="off" sx={{ mt: 3 }}>
        <Typography variant="h6" gutterBottom>
          Personal Information
        </Typography>
        <Grid container spacing={2}>
          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              label="Username"
              name="username"
              value={formData.username}
              onChange={handleInputChange}
              variant="outlined"
              disabled
              helperText="Username can only be changed once per year."
              sx={{
                input: { color: "white" },
                "& .MuiInputLabel-root": { color: "white" },
                "& .MuiOutlinedInput-root": {
                  "& fieldset": { borderColor: "white" },
                  "&:hover fieldset": { borderColor: "primary.main" },
                  "&.Mui-focused fieldset": { borderColor: "primary.main" },
                },
                "& .MuiFormHelperText-root": { color: "white" },
              }}
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              label="Email"
              name="email"
              value={formData.email}
              onChange={handleInputChange}
              variant="outlined"
              helperText="Changing your email requires MFA and re-verification."
              sx={{
                input: { color: "white" },
                "& .MuiInputLabel-root": { color: "white" },
                "& .MuiOutlinedInput-root": {
                  "& fieldset": { borderColor: "white" },
                  "&:hover fieldset": { borderColor: "primary.main" },
                  "&.Mui-focused fieldset": { borderColor: "primary.main" },
                },
                "& .MuiFormHelperText-root": { color: "white" },
              }}
            />
          </Grid>
          <Grid item xs={12}>
            <TextField
              fullWidth
              label="Full Name"
              name="name"
              value={formData.name}
              onChange={handleInputChange}
              variant="outlined"
              sx={{
                input: { color: "white" },
                "& .MuiInputLabel-root": { color: "white" },
                "& .MuiOutlinedInput-root": {
                  "& fieldset": { borderColor: "white" },
                  "&:hover fieldset": { borderColor: "primary.main" },
                  "&.Mui-focused fieldset": { borderColor: "primary.main" },
                },
              }}
            />
          </Grid>
        </Grid>

        <Typography variant="h6" gutterBottom sx={{ mt: 4 }}>
          Physical Metrics
        </Typography>
        <Grid container spacing={2}>
          <Grid item xs={12} sm={4}>
            <TextField
              fullWidth
              label="Age"
              name="age"
              value={formData.age}
              onChange={handleInputChange}
              variant="outlined"
              type="number"
              inputProps={{ step: 1 }}
              sx={{
                input: { color: "white" },
                "& .MuiInputLabel-root": { color: "white" },
                "& .MuiOutlinedInput-root": {
                  "& fieldset": { borderColor: "white" },
                  "&:hover fieldset": { borderColor: "primary.main" },
                  "&.Mui-focused fieldset": { borderColor: "primary.main" },
                },
              }}
            />
          </Grid>
          <Grid item xs={12} sm={4}>
            <TextField
              fullWidth
              label={`Weight (${formData.weight_unit})`}
              name="weight"
              value={formData.weight}
              onChange={handleInputChange}
              variant="outlined"
              type="text"
              sx={{
                input: { color: "white" },
                "& .MuiInputLabel-root": { color: "white" },
                "& .MuiOutlinedInput-root": {
                  "& fieldset": { borderColor: "white" },
                  "&:hover fieldset": { borderColor: "primary.main" },
                  "&.Mui-focused fieldset": { borderColor: "primary.main" },
                },
              }}
              InputProps={{
                endAdornment: (
                  <TextField
                    select
                    value={formData.weight_unit}
                    name="weight_unit"
                    onChange={handleInputChange}
                    variant="standard"
                    sx={{ color: "white", width: "100px" }}
                  >
                    <MenuItem value="kg">kg</MenuItem>
                    <MenuItem value="lbs">lbs</MenuItem>
                  </TextField>
                ),
              }}
            />
          </Grid>
          <Grid item xs={12} sm={4}>
            {formData.height_unit === "ft/in" ? (
              <Grid container spacing={1}>
                <Grid item xs={6}>
                  <TextField
                    fullWidth
                    label="Feet"
                    name="height_ft"
                    value={formData.height_ft}
                    onChange={handleInputChange}
                    variant="outlined"
                    type="number"
                    inputProps={{ step: 1 }}
                    sx={{
                      input: { color: "white" },
                      "& .MuiInputLabel-root": { color: "white" },
                      "& .MuiOutlinedInput-root": {
                        "& fieldset": { borderColor: "white" },
                        "&:hover fieldset": { borderColor: "primary.main" },
                        "&.Mui-focused fieldset": { borderColor: "primary.main" },
                      },
                    }}
                  />
                </Grid>
                <Grid item xs={6}>
                  <TextField
                    fullWidth
                    label="Inches"
                    name="height_in"
                    value={formData.height_in}
                    onChange={handleInputChange}
                    variant="outlined"
                    type="number"
                    inputProps={{ step: 1 }}
                    sx={{
                      input: { color: "white" },
                      "& .MuiInputLabel-root": { color: "white" },
                      "& .MuiOutlinedInput-root": {
                        "& fieldset": { borderColor: "white" },
                        "&:hover fieldset": { borderColor: "primary.main" },
                        "&.Mui-focused fieldset": { borderColor: "primary.main" },
                      },
                    }}
                  />
                </Grid>
              </Grid>
            ) : (
              <TextField
                fullWidth
                label="Height (cm)"
                name="height_cm"
                value={formData.height_cm}
                onChange={handleInputChange}
                variant="outlined"
                type="number"
                inputProps={{ step: 1 }}
                sx={{
                  input: { color: "white" },
                  "& .MuiInputLabel-root": { color: "white" },
                  "& .MuiOutlinedInput-root": {
                    "& fieldset": { borderColor: "white" },
                    "&:hover fieldset": { borderColor: "primary.main" },
                    "&.Mui-focused fieldset": { borderColor: "primary.main" },
                  },
                }}
              />
            )}
          </Grid>
        </Grid>

        <Typography variant="h6" gutterBottom sx={{ mt: 4 }}>
          Avatar
        </Typography>
        <Grid container alignItems="center" spacing={2}>
          <Grid item>
            <Avatar
              src={formData.avatar}
              alt="User Avatar"
              sx={{ width: 100, height: 100 }}
            />
          </Grid>
          <Grid item>
            <Button
              variant="contained"
              component="label"
              sx={{
                bgcolor: "primary.main",
                "&:hover": { bgcolor: "primaryHover" },
              }}
            >
              Upload Avatar
              <input
                type="file"
                hidden
                accept="image/*"
                onChange={handleAvatarUpload}
              />
            </Button>
          </Grid>
        </Grid>

        <Button
          variant="contained"
          color="primary"
          onClick={handleSaveChanges}
          sx={{ mt: 4 }}
        >
          Save Changes
        </Button>
      </Box>
    </Box>
  );
};

export default ProfileSettings;
