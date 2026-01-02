/**
 * Role-Based Authorization Middleware
 * Checks if user has required role
 */

/**
 * Middleware to check if user has required role
 * Must be used after authMiddleware
 * @param {string} requiredRole - Required role ('admin', 'customer')
 * @returns {Function} Express middleware
 */
const roleCheck = (requiredRole) => {
  return (req, res, next) => {
    // User attached by authMiddleware
    if (!req.user) {
      return res.status(401).json({
        success: false,
        message: 'Authentication required'
      });
    }

    // Check role
    if (req.user.role !== requiredRole) {
      return res.status(403).json({
        success: false,
        message: 'Insufficient permissions'
      });
    }

    // User has required role
    next();
  };
};

/**
 * Middleware to check if user is admin
 * Convenience wrapper for roleCheck('admin')
 */
const adminOnly = roleCheck('admin');

module.exports = {
  roleCheck,
  adminOnly
};

