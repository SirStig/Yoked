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
import { updateProfileSettings } from "../../api/settingsApi";
import { getProfile } from "../../api/userApi";

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

        const heightUnit = profile.height_unit === "ft" ? "ft/in" : "cm"; // Ensure correct unit is assigned
        const heightFt = heightUnit === "ft/in" ? Math.floor(profile.height / 30.48) : "";
        const heightIn = heightUnit === "ft/in" ? Math.round((profile.height % 30.48) / 2.54) : "";
        const heightCm = heightUnit === "cm" ? profile.height : "";

        setFormData({
          username: profile.username || "",
          email: profile.email || "",
          name: profile.full_name || "",
          age: profile.age || "",
          weight: profile.weight_unit === "lbs"
            ? Math.round(profile.weight * 2.20462)
            : profile.weight || "",
          weight_unit: profile.weight_unit || "kg",
          height_ft: heightFt,
          height_in: heightIn,
          height_cm: heightCm,
          height_unit: heightUnit, // Set the correct unit automatically
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

  // Toggle between kg and lbs
  const handleWeightUnitChange = (e) => {
    const newUnit = e.target.value;
    setFormData((prev) => ({
      ...prev,
      weight_unit: newUnit,
      weight: newUnit === "kg"
        ? Math.round(prev.weight / 2.20462)
        : Math.round(prev.weight * 2.20462),
    }));
  };

  // Toggle between cm and ft/in
  const handleHeightUnitChange = (e) => {
    const newUnit = e.target.value;
    setFormData((prev) => {
      if (newUnit === "ft/in") {
        return {
          ...prev,
          height_unit: "ft/in",
          height_ft: Math.floor(prev.height_cm / 30.48),
          height_in: Math.round((prev.height_cm % 30.48) / 2.54),
          height_cm: "",
        };
      } else {
        return {
          ...prev,
          height_unit: "cm",
          height_cm: Math.round(prev.height_ft * 30.48 + prev.height_in * 2.54),
          height_ft: "",
          height_in: "",
        };
      }
    });
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

      await updateProfileSettings(convertedFormData);
      setSuccessMessage("Profile updated successfully!");
    } catch (error) {
      setErrorMessage("Failed to save changes. Please try again.");
    } finally {
      setLoading(false);
    }
  };
  return (
      <Box sx={{color: "white", mt: 4}}>
        <Typography variant="h4" gutterBottom sx={{fontWeight: "bold"}}>
          Profile Settings
        </Typography>

        {loading && <CircularProgress color="primary"/>}
        {successMessage && <Alert severity="success">{successMessage}</Alert>}
        {errorMessage && <Alert severity="error">{errorMessage}</Alert>}

        <Box component="form" noValidate autoComplete="off" sx={{mt: 3}}>
          {/* Personal Information */}
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
                  helperText="Username can only be changed once per year."
                  sx={{
                    input: {color: "white"},
                    "& .MuiInputLabel-root": {color: "white"},
                    "& .MuiOutlinedInput-root": {
                      "& fieldset": {borderColor: "white"},
                      "&:hover fieldset": {borderColor: "primary.main"},
                      "&.Mui-focused fieldset": {borderColor: "primary.main"},
                    },
                    "& .MuiFormHelperText-root": {color: "white"},
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
                    input: {color: "white"},
                    "& .MuiInputLabel-root": {color: "white"},
                    "& .MuiOutlinedInput-root": {
                      "& fieldset": {borderColor: "white"},
                      "&:hover fieldset": {borderColor: "primary.main"},
                      "&.Mui-focused fieldset": {borderColor: "primary.main"},
                    },
                    "& .MuiFormHelperText-root": {color: "white"},
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
                    input: {color: "white"},
                    "& .MuiInputLabel-root": {color: "white"},
                    "& .MuiOutlinedInput-root": {
                      "& fieldset": {borderColor: "white"},
                      "&:hover fieldset": {borderColor: "primary.main"},
                      "&.Mui-focused fieldset": {borderColor: "primary.main"},
                    },
                  }}
              />
            </Grid>
          </Grid>

          {/* Physical Metrics */}
          <Typography variant="h6" gutterBottom sx={{ mt: 4 }}>
            Physical Metrics
          </Typography>
          <Grid container spacing={2}>
            {/* Age Field */}
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

            {/* Weight Field */}
            <Grid item xs={12} sm={4}>
              <TextField
                fullWidth
                label="Weight"
                name="weight"
                value={formData.weight}
                onChange={handleInputChange}
                variant="outlined"
                type="number"
                inputProps={{ step: 0.1 }}
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

            {/* Weight Unit Selector */}
            <Grid item xs={12} sm={2}>
              <TextField
                select
                fullWidth
                label="Unit"
                value={formData.weight_unit}
                onChange={handleWeightUnitChange}
                variant="outlined"
                sx={{
                  color: "white",
                  "& .MuiInputBase-input": { color: "white" },
                  "& .MuiInputLabel-root": { color: "white" },
                  "& .MuiOutlinedInput-root": {
                    "& fieldset": { borderColor: "white" },
                    "&:hover fieldset": { borderColor: "primary.main" },
                    "&.Mui-focused fieldset": { borderColor: "primary.main" },
                  },
                }}
              >
                <MenuItem value="kg">kg</MenuItem>
                <MenuItem value="lbs">lbs</MenuItem>
              </TextField>
            </Grid>

            {/* Height Fields */}
            {formData.height_unit === "ft/in" ? (
              <>
                <Grid item xs={6} sm={3}>
                  <TextField
                    fullWidth
                    label="Feet"
                    name="height_ft"
                    value={formData.height_ft || ""}
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
                <Grid item xs={6} sm={3}>
                  <TextField
                    fullWidth
                    label="Inches"
                    name="height_in"
                    value={formData.height_in || ""}
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
              </>
            ) : (
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="Height (cm)"
                  name="height_cm"
                  value={formData.height_cm || ""}
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
            )}

            {/* Height Unit Selector */}
            <Grid item xs={12} sm={3}>
              <TextField
                select
                fullWidth
                label="Unit"
                value={formData.height_unit}
                onChange={handleHeightUnitChange}
                variant="outlined"
                sx={{
                  color: "white",
                  "& .MuiInputBase-input": { color: "white" },
                  "& .MuiInputLabel-root": { color: "white" },
                  "& .MuiOutlinedInput-root": {
                    "& fieldset": { borderColor: "white" },
                    "&:hover fieldset": { borderColor: "primary.main" },
                    "&.Mui-focused fieldset": { borderColor: "primary.main" },
                  },
                }}
              >
                <MenuItem value="cm">cm</MenuItem>
                <MenuItem value="ft/in">ft/in</MenuItem>
              </TextField>
            </Grid>
          </Grid>

          {/* Avatar Upload */}
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
              <Button variant="contained" component="label">
                Upload Avatar
                <input type="file" hidden accept="image/*" onChange={handleAvatarUpload} />
              </Button>
            </Grid>
          </Grid>

          <Button variant="contained" color="primary" onClick={handleSaveChanges} sx={{ mt: 4 }}>
            Save Changes
          </Button>
        </Box>
      </Box>
  );
};

 export default ProfileSettings;
