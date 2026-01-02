/**
 * Product Routes
 * Public and admin product management endpoints
 */

const express = require('express');
const multer = require('multer');
const { body, validationResult } = require('express-validator');
const productService = require('../services/productService');
const cloudinaryService = require('../services/cloudinaryService');
const authMiddleware = require('../middleware/auth');
const { adminOnly } = require('../middleware/roleCheck');

const router = express.Router();

// Configure multer for file uploads (memory storage)
const upload = multer({
  storage: multer.memoryStorage(),
  limits: {
    fileSize: 10 * 1024 * 1024 // 10MB limit (as per constraints)
  },
  fileFilter: (req, file, cb) => {
    // Accept only images
    if (file.mimetype.startsWith('image/')) {
      cb(null, true);
    } else {
      cb(new Error('Only image files are allowed'), false);
    }
  }
});

// Validation rules
const productValidation = [
  body('name').trim().notEmpty().withMessage('Name is required'),
  body('description').optional().trim(),
  body('price').isFloat({ min: 0 }).withMessage('Price must be positive'),
  body('stockQuantity').optional().isInt({ min: 0 }).withMessage('Stock must be non-negative'),
  body('categoryId').optional().isInt()
];

/**
 * GET /api/products
 * Get all products with optional filters (public)
 */
router.get('/', async (req, res) => {
  try {
    const { page, limit, search, category } = req.query;
    
    const options = {
      page: parseInt(page) || 1,
      limit: parseInt(limit) || 20,
      search: search || '',
      categoryId: category ? parseInt(category) : null
    };

    const result = await productService.getProducts(options);

    res.status(200).json({
      success: true,
      ...result
    });

  } catch (error) {
    console.error('Get products error:', error);
    res.status(500).json({
      success: false,
      message: 'Server error'
    });
  }
});

/**
 * GET /api/products/:id
 * Get single product with images (public)
 */
router.get('/:id', async (req, res) => {
  try {
    const productId = parseInt(req.params.id);
    
    const product = await productService.getProductById(productId);

    if (!product) {
      return res.status(404).json({
        success: false,
        message: 'Product not found'
      });
    }

    res.status(200).json({
      success: true,
      product
    });

  } catch (error) {
    console.error('Get product error:', error);
    res.status(500).json({
      success: false,
      message: 'Server error'
    });
  }
});

/**
 * POST /api/products
 * Create new product (admin only)
 */
router.post('/', authMiddleware, adminOnly, productValidation, async (req, res) => {
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

    const product = await productService.createProduct(req.body);

    res.status(201).json({
      success: true,
      product
    });

  } catch (error) {
    console.error('Create product error:', error);
    res.status(500).json({
      success: false,
      message: 'Server error'
    });
  }
});

/**
 * PUT /api/products/:id
 * Update product (admin only)
 */
router.put('/:id', authMiddleware, adminOnly, productValidation, async (req, res) => {
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

    const productId = parseInt(req.params.id);
    const product = await productService.updateProduct(productId, req.body);

    if (!product) {
      return res.status(404).json({
        success: false,
        message: 'Product not found'
      });
    }

    res.status(200).json({
      success: true,
      product
    });

  } catch (error) {
    console.error('Update product error:', error);
    res.status(500).json({
      success: false,
      message: 'Server error'
    });
  }
});

/**
 * DELETE /api/products/:id
 * Delete product (admin only)
 */
router.delete('/:id', authMiddleware, adminOnly, async (req, res) => {
  try {
    const productId = parseInt(req.params.id);
    const deleted = await productService.deleteProduct(productId);

    if (!deleted) {
      return res.status(404).json({
        success: false,
        message: 'Product not found'
      });
    }

    res.status(200).json({
      success: true,
      message: 'Product deleted successfully'
    });

  } catch (error) {
    console.error('Delete product error:', error);
    res.status(500).json({
      success: false,
      message: 'Server error'
    });
  }
});

/**
 * POST /api/products/:id/images
 * Upload product image to Cloudinary (admin only)
 */
router.post('/:id/images', authMiddleware, adminOnly, upload.single('image'), async (req, res) => {
  try {
    const productId = parseInt(req.params.id);

    if (!req.file) {
      return res.status(400).json({
        success: false,
        message: 'No image file provided'
      });
    }

    // Check if product exists
    const product = await productService.getProductById(productId);
    if (!product) {
      return res.status(404).json({
        success: false,
        message: 'Product not found'
      });
    }

    // Convert buffer to base64 data URI
    const base64Image = `data:${req.file.mimetype};base64,${req.file.buffer.toString('base64')}`;

    // Upload to Cloudinary
    const uploadResult = await cloudinaryService.uploadImage(base64Image);

    // Save image reference in database
    const imageRecord = await productService.addProductImage(productId, {
      publicId: uploadResult.publicId,
      url: uploadResult.url,
      isPrimary: req.body.isPrimary === 'true' || product.images.length === 0
    });

    res.status(201).json({
      success: true,
      image: imageRecord
    });

  } catch (error) {
    console.error('Image upload error:', error);
    res.status(500).json({
      success: false,
      message: `Image upload failed: ${error.message}`
    });
  }
});

module.exports = router;

