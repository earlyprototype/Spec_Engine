/**
 * JWT Token Utilities
 * Generation and verification of JSON Web Tokens
 */

const jwt = require('jsonwebtoken');

const JWT_SECRET = process.env.JWT_SECRET || 'dev_secret_min_32_chars_change_in_production';
const JWT_EXPIRES_IN = '24h';

/**
 * Generate JWT token for user
 * @param {object} user - User object with id, email, role
 * @returns {string} JWT token
 */
const generateToken = (user) => {
  const payload = {
    userId: user.id,
    email: user.email,
    role: user.role
  };

  const token = jwt.sign(payload, JWT_SECRET, {
    expiresIn: JWT_EXPIRES_IN
  });

  return token;
};

/**
 * Verify and decode JWT token
 * @param {string} token - JWT token
 * @returns {object} Decoded payload
 * @throws {Error} If token invalid or expired
 */
const verifyToken = (token) => {
  try {
    const decoded = jwt.verify(token, JWT_SECRET);
    return decoded;
  } catch (error) {
    if (error.name === 'TokenExpiredError') {
      throw new Error('Token expired');
    }
    if (error.name === 'JsonWebTokenError') {
      throw new Error('Invalid token');
    }
    throw error;
  }
};

/**
 * Extract token from Authorization header
 * @param {string} authHeader - Authorization header value
 * @returns {string|null} Token or null
 */
const extractToken = (authHeader) => {
  if (!authHeader) {
    return null;
  }

  // Expected format: "Bearer <token>"
  const parts = authHeader.split(' ');
  if (parts.length !== 2 || parts[0] !== 'Bearer') {
    return null;
  }

  return parts[1];
};

module.exports = {
  generateToken,
  verifyToken,
  extractToken
};

