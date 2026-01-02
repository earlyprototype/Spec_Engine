# Authentication Architecture - Boutique Scarf Shop

## Overview
JWT-based authentication with bcrypt password hashing and role-based access control.

## Authentication Flow

### Registration Flow
1. Client submits registration form (email, password, name)
2. Backend validates input (email format, password strength)
3. Check if email already exists in database
4. Hash password with bcrypt (salt rounds: 10)
5. Create user record in database with role='customer'
6. Generate JWT token
7. Return token and user info (excluding password) to client
8. Client stores token (localStorage or httpOnly cookie)

### Login Flow
1. Client submits login credentials (email, password)
2. Backend validates input format
3. Query database for user by email
4. Compare submitted password with stored hash using bcrypt
5. If match: generate JWT token with user payload
6. Return token and user info to client
7. If no match: return 401 Unauthorized

### Protected Routes
1. Client includes JWT token in Authorization header: `Bearer <token>`
2. Middleware extracts and verifies token signature
3. Decode token to extract user payload (id, role, email)
4. Attach user info to request object
5. Route handler proceeds with authenticated user context
6. If token invalid/expired: return 401 Unauthorized

### Role-Based Access Control (RBAC)
- **Customer role**: Can browse products, manage cart, place orders, view own orders
- **Admin role**: All customer permissions + manage products, view all orders, update order status

## JWT Token Structure

```javascript
{
  payload: {
    userId: 123,
    email: 'user@example.com',
    role: 'customer', // or 'admin'
  },
  expiresIn: '24h',
  secret: process.env.JWT_SECRET
}
```

## Password Security

### Hashing Strategy
- Algorithm: bcrypt
- Salt rounds: 10
- Never store plain passwords
- Hash generated on registration and password change

### Password Requirements
- Minimum length: 8 characters
- Must contain: letters and numbers
- Recommended: special characters

## Session Management

### Token Expiry
- Access token: 24 hours
- Refresh token: Optional future enhancement (7 days)

### Token Storage (Client)
- localStorage: Simple but vulnerable to XSS
- httpOnly cookie: More secure (recommended for production)
- Current implementation: Allow both, configurable

## API Endpoints

### Public Endpoints
```
POST /api/auth/register
POST /api/auth/login
```

### Protected Endpoints
```
GET /api/auth/me (get current user info)
PUT /api/auth/profile (update user profile)
PUT /api/auth/password (change password)
```

### Admin-Only Endpoints
```
All endpoints under /api/admin/*
```

## Middleware

### authMiddleware
```javascript
// Verifies JWT token
// Attaches user to req.user
// Returns 401 if token invalid
```

### roleMiddleware(requiredRole)
```javascript
// Checks if req.user.role matches requiredRole
// Returns 403 if insufficient permissions
```

## Security Measures

1. **Password Hashing**: bcrypt with 10 salt rounds
2. **JWT Secret**: Stored in environment variable, minimum 32 characters
3. **Token Expiry**: 24-hour expiration
4. **Input Validation**: express-validator on all inputs
5. **Rate Limiting**: Optional enhancement to prevent brute force
6. **HTTPS Only**: In production
7. **No Credentials in Logs**: Password never logged
8. **SQL Injection Prevention**: Parameterized queries with pg library

## Error Handling

### Registration Errors
- 400: Invalid input (email format, password requirements)
- 409: Email already exists
- 500: Server error

### Login Errors
- 400: Invalid input
- 401: Invalid credentials
- 500: Server error

### Protected Route Errors
- 401: No token, invalid token, expired token
- 403: Insufficient permissions (role check failed)

## Testing Strategy

### Unit Tests
- Password hashing correctness
- JWT token generation/verification
- Middleware functions

### Integration Tests
- Registration endpoint (success, validation errors, duplicates)
- Login endpoint (success, invalid credentials)
- Protected routes (valid token, no token, expired token)
- Role checks (customer vs admin access)

## Implementation Files

```
backend/src/
├── middleware/
│   ├── auth.js              # JWT verification middleware
│   └── roleCheck.js         # Role-based authorization
├── services/
│   ├── authService.js       # Authentication business logic
│   └── userService.js       # User CRUD operations
├── routes/
│   └── auth.js              # Auth endpoint handlers
└── utils/
    ├── jwt.js               # JWT utilities
    └── validators.js        # Input validation rules
```

## Future Enhancements
- Refresh tokens for extended sessions
- Email verification on registration
- Password reset flow
- Two-factor authentication (2FA)
- OAuth integration (Google, Facebook)

---

**Generated:** 2025-11-02  
**Project:** ATGCATGC - scarf-boutique-ecommerce

