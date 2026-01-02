/**
 * Authentication Routes
 * Handles registration, login, and profile endpoints
 */

const express = require('express');
const { validationResult } = require('express-validator');
const userService = require('../services/userService');
const { generateToken } = require('../utils/jwt');
const { registrationValidation, loginValidation, profileUpdateValidation } = require('../utils/validators');
const authMiddleware = require('../middleware/auth');

const router = express.Router();

/**
 * POST /api/auth/register
 * Register new user
 */
router.post('/register', registrationValidation, async (req, res) => {
  try {
    // Check validation errors
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({
        success: false,
        errors: errors.array().map(err => ({
          field: err.path || err.param,
          message: err.msg
        }))
      });
    }

    // Create user
    const user = await userService.createUser(req.body);

    // Generate JWT token
    const token = generateToken(user);

    // Return success response
    res.status(201).json({
      success: true,
      token,
      user: {
        id: user.id,
        email: user.email,
        firstName: user.firstName,
        lastName: user.lastName,
        role: user.role
      }
    });

  } catch (error) {
    // Handle duplicate email (409)
    if (error.statusCode === 409) {
      return res.status(409).json({
        success: false,
        message: error.message
      });
    }

    // Handle other errors (500)
    console.error('Registration error:', error);
    res.status(500).json({
      success: false,
      message: 'Server error during registration'
    });
  }
});

/**
 * POST /api/auth/login
 * Login existing user
 */
router.post('/login', loginValidation, async (req, res) => {
  try {
    // Check validation errors
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({
        success: false,
        errors: errors.array().map(err => ({
          field: err.path || err.param,
          message: err.msg
        }))
      });
    }

    const { email, password } = req.body;

    // Get user by email
    const user = await userService.getUserByEmail(email);
    if (!user) {
      return res.status(401).json({
        success: false,
        message: 'Invalid credentials'
      });
    }

    // Verify password
    const isValidPassword = await userService.verifyPassword(password, user.passwordHash);
    if (!isValidPassword) {
      return res.status(401).json({
        success: false,
        message: 'Invalid credentials'
      });
    }

    // Generate JWT token
    const token = generateToken(user);

    // Return success response (without password)
    res.status(200).json({
      success: true,
      token,
      user: {
        id: user.id,
        email: user.email,
        firstName: user.firstName,
        lastName: user.lastName,
        role: user.role
      }
    });

  } catch (error) {
    console.error('Login error:', error);
    res.status(500).json({
      success: false,
      message: 'Server error during login'
    });
  }
});

/**
 * GET /api/auth/me
 * Get current user info (protected)
 */
router.get('/me', authMiddleware, async (req, res) => {
  try {
    // User info attached by authMiddleware
    const user = await userService.getUserById(req.user.userId);

    if (!user) {
      return res.status(404).json({
        success: false,
        message: 'User not found'
      });
    }

    res.status(200).json({
      success: true,
      user: {
        id: user.id,
        email: user.email,
        firstName: user.firstName,
        lastName: user.lastName,
        role: user.role
      }
    });

  } catch (error) {
    console.error('Get user error:', error);
    res.status(500).json({
      success: false,
      message: 'Server error'
    });
  }
});

/**
 * PUT /api/auth/profile
 * Update user profile (protected)
 */
router.put('/profile', authMiddleware, profileUpdateValidation, async (req, res) => {
  try {
    // Check validation errors
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({
        success: false,
        errors: errors.array().map(err => ({
          field: err.path || err.param,
          message: err.msg
        }))
      });
    }

    // Update user
    const updatedUser = await userService.updateUser(req.user.userId, req.body);

    if (!updatedUser) {
      return res.status(404).json({
        success: false,
        message: 'User not found'
      });
    }

    res.status(200).json({
      success: true,
      user: {
        id: updatedUser.id,
        email: updatedUser.email,
        firstName: updatedUser.firstName,
        lastName: updatedUser.lastName,
        role: updatedUser.role
      }
    });

  } catch (error) {
    console.error('Profile update error:', error);
    res.status(500).json({
      success: false,
      message: 'Server error'
    });
  }
});

module.exports = router;

