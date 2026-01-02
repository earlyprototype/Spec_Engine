/**
 * Order Service
 * Business logic for order management
 */

const db = require('../utils/database');

/**
 * Create order from successful payment
 * @param {object} orderData - Order data
 * @returns {Promise<object>} Created order
 */
const createOrder = async (orderData) => {
  const { userId, stripePaymentIntentId, totalAmount, items, shippingAddressId } = orderData;

  const client = await db.getClient();

  try {
    await client.query('BEGIN');

    // Create order
    const orderQuery = `
      INSERT INTO orders (user_id, stripe_payment_intent_id, total_amount, shipping_address_id, status)
      VALUES ($1, $2, $3, $4, $5)
      RETURNING id, user_id, stripe_payment_intent_id, total_amount, status, shipping_address_id, created_at
    `;

    const orderValues = [userId, stripePaymentIntentId, totalAmount, shippingAddressId || null, 'pending'];
    const orderResult = await client.query(orderQuery, orderValues);
    const order = orderResult.rows[0];

    // Create order items
    for (const item of items) {
      const itemQuery = `
        INSERT INTO order_items (order_id, product_id, product_name, quantity, price_at_purchase)
        VALUES ($1, $2, $3, $4, $5)
      `;

      const itemValues = [
        order.id,
        item.productId,
        item.productName,
        item.quantity,
        item.priceAtAddition
      ];

      await client.query(itemQuery, itemValues);

      // Reduce stock
      const stockQuery = `
        UPDATE products
        SET stock_quantity = stock_quantity - $1
        WHERE id = $2 AND stock_quantity >= $1
      `;

      const stockResult = await client.query(stockQuery, [item.quantity, item.productId]);

      if (stockResult.rowCount === 0) {
        throw new Error(`Insufficient stock for product ${item.productName}`);
      }
    }

    await client.query('COMMIT');

    return {
      id: order.id,
      userId: order.user_id,
      stripePaymentIntentId: order.stripe_payment_intent_id,
      totalAmount: parseFloat(order.total_amount),
      status: order.status,
      shippingAddressId: order.shipping_address_id,
      createdAt: order.created_at
    };

  } catch (error) {
    await client.query('ROLLBACK');
    console.error('Create order error:', error);
    throw error;
  } finally {
    client.release();
  }
};

/**
 * Get order by ID
 * @param {number} orderId - Order ID
 * @param {number} userId - User ID (for authorization)
 * @returns {Promise<object|null>} Order with items or null
 */
const getOrderById = async (orderId, userId = null) => {
  const query = `
    SELECT o.id, o.user_id, o.stripe_payment_intent_id, o.total_amount, o.status,
           o.shipping_address_id, o.created_at, o.updated_at,
           json_agg(
             json_build_object(
               'id', oi.id,
               'productId', oi.product_id,
               'productName', oi.product_name,
               'quantity', oi.quantity,
               'priceAtPurchase', oi.price_at_purchase
             ) ORDER BY oi.id
           ) as items
    FROM orders o
    LEFT JOIN order_items oi ON o.id = oi.order_id
    WHERE o.id = $1 ${userId ? 'AND o.user_id = $2' : ''}
    GROUP BY o.id
  `;

  const params = userId ? [orderId, userId] : [orderId];
  const result = await db.query(query, params);

  if (result.rows.length === 0) {
    return null;
  }

  const order = result.rows[0];
  return {
    id: order.id,
    userId: order.user_id,
    stripePaymentIntentId: order.stripe_payment_intent_id,
    totalAmount: parseFloat(order.total_amount),
    status: order.status,
    shippingAddressId: order.shipping_address_id,
    items: order.items,
    createdAt: order.created_at,
    updatedAt: order.updated_at
  };
};

/**
 * Get user's orders
 * @param {number} userId - User ID
 * @param {object} options - Pagination options
 * @returns {Promise<object>} Orders with pagination
 */
const getUserOrders = async (userId, options = {}) => {
  const { page = 1, limit = 20 } = options;
  const offset = (page - 1) * limit;

  // Get total count
  const countQuery = 'SELECT COUNT(*) FROM orders WHERE user_id = $1';
  const countResult = await db.query(countQuery, [userId]);
  const total = parseInt(countResult.rows[0].count);

  // Get orders
  const query = `
    SELECT id, user_id, stripe_payment_intent_id, total_amount, status, 
           shipping_address_id, created_at, updated_at
    FROM orders
    WHERE user_id = $1
    ORDER BY created_at DESC
    LIMIT $2 OFFSET $3
  `;

  const result = await db.query(query, [userId, limit, offset]);

  const orders = result.rows.map(o => ({
    id: o.id,
    userId: o.user_id,
    stripePaymentIntentId: o.stripe_payment_intent_id,
    totalAmount: parseFloat(o.total_amount),
    status: o.status,
    shippingAddressId: o.shipping_address_id,
    createdAt: o.created_at,
    updatedAt: o.updated_at
  }));

  return {
    orders,
    pagination: {
      page,
      limit,
      total,
      pages: Math.ceil(total / limit)
    }
  };
};

/**
 * Update order status
 * @param {number} orderId - Order ID
 * @param {string} status - New status
 * @returns {Promise<object|null>} Updated order or null
 */
const updateOrderStatus = async (orderId, status) => {
  const validStatuses = ['pending', 'processing', 'shipped', 'delivered', 'cancelled'];

  if (!validStatuses.includes(status)) {
    throw new Error('Invalid order status');
  }

  const query = `
    UPDATE orders
    SET status = $1, updated_at = CURRENT_TIMESTAMP
    WHERE id = $2
    RETURNING id, user_id, status, updated_at
  `;

  const result = await db.query(query, [status, orderId]);

  if (result.rows.length === 0) {
    return null;
  }

  const order = result.rows[0];
  return {
    id: order.id,
    userId: order.user_id,
    status: order.status,
    updatedAt: order.updated_at
  };
};

/**
 * Get all orders (admin)
 * @param {object} options - Pagination and filter options
 * @returns {Promise<object>} Orders with pagination
 */
const getAllOrders = async (options = {}) => {
  const { page = 1, limit = 20, status = null } = options;
  const offset = (page - 1) * limit;

  let whereClause = '';
  const params = [limit, offset];

  if (status) {
    whereClause = 'WHERE status = $3';
    params.push(status);
  }

  // Get total count
  const countQuery = `SELECT COUNT(*) FROM orders ${whereClause.replace('$3', '$1')}`;
  const countParams = status ? [status] : [];
  const countResult = await db.query(countQuery, countParams);
  const total = parseInt(countResult.rows[0].count);

  // Get orders
  const query = `
    SELECT id, user_id, stripe_payment_intent_id, total_amount, status,
           shipping_address_id, created_at, updated_at
    FROM orders
    ${whereClause}
    ORDER BY created_at DESC
    LIMIT $1 OFFSET $2
  `;

  const result = await db.query(query, params);

  const orders = result.rows.map(o => ({
    id: o.id,
    userId: o.user_id,
    stripePaymentIntentId: o.stripe_payment_intent_id,
    totalAmount: parseFloat(o.total_amount),
    status: o.status,
    shippingAddressId: o.shipping_address_id,
    createdAt: o.created_at,
    updatedAt: o.updated_at
  }));

  return {
    orders,
    pagination: {
      page,
      limit,
      total,
      pages: Math.ceil(total / limit)
    }
  };
};

module.exports = {
  createOrder,
  getOrderById,
  getUserOrders,
  updateOrderStatus,
  getAllOrders
};

