# Local Setup Guide - Boutique Scarf Shop

## Quick Start (Development Mode)

### 1. Install Dependencies

**Backend:**
```powershell
cd boutique-scarf-shop\backend
npm install
```

**Frontend:**
```powershell
cd boutique-scarf-shop\frontend
npm install
```

### 2. Set Up Database

**Install PostgreSQL** (if not already installed):
- Download from https://www.postgresql.org/download/windows/
- Or use Docker: `docker run --name postgres-boutique -e POSTGRES_PASSWORD=yourpassword -p 5432:5432 -d postgres:16`

**Create Database:**
```sql
CREATE DATABASE boutique_scarf_shop;
```

**Run Migrations:**
```powershell
# Connect to PostgreSQL
psql -U postgres -d boutique_scarf_shop

# Run the migration file
\i backend/migrations/001_initial_schema.sql
```

### 3. Configure Environment

**Backend Configuration:**

Create `backend/config/config.js` (copy from config.example.js):

```javascript
module.exports = {
  database: {
    host: 'localhost',
    port: 5432,
    name: 'boutique_scarf_shop',
    user: 'postgres',
    password: 'your_postgres_password'
  },
  server: {
    port: 3001,
    nodeEnv: 'development'
  },
  jwt: {
    secret: 'dev_secret_at_least_32_characters_long_change_in_prod',
    expiresIn: '24h'
  },
  // Optional: External services (can skip for initial testing)
  cloudinary: {
    cloudName: process.env.CLOUDINARY_CLOUD_NAME,
    apiKey: process.env.CLOUDINARY_API_KEY,
    apiSecret: process.env.CLOUDINARY_API_SECRET
  },
  stripe: {
    secretKey: process.env.STRIPE_SECRET_KEY || 'sk_test_your_key',
    publishableKey: process.env.STRIPE_PUBLISHABLE_KEY || 'pk_test_your_key',
    webhookSecret: process.env.STRIPE_WEBHOOK_SECRET
  },
  email: {
    provider: 'sendgrid',
    sendgrid: {
      apiKey: process.env.SENDGRID_API_KEY,
      fromEmail: 'noreply@localhost'
    }
  },
  cors: {
    origin: 'http://localhost:5173'
  }
};
```

**Or use environment variables** (create `.env` in backend folder):
```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=boutique_scarf_shop
DB_USER=postgres
DB_PASSWORD=your_postgres_password

PORT=3001
NODE_ENV=development

JWT_SECRET=dev_secret_at_least_32_characters_long_change_in_prod

FRONTEND_URL=http://localhost:5173

# Optional: Add these when ready to test external services
# CLOUDINARY_CLOUD_NAME=your_cloud_name
# CLOUDINARY_API_KEY=your_api_key
# CLOUDINARY_API_SECRET=your_api_secret

# STRIPE_SECRET_KEY=sk_test_your_stripe_key
# STRIPE_PUBLISHABLE_KEY=pk_test_your_stripe_key
# STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret

# SENDGRID_API_KEY=your_sendgrid_key
# SENDGRID_FROM_EMAIL=noreply@localhost
```

### 4. Start the Servers

**Backend (Terminal 1):**
```powershell
cd backend
npm run dev
```

You should see:
```
Database connected successfully
Server running on port 3001
```

**Frontend (Terminal 2):**
```powershell
cd frontend
npm run dev
```

You should see:
```
VITE ready in XXX ms
➜  Local:   http://localhost:5173/
```

### 5. View the Application

**Open browser:**
- Frontend: http://localhost:5173
- Backend API: http://localhost:3001

**Test the API:**
```powershell
# Test health check (you can add a simple GET / route that returns { status: 'ok' })
curl http://localhost:3001/

# Register a user
curl -X POST http://localhost:3001/api/auth/register -H "Content-Type: application/json" -d "{\"email\":\"test@example.com\",\"password\":\"Test123456\",\"firstName\":\"Test\",\"lastName\":\"User\"}"

# Login
curl -X POST http://localhost:3001/api/auth/login -H "Content-Type: application/json" -d "{\"email\":\"test@example.com\",\"password\":\"Test123456\"}"
```

## Testing Without Frontend

While frontend is being built, you can test the API directly:

### Using PowerShell:
```powershell
# Register
$body = @{
    email = "admin@test.com"
    password = "Admin123456"
    firstName = "Admin"
    lastName = "User"
} | ConvertTo-Json

Invoke-RestMethod -Uri http://localhost:3001/api/auth/register -Method Post -Body $body -ContentType "application/json"

# Login
$loginBody = @{
    email = "admin@test.com"
    password = "Admin123456"
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri http://localhost:3001/api/auth/login -Method Post -Body $loginBody -ContentType "application/json"
$token = $response.token

# Get products (public)
Invoke-RestMethod -Uri http://localhost:3001/api/products -Method Get

# Get cart (protected - needs token)
$headers = @{
    Authorization = "Bearer $token"
}
Invoke-RestMethod -Uri http://localhost:3001/api/cart -Method Get -Headers $headers
```

### Using a REST client:
- Install **Postman**, **Insomnia**, or **Thunder Client** (VS Code extension)
- Import the endpoints listed below

## API Endpoints Reference

### Authentication (Public)
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/me` - Get current user (protected)
- `PUT /api/auth/profile` - Update profile (protected)

### Products
- `GET /api/products` - List all products (public)
- `GET /api/products/:id` - Get product details (public)
- `POST /api/products` - Create product (admin)
- `PUT /api/products/:id` - Update product (admin)
- `DELETE /api/products/:id` - Delete product (admin)
- `POST /api/products/:id/images` - Upload image (admin)

### Shopping Cart (Protected)
- `GET /api/cart` - Get cart
- `POST /api/cart/items` - Add item
- `PUT /api/cart/items/:id` - Update quantity
- `DELETE /api/cart/items/:id` - Remove item
- `DELETE /api/cart` - Clear cart
- `POST /api/cart/validate` - Validate before checkout

### Payments (Protected)
- `POST /api/payments/create-checkout-session` - Create Stripe session
- `POST /api/payments/webhook` - Stripe webhook (public)
- `GET /api/payments/session/:id` - Get session details

### Orders (Protected)
- `GET /api/orders` - Get user's orders
- `GET /api/orders/:id` - Get specific order
- `GET /api/orders/admin/all` - Get all orders (admin)
- `PUT /api/orders/:id/status` - Update status (admin)

## Running Tests

```powershell
# Backend tests
cd backend
npm test

# Frontend tests
cd frontend
npm test
```

## Default Admin Credentials

The database migration creates a default admin account:
- **Email:** admin@boutique-scarves.com
- **Password:** admin123

**⚠️ IMPORTANT:** Change this password immediately after first login!

## Troubleshooting

### Database Connection Error
```
Error: connect ECONNREFUSED 127.0.0.1:5432
```
**Solution:** Ensure PostgreSQL is running:
```powershell
# Check if PostgreSQL service is running
Get-Service -Name postgresql*

# Start if not running
Start-Service -Name postgresql-x64-16
```

### Port Already in Use
```
Error: listen EADDRINUSE: address already in use :::3001
```
**Solution:** Change port in config.js or kill the process:
```powershell
# Find process using port 3001
netstat -ano | findstr :3001

# Kill process (replace PID with actual process ID)
taskkill /PID <PID> /F
```

### CORS Error
```
Access to fetch has been blocked by CORS policy
```
**Solution:** Ensure backend config has correct frontend URL:
```javascript
cors: {
  origin: 'http://localhost:5173'
}
```

### Missing Dependencies
```
Error: Cannot find module 'express'
```
**Solution:** Run npm install again:
```powershell
npm install
```

## External Services Setup (Optional)

### Cloudinary (Image Hosting)
1. Create free account at https://cloudinary.com
2. Get credentials from Dashboard
3. Add to config.js or .env

### Stripe (Payments)
1. Create account at https://stripe.com
2. Get test API keys from Dashboard
3. Add to config.js or .env
4. Use test card: 4242 4242 4242 4242

### SendGrid (Email)
1. Create account at https://sendgrid.com
2. Create API key
3. Add to config.js or .env

## Production Deployment

See `EXECUTION_REPORT.md` section "Recommendations > For Deployment"

## Need Help?

- Check `EXECUTION_REPORT.md` for comprehensive documentation
- Review `docs/TECH_STACK.md` for architecture details
- See `docs/DATABASE_SCHEMA.md` for database structure
- Read `docs/AUTHENTICATION_ARCHITECTURE.md` for auth flow

---

**Quick Commands Summary:**
```powershell
# Setup
cd backend && npm install
cd frontend && npm install

# Run
cd backend && npm run dev    # Terminal 1
cd frontend && npm run dev   # Terminal 2

# Test
cd backend && npm test
```

**Access:**
- Frontend: http://localhost:5173
- Backend: http://localhost:3001
- Admin: admin@boutique-scarves.com / admin123

