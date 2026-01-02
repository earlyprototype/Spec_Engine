/**
 * Product Service
 * Business logic for product operations
 */

const db = require('../utils/database');

/**
 * Create new product
 * @param {object} productData - Product creation data
 * @returns {Promise<object>} Created product
 */
const createProduct = async (productData) => {
  const { name, description, price, stockQuantity, categoryId } = productData;

  const query = `
    INSERT INTO products (name, description, price, stock_quantity, category_id)
    VALUES ($1, $2, $3, $4, $5)
    RETURNING id, name, description, price, stock_quantity, category_id, created_at, updated_at
  `;

  const values = [name, description, price || 0, stockQuantity || 0, categoryId || null];
  
  const result = await db.query(query, values);
  const product = result.rows[0];

  return {
    id: product.id,
    name: product.name,
    description: product.description,
    price: parseFloat(product.price),
    stockQuantity: product.stock_quantity,
    categoryId: product.category_id,
    createdAt: product.created_at,
    updatedAt: product.updated_at
  };
};

/**
 * Get all products with pagination
 * @param {object} options - Query options (page, limit, search, category)
 * @returns {Promise<object>} Products and pagination info
 */
const getProducts = async (options = {}) => {
  const { page = 1, limit = 20, search = '', categoryId = null } = options;
  const offset = (page - 1) * limit;

  let whereConditions = [];
  let queryParams = [];
  let paramCount = 1;

  // Search by name or description
  if (search) {
    whereConditions.push(`(name ILIKE $${paramCount} OR description ILIKE $${paramCount})`);
    queryParams.push(`%${search}%`);
    paramCount++;
  }

  // Filter by category
  if (categoryId) {
    whereConditions.push(`category_id = $${paramCount}`);
    queryParams.push(categoryId);
    paramCount++;
  }

  const whereClause = whereConditions.length > 0 ? `WHERE ${whereConditions.join(' AND ')}` : '';

  // Get total count
  const countQuery = `SELECT COUNT(*) FROM products ${whereClause}`;
  const countResult = await db.query(countQuery, queryParams);
  const total = parseInt(countResult.rows[0].count);

  // Get products
  const query = `
    SELECT id, name, description, price, stock_quantity, category_id, created_at, updated_at
    FROM products
    ${whereClause}
    ORDER BY created_at DESC
    LIMIT $${paramCount} OFFSET $${paramCount + 1}
  `;
  
  queryParams.push(limit, offset);
  const result = await db.query(query, queryParams);

  const products = result.rows.map(p => ({
    id: p.id,
    name: p.name,
    description: p.description,
    price: parseFloat(p.price),
    stockQuantity: p.stock_quantity,
    categoryId: p.category_id,
    createdAt: p.created_at,
    updatedAt: p.updated_at
  }));

  return {
    products,
    pagination: {
      page,
      limit,
      total,
      pages: Math.ceil(total / limit)
    }
  };
};

/**
 * Get product by ID with images
 * @param {number} productId - Product ID
 * @returns {Promise<object|null>} Product with images or null
 */
const getProductById = async (productId) => {
  const query = `
    SELECT p.id, p.name, p.description, p.price, p.stock_quantity, p.category_id, 
           p.created_at, p.updated_at,
           json_agg(
             json_build_object(
               'id', pi.id,
               'url', pi.cloudinary_url,
               'publicId', pi.cloudinary_public_id,
               'isPrimary', pi.is_primary,
               'displayOrder', pi.display_order
             ) ORDER BY pi.display_order
           ) FILTER (WHERE pi.id IS NOT NULL) as images
    FROM products p
    LEFT JOIN product_images pi ON p.id = pi.product_id
    WHERE p.id = $1
    GROUP BY p.id
  `;

  const result = await db.query(query, [productId]);

  if (result.rows.length === 0) {
    return null;
  }

  const p = result.rows[0];
  return {
    id: p.id,
    name: p.name,
    description: p.description,
    price: parseFloat(p.price),
    stockQuantity: p.stock_quantity,
    categoryId: p.category_id,
    images: p.images || [],
    createdAt: p.created_at,
    updatedAt: p.updated_at
  };
};

/**
 * Update product
 * @param {number} productId - Product ID
 * @param {object} updates - Fields to update
 * @returns {Promise<object|null>} Updated product or null
 */
const updateProduct = async (productId, updates) => {
  const { name, description, price, stockQuantity, categoryId } = updates;

  const fields = [];
  const values = [];
  let paramCount = 1;

  if (name !== undefined) {
    fields.push(`name = $${paramCount++}`);
    values.push(name);
  }
  if (description !== undefined) {
    fields.push(`description = $${paramCount++}`);
    values.push(description);
  }
  if (price !== undefined) {
    fields.push(`price = $${paramCount++}`);
    values.push(price);
  }
  if (stockQuantity !== undefined) {
    fields.push(`stock_quantity = $${paramCount++}`);
    values.push(stockQuantity);
  }
  if (categoryId !== undefined) {
    fields.push(`category_id = $${paramCount++}`);
    values.push(categoryId);
  }

  if (fields.length === 0) {
    throw new Error('No fields to update');
  }

  fields.push(`updated_at = CURRENT_TIMESTAMP`);
  values.push(productId);

  const query = `
    UPDATE products
    SET ${fields.join(', ')}
    WHERE id = $${paramCount}
    RETURNING id, name, description, price, stock_quantity, category_id, created_at, updated_at
  `;

  const result = await db.query(query, values);

  if (result.rows.length === 0) {
    return null;
  }

  const p = result.rows[0];
  return {
    id: p.id,
    name: p.name,
    description: p.description,
    price: parseFloat(p.price),
    stockQuantity: p.stock_quantity,
    categoryId: p.category_id,
    createdAt: p.created_at,
    updatedAt: p.updated_at
  };
};

/**
 * Delete product
 * @param {number} productId - Product ID
 * @returns {Promise<boolean>} True if deleted
 */
const deleteProduct = async (productId) => {
  const query = 'DELETE FROM products WHERE id = $1';
  const result = await db.query(query, [productId]);
  return result.rowCount > 0;
};

/**
 * Add image to product
 * @param {number} productId - Product ID
 * @param {object} imageData - Image data (publicId, url, isPrimary)
 * @returns {Promise<object>} Created image record
 */
const addProductImage = async (productId, imageData) => {
  const { publicId, url, isPrimary = false, displayOrder = 0 } = imageData;

  const query = `
    INSERT INTO product_images (product_id, cloudinary_public_id, cloudinary_url, is_primary, display_order)
    VALUES ($1, $2, $3, $4, $5)
    RETURNING id, product_id, cloudinary_public_id, cloudinary_url, is_primary, display_order, created_at
  `;

  const values = [productId, publicId, url, isPrimary, displayOrder];
  const result = await db.query(query, values);
  const img = result.rows[0];

  return {
    id: img.id,
    productId: img.product_id,
    publicId: img.cloudinary_public_id,
    url: img.cloudinary_url,
    isPrimary: img.is_primary,
    displayOrder: img.display_order,
    createdAt: img.created_at
  };
};

module.exports = {
  createProduct,
  getProducts,
  getProductById,
  updateProduct,
  deleteProduct,
  addProductImage
};

