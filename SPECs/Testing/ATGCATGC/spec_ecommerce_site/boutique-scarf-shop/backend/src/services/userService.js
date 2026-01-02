/**
 * User Service
 * Business logic for user operations
 */

const bcrypt = require('bcrypt');
const db = require('../utils/database');

const SALT_ROUNDS = 10;

/**
 * Create new user (registration)
 * @param {object} userData - User registration data
 * @returns {Promise<object>} Created user (without password)
 */
const createUser = async (userData) => {
  const { email, password, firstName, lastName } = userData;

  // Check if email already exists (case-insensitive)
  const existingUser = await getUserByEmail(email);
  if (existingUser) {
    const error = new Error('Email already exists');
    error.statusCode = 409;
    throw error;
  }

  // Hash password
  const passwordHash = await bcrypt.hash(password, SALT_ROUNDS);

  // Insert user into database
  const query = `
    INSERT INTO users (email, password_hash, first_name, last_name, role)
    VALUES ($1, $2, $3, $4, $5)
    RETURNING id, email, first_name, last_name, role, created_at
  `;

  const values = [
    email.toLowerCase(),
    passwordHash,
    firstName || null,
    lastName || null,
    'customer' // Default role
  ];

  const result = await db.query(query, values);
  const user = result.rows[0];

  // Convert snake_case to camelCase
  return {
    id: user.id,
    email: user.email,
    firstName: user.first_name,
    lastName: user.last_name,
    role: user.role,
    createdAt: user.created_at
  };
};

/**
 * Get user by email
 * @param {string} email - User email
 * @returns {Promise<object|null>} User or null
 */
const getUserByEmail = async (email) => {
  const query = `
    SELECT id, email, password_hash, first_name, last_name, role, created_at
    FROM users
    WHERE LOWER(email) = LOWER($1)
  `;

  const result = await db.query(query, [email]);

  if (result.rows.length === 0) {
    return null;
  }

  const user = result.rows[0];
  return {
    id: user.id,
    email: user.email,
    passwordHash: user.password_hash,
    firstName: user.first_name,
    lastName: user.last_name,
    role: user.role,
    createdAt: user.created_at
  };
};

/**
 * Get user by ID
 * @param {number} userId - User ID
 * @returns {Promise<object|null>} User or null
 */
const getUserById = async (userId) => {
  const query = `
    SELECT id, email, first_name, last_name, role, created_at
    FROM users
    WHERE id = $1
  `;

  const result = await db.query(query, [userId]);

  if (result.rows.length === 0) {
    return null;
  }

  const user = result.rows[0];
  return {
    id: user.id,
    email: user.email,
    firstName: user.first_name,
    lastName: user.last_name,
    role: user.role,
    createdAt: user.created_at
  };
};

/**
 * Verify user password
 * @param {string} plainPassword - Plain text password
 * @param {string} passwordHash - Stored bcrypt hash
 * @returns {Promise<boolean>} True if match
 */
const verifyPassword = async (plainPassword, passwordHash) => {
  return await bcrypt.compare(plainPassword, passwordHash);
};

/**
 * Update user profile
 * @param {number} userId - User ID
 * @param {object} updates - Fields to update
 * @returns {Promise<object>} Updated user
 */
const updateUser = async (userId, updates) => {
  const { firstName, lastName, email } = updates;
  
  // Build dynamic update query
  const fields = [];
  const values = [];
  let paramCount = 1;

  if (firstName !== undefined) {
    fields.push(`first_name = $${paramCount++}`);
    values.push(firstName);
  }
  if (lastName !== undefined) {
    fields.push(`last_name = $${paramCount++}`);
    values.push(lastName);
  }
  if (email !== undefined) {
    fields.push(`email = $${paramCount++}`);
    values.push(email.toLowerCase());
  }

  if (fields.length === 0) {
    throw new Error('No fields to update');
  }

  fields.push(`updated_at = CURRENT_TIMESTAMP`);
  values.push(userId);

  const query = `
    UPDATE users
    SET ${fields.join(', ')}
    WHERE id = $${paramCount}
    RETURNING id, email, first_name, last_name, role, created_at, updated_at
  `;

  const result = await db.query(query, values);
  
  if (result.rows.length === 0) {
    return null;
  }

  const user = result.rows[0];
  return {
    id: user.id,
    email: user.email,
    firstName: user.first_name,
    lastName: user.last_name,
    role: user.role,
    createdAt: user.created_at,
    updatedAt: user.updated_at
  };
};

module.exports = {
  createUser,
  getUserByEmail,
  getUserById,
  verifyPassword,
  updateUser
};

