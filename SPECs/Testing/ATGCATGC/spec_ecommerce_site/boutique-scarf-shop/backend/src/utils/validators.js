/**
 * Input Validation Rules
 * Using express-validator
 */

const { body } = require('express-validator');

const registrationValidation = [
  body('email')
    .trim()
    .notEmpty().withMessage('Email is required')
    .isEmail().withMessage('Must be a valid email address')
    .normalizeEmail(),
  
  body('password')
    .notEmpty().withMessage('Password is required')
    .isLength({ min: 8 }).withMessage('Password must be at least 8 characters')
    .matches(/^(?=.*[A-Za-z])(?=.*\d)/).withMessage('Password must contain letters and numbers'),
  
  body('firstName')
    .optional()
    .trim()
    .isLength({ max: 100 }).withMessage('First name too long'),
  
  body('lastName')
    .optional()
    .trim()
    .isLength({ max: 100 }).withMessage('Last name too long')
];

const loginValidation = [
  body('email')
    .trim()
    .notEmpty().withMessage('Email is required')
    .isEmail().withMessage('Must be a valid email address')
    .normalizeEmail(),
  
  body('password')
    .notEmpty().withMessage('Password is required')
];

const profileUpdateValidation = [
  body('firstName')
    .optional()
    .trim()
    .isLength({ max: 100 }).withMessage('First name too long'),
  
  body('lastName')
    .optional()
    .trim()
    .isLength({ max: 100 }).withMessage('Last name too long'),
  
  body('email')
    .optional()
    .trim()
    .isEmail().withMessage('Must be a valid email address')
    .normalizeEmail()
];

module.exports = {
  registrationValidation,
  loginValidation,
  profileUpdateValidation
};

