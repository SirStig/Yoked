/**
 * Generate a strong password.
 * - Minimum length: 12 characters
 * - Includes: Uppercase, lowercase, numbers, and special characters
 *
 * @returns {string} A randomly generated strong password.
 */
export const generateStrongPassword = () => {
  const length = 20; // Minimum length
  const uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
  const lowercase = "abcdefghijklmnopqrstuvwxyz";
  const numbers = "0123456789";
  const specialCharacters = "@$!%*?&";
  const allCharacters = uppercase + lowercase + numbers + specialCharacters;

  let password = "";

  // Ensure at least one character from each category
  password += uppercase[Math.floor(Math.random() * uppercase.length)];
  password += lowercase[Math.floor(Math.random() * lowercase.length)];
  password += numbers[Math.floor(Math.random() * numbers.length)];
  password += specialCharacters[Math.floor(Math.random() * specialCharacters.length)];

  // Fill the rest of the password with random characters
  for (let i = password.length; i < length; i++) {
    password += allCharacters[Math.floor(Math.random() * allCharacters.length)];
  }

  // Shuffle the password to ensure randomness
  return password
    .split("")
    .sort(() => 0.5 - Math.random())
    .join("");
};
