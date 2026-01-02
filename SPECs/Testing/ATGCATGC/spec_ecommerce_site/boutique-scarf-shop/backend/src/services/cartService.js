/**
 * Shopping Cart Service
 * Business logic for cart operations
 */

const db = require('../utils/database');

/**
 * Get or create cart for user
 * @param {number} userId - User ID
 * @returns {Promise<object>} Cart
 */
const getOrCreateCart = async (userId) => {
  // Try to get existing cart
  let query = 'SELECT id, user_id, created_at, updated_at FROM carts WHERE user_id = $1';
  let result = await db.query(query, [userId]);

  if (result.rows.length > 0) {
    const cart = result.rows[0];
    return {
      id: cart.id,
      userId: cart.user_id,
      createdAt: cart.created_at,
      updatedAt: cart.updated_at
    };
  }

  // Create new cart
  query = `
    INSERT INTO carts (user_id)
    VALUES ($1)
    RETURNING id, user_id, created_at, updated_at
  `;
  
  result = await db.query(query, [userId]);
  const cart = result.rows[0];
  
  return {
    id: cart.id,
    userId: cart.user_id,
    createdAt: cart.created_at,
    updatedAt: cart.updated_at
  };
};

/**
 * Get cart with items
 * @param {number} userId - User ID
 * @returns {Promise<object>} Cart with items and total
 */
const getCart = async (userId) => {
  const cart = await getOrCreateCart(userId);

  const query = `
    SELECT ci.id, ci.quantity, ci.price_at_addition,
           p.id as product_id, p.name as product_name, p.price as current_price, 
           p.stock_quantity, p.description
    FROM cart_items ci
    JOIN products p ON ci.product_id = p.id
    WHERE ci.cart_id = $1
    ORDER BY ci.created_at DESC
  `;

  const result = await db.query(query, [cart.id]);

  const items = result.rows.map(item => ({
    id: item.id,
    productId: item.product_id,
    productName: item.product_name,
    quantity: item.quantity,
    priceAtAddition: parseFloat(item.price_at_addition),
    currentPrice: parseFloat(item.current_price),
    stockQuantity: item.stock_quantity,
    subtotal: parseFloat(item.price_at_addition) * item.quantity
  }));

  const total = items.reduce((sum, item) => sum + item.subtotal, 0);

  return {
    cartId: cart.id,
    items,
    total
  };
};

/**
 * Add item to cart
 * @param {number} userId - User ID
 * @param {number} productId - Product ID
 * @param {number} quantity - Quantity to add
 * @returns {Promise<object>} Updated cart
 */
const addItem = async (userId, productId, quantity = 1) => {
  const cart = await getOrCreateCart(userId);

  // Check if product exists and has stock
  const productQuery = 'SELECT id, price, stock_quantity FROM products WHERE id = $1';
  const productResult = await db.query(productQuery, [productId]);

  if (productResult.rows.length === 0) {
    const error = new Error('Product not found');
    error.statusCode = 404;
    throw error;
  }

  const product = productResult.rows[0];

  if (product.stock_quantity < quantity) {
    const error = new Error('Insufficient stock');
    error.statusCode = 400;
    throw error;
  }

  // Check if item already in cart
  const checkQuery = 'SELECT id, quantity FROM cart_items WHERE cart_id = $1 AND product_id = $2';
  const checkResult = await db.query(checkQuery, [cart.id, productId]);

  if (checkResult.rows.length > 0) {
    // Update quantity
    const existingItem = checkResult.rows[0];
    const newQuantity = existingItem.quantity + quantity;

    if (product.stock_quantity < newQuantity) {
      const error = new Error('Insufficient stock');
      error.statusCode = 400;
      throw error;
    }

    const updateQuery = `
      UPDATE cart_items
      SET quantity = $1, updated_at = CURRENT_TIMESTAMP
      WHERE id = $2
      RETURNING id
    `;
    await db.query(updateQuery, [newQuantity, existingItem.id]);
  } else {
    // Add new item
    const insertQuery = `
      INSERT INTO cart_items (cart_id, product_id, quantity, price_at_addition)
      VALUES ($1, $2, $3, $4)
    `;
    await db.query(insertQuery, [cart.id, productId, quantity, product.price]);
  }

  // Update cart timestamp
  await db.query('UPDATE carts SET updated_at = CURRENT_TIMESTAMP WHERE id = $1', [cart.id]);

  return await getCart(userId);
};

/**
 * Update cart item quantity
 * @param {number} userId - User ID
 * @param {number} itemId - Cart item ID
 * @param {number} quantity - New quantity
 * @returns {Promise<object>} Updated cart
 */
const updateItem = async (userId, itemId, quantity) => {
  const cart = await getOrCreateCart(userId);

  if (quantity < 1) {
    const error = new Error('Quantity must be at least 1');
    error.statusCode = 400;
    throw error;
  }

  // Check if item belongs to user's cart
  const checkQuery = `
    SELECT ci.product_id, p.stock_quantity
    FROM cart_items ci
    JOIN products p ON ci.product_id = p.id
    WHERE ci.id = $1 AND ci.cart_id = $2
  `;
  const checkResult = await db.query(checkQuery, [itemId, cart.id]);

  if (checkResult.rows.length === 0) {
    const error = new Error('Cart item not found');
    error.statusCode = 404;
    throw error;
  }

  const { stock_quantity } = checkResult.rows[0];

  if (stock_quantity < quantity) {
    const error = new Error('Insufficient stock');
    error.statusCode = 400;
    throw error;
  }

  // Update quantity
  const updateQuery = `
    UPDATE cart_items
    SET quantity = $1, updated_at = CURRENT_TIMESTAMP
    WHERE id = $2
  `;
  await db.query(updateQuery, [quantity, itemId]);

  await db.query('UPDATE carts SET updated_at = CURRENT_TIMESTAMP WHERE id = $1', [cart.id]);

  return await getCart(userId);
};

/**
 * Remove item from cart
 * @param {number} userId - User ID
 * @param {number} itemId - Cart item ID
 * @returns {Promise<object>} Updated cart
 */
const removeItem = async (userId, itemId) => {
  const cart = await getOrCreateCart(userId);

  const deleteQuery = 'DELETE FROM cart_items WHERE id = $1 AND cart_id = $2';
  const result = await db.query(deleteQuery, [itemId, cart.id]);

  if (result.rowCount === 0) {
    const error = new Error('Cart item not found');
    error.statusCode = 404;
    throw error;
  }

  await db.query('UPDATE carts SET updated_at = CURRENT_TIMESTAMP WHERE id = $1', [cart.id]);

  return await getCart(userId);
};

/**
 * Clear cart
 * @param {number} userId - User ID
 * @returns {Promise<object>} Empty cart
 */
const clearCart = async (userId) => {
  const cart = await getOrCreateCart(userId);

  await db.query('DELETE FROM cart_items WHERE cart_id = $1', [cart.id]);
  await db.query('UPDATE carts SET updated_at = CURRENT_TIMESTAMP WHERE id = $1', [cart.id]);

  return {
    cartId: cart.id,
    items: [],
    total: 0
  };
};

/**
 * Validate cart before checkout
 * @param {number} userId - User ID
 * @returns {Promise<object>} Validation result
 */
const validateCart = async (userId) => {
  const cart = await getCart(userId);

  if (cart.items.length === 0) {
    return {
      valid: false,
      errors: ['Cart is empty']
    };
  }

  const errors = [];

  for (const item of cart.items) {
    // Check if product still exists
    if (!item.productId) {
      errors.push(`Product no longer available`);
      continue;
    }

    // Check stock
    if (item.stockQuantity < item.quantity) {
      errors.push(`Insufficient stock for ${item.productName}`);
    }

    // Check price changes
    if (item.currentPrice !== item.priceAtAddition) {
      errors.push(`Price changed for ${item.productName}`);
    }
  }

  return {
    valid: errors.length === 0,
    errors
  };
};

module.exports = {
  getCart,
  addItem,
  updateItem,
  removeItem,
  clearCart,
  validateCart
};

