# Boutique Handcrafted Scarf Shop

An e-commerce platform for selling fine handcrafted scarves.

## Quick Start Scripts

### Full Setup (with Database)
```powershell
.\start-with-database.ps1
```

**What it does:**
- Checks prerequisites (Node.js, PostgreSQL)
- Installs all dependencies
- Sets up PostgreSQL database
- Runs database migrations
- Creates backend configuration
- Starts both backend and frontend servers
- Opens browser to http://localhost:5173

**Prerequisites:**
- Node.js 18+
- PostgreSQL 14+
- PowerShell (Windows)

---

### Quick Test (without Database)
```powershell
.\start-without-database.ps1
```

**What it does:**
- Checks prerequisites (Node.js only)
- Installs dependencies
- Creates minimal configuration
- Starts both servers
- Opens browser

**What works:**
- Server health check
- Frontend displays
- API structure accessible

**What doesn't work:**
- User authentication
- Product management
- Shopping cart
- Orders
- Any database operations

**Use this mode to:**
- Test server setup quickly
- Verify API routing
- Check frontend without data
- Debug server configuration issues

---

## Manual Setup

If you prefer manual setup or the scripts don't work:

### 1. Install Dependencies
```powershell
cd backend
npm install

cd ..\frontend
npm install
```

### 2. Set Up Database
```sql
CREATE DATABASE boutique_scarf_shop;
\i backend/migrations/001_initial_schema.sql
```

### 3. Configure Backend
Create `backend/config/config.js` (see `backend/config/config.example.js`)

### 4. Start Servers
```powershell
# Terminal 1
cd backend
npm run dev

# Terminal 2
cd frontend
npm run dev
```

### 5. Open Browser
- Frontend: http://localhost:5173
- Backend: http://localhost:3001

---

## Project Structure

```
boutique-scarf-shop/
├── backend/                 # Node.js/Express API
│   ├── config/             # Configuration files
│   ├── migrations/         # Database schema
│   ├── src/
│   │   ├── middleware/     # Auth, RBAC middleware
│   │   ├── routes/         # API endpoints
│   │   ├── services/       # Business logic
│   │   └── utils/          # Helper functions
│   └── tests/              # Jest tests
├── frontend/               # React/Vite application
│   ├── public/
│   ├── src/
│   └── tests/
├── docs/                   # Documentation
├── start-with-database.ps1
├── start-without-database.ps1
└── SETUP_GUIDE.md          # Detailed setup instructions
```

---

## Technology Stack

**Frontend:**
- React 18
- Vite
- React Router
- Axios

**Backend:**
- Node.js
- Express
- PostgreSQL
- JWT Authentication
- Bcrypt

**External Services:**
- Stripe (Payments)
- Cloudinary (Image hosting)
- SendGrid/Mailgun (Email)

---

## Default Credentials

After running migrations, a default admin account is created:
- **Email:** admin@boutique-scarves.com
- **Password:** admin123

**⚠️ Change this immediately after first login!**

---

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login
- `GET /api/auth/me` - Get current user (protected)

### Products
- `GET /api/products` - List products
- `POST /api/products` - Create product (admin)
- `GET /api/products/:id` - Get product details

### Shopping Cart
- `GET /api/cart` - Get cart (protected)
- `POST /api/cart/items` - Add item (protected)
- `DELETE /api/cart` - Clear cart (protected)

### Payments
- `POST /api/payments/create-checkout-session` - Stripe checkout (protected)

### Orders
- `GET /api/orders` - Get user orders (protected)
- `GET /api/orders/admin/all` - All orders (admin)

---

## Testing

```powershell
# Backend tests
cd backend
npm test

# Frontend tests
cd frontend
npm test
```

---

## Documentation

- **SETUP_GUIDE.md** - Complete setup and configuration guide
- **EXECUTION_REPORT.md** - Full project documentation and architecture
- **docs/TECH_STACK.md** - Technology choices and rationale
- **docs/DATABASE_SCHEMA.md** - Database structure
- **docs/AUTHENTICATION_ARCHITECTURE.md** - Auth flow and security

---

## Troubleshooting

### "Cannot find module"
```powershell
npm install
```

### "Database connection failed"
Check PostgreSQL is running:
```powershell
Get-Service -Name postgresql*
```

### "Port already in use"
Change port in config or kill process:
```powershell
netstat -ano | findstr :3001
taskkill /PID <PID> /F
```

### Scripts won't run
Enable PowerShell script execution:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## Development

### Backend Development
```powershell
cd backend
npm run dev  # Auto-reload with nodemon
```

### Frontend Development
```powershell
cd frontend
npm run dev  # Hot module reload
```

### Linting
```powershell
npm run lint
```

### Format Code
```powershell
npm run format
```

---

## Production Deployment

See **EXECUTION_REPORT.md** section "Recommendations > For Deployment" for:
- Environment variable configuration
- Database security hardening
- SSL/TLS setup
- CDN configuration
- Monitoring and logging
- Backup strategies

---

## Project DNA: ATGCATGC

This project was generated using the SPEC framework. For more information about the development process and execution details, see:
- `../EXECUTION_REPORT.md`
- `../spec_ecommerce_site.md`
- `../exe_ecommerce_site.md`

---

## Support

For issues or questions:
1. Check **SETUP_GUIDE.md** for detailed instructions
2. Review **EXECUTION_REPORT.md** for architecture details
3. Check logs in console for error messages
4. Verify all prerequisites are installed

---

## License

Proprietary - Boutique Handcrafted Scarves

---

**Built with the SPEC Framework**  
DNA Code: ATGCATGC

