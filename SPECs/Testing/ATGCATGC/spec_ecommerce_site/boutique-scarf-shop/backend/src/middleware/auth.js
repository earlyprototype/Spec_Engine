/**
 * Authentication Middleware
 * Verifies JWT token and attaches user to request
 */

const { verifyToken, extractToken } = require('../utils/jwt');

/**
 * Middleware to verify JWT token
 * Attaches user info to req.user if valid
 * Returns 401 if token missing, invalid, or expired
 */
const authMiddleware = async (req, res, next) => {
  try {
    // Extract token from Authorization header
    const authHeader = req.headers.authorization;
    const token = extractToken(authHeader);

    if (!token) {
      return res.status(401).json({
        success: false,
        message: 'No token provided'
      });
    }

    // Verify and decode token
    const decoded = verifyToken(token);

    // Attach user info to request
    req.user = {
      userId: decoded.userId,
      email: decoded.email,
      role: decoded.role
    };

    // Continue to route handler
    next();

  } catch (error) {
    if (error.message === 'Token expired') {
      return res.status(401).json({
        success: false,
        message: 'Token expired'
      });
    }

    if (error.message === 'Invalid token') {
      return res.status(401).json({
        success: false,
        message: 'Invalid token'
      });
    }

    console.error('Auth middleware error:', error);
    return res.status(401).json({
      success: false,
      message: 'Authentication failed'
    });
  }
};

module.exports = authMiddleware;

