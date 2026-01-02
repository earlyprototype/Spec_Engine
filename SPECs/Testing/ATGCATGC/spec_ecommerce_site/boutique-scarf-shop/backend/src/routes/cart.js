/**
 * Shopping Cart Routes
 * Cart management endpoints
 */

const express = require('express');
const { body, validationResult } = require('express-validator');
const cartService = require('../services/cartService');
const authMiddleware = require('../middleware/auth');

const router = express.Router();

// All cart routes require authentication
router.use(authMiddleware);

/**
 * GET /api/cart
 * Get current user's cart
 */
router.get('/', async (req, res) => {
  try {
    const cart = await cartService.getCart(req.user.userId);

    res.status(200).json({
      success: true,
      cart
    });

  } catch (error) {
    console.error('Get cart error:', error);
    res.status(500).json({
      success: false,
      message: 'Server error'
    });
  }
});

/**
 * POST /api/cart/items
 * Add item to cart
 */
router.post('/items', [
  body('productId').isInt({ min: 1 }).withMessage('Valid product ID required'),
  body('quantity').optional().isInt({ min: 1 }).withMessage('Quantity must be positive')
], async (req, res) => {
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

    const { productId, quantity = 1 } = req.body;
    const cart = await cartService.addItem(req.user.userId, productId, quantity);

    res.status(200).json({
      success: true,
      cart
    });

  } catch (error) {
    if (error.statusCode) {
      return res.status(error.statusCode).json({
        success: false,
        message: error.message
      });
    }

    console.error('Add to cart error:', error);
    res.status(500).json({
      success: false,
      message: 'Server error'
    });
  }
});

/**
 * PUT /api/cart/items/:id
 * Update cart item quantity
 */
router.put('/items/:id', [
  body('quantity').isInt({ min: 1 }).withMessage('Quantity must be positive')
], async (req, res) => {
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

    const itemId = parseInt(req.params.id);
    const { quantity } = req.body;

    const cart = await cartService.updateItem(req.user.userId, itemId, quantity);

    res.status(200).json({
      success: true,
      cart
    });

  } catch (error) {
    if (error.statusCode) {
      return res.status(error.statusCode).json({
        success: false,
        message: error.message
      });
    }

    console.error('Update cart item error:', error);
    res.status(500).json({
      success: false,
      message: 'Server error'
    });
  }
});

/**
 * DELETE /api/cart/items/:id
 * Remove item from cart
 */
router.delete('/items/:id', async (req, res) => {
  try {
    const itemId = parseInt(req.params.id);
    const cart = await cartService.removeItem(req.user.userId, itemId);

    res.status(200).json({
      success: true,
      cart
    });

  } catch (error) {
    if (error.statusCode) {
      return res.status(error.statusCode).json({
        success: false,
        message: error.message
      });
    }

    console.error('Remove cart item error:', error);
    res.status(500).json({
      success: false,
      message: 'Server error'
    });
  }
});

/**
 * DELETE /api/cart
 * Clear cart
 */
router.delete('/', async (req, res) => {
  try {
    const cart = await cartService.clearCart(req.user.userId);

    res.status(200).json({
      success: true,
      cart
    });

  } catch (error) {
    console.error('Clear cart error:', error);
    res.status(500).json({
      success: false,
      message: 'Server error'
    });
  }
});

/**
 * POST /api/cart/validate
 * Validate cart before checkout
 */
router.post('/validate', async (req, res) => {
  try {
    const validation = await cartService.validateCart(req.user.userId);

    res.status(200).json({
      success: true,
      validation
    });

  } catch (error) {
    console.error('Validate cart error:', error);
    res.status(500).json({
      success: false,
      message: 'Server error'
    });
  }
});

module.exports = router;

