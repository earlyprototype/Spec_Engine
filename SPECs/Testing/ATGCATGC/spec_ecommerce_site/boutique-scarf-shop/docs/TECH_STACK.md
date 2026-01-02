# Technology Stack - Boutique Scarf Shop

## Frontend
- **Framework:** React 18.x
- **Build Tool:** Vite 5.x
- **State Management:** React Context API + Hooks
- **Routing:** React Router v6
- **HTTP Client:** Axios
- **Testing:** Jest + React Testing Library
- **Styling:** CSS Modules + modern CSS

## Backend
- **Runtime:** Node.js 20.x LTS
- **Framework:** Express 4.x
- **Database:** PostgreSQL 16.x
- **ORM:** node-postgres (pg)
- **Authentication:** bcrypt + JWT (jsonwebtoken)
- **Testing:** Jest + Supertest
- **Validation:** express-validator

## External Services
- **Image Hosting:** Cloudinary
- **Payment Processing:** Stripe API
- **Email Service:** SendGrid (primary) / Mailgun (backup)

## Development Tools
- **Linting:** ESLint
- **Formatting:** Prettier
- **Version Control:** Git
- **Package Manager:** npm

## Database Schema
See `/docs/DATABASE_SCHEMA.md` for complete schema design.

## Testing Strategy
- **TDD Approach:** Write tests before implementation
- **Unit Tests:** All business logic functions
- **Integration Tests:** API endpoints, database operations
- **Coverage Target:** 80%+ for critical paths

## Security
- Passwords hashed with bcrypt (salt rounds: 10)
- JWT tokens for session management
- Environment variables for all credentials
- Input validation on all endpoints
- HTTPS in production
- Stripe for PCI-compliant payment handling

## Project Structure
```
boutique-scarf-shop/
├── backend/
│   ├── src/
│   │   ├── models/          # Database models
│   │   ├── routes/          # API route handlers
│   │   ├── middleware/      # Authentication, validation
│   │   ├── services/        # Business logic
│   │   └── server.js        # Entry point
│   ├── tests/               # Test files
│   ├── config/              # Configuration files
│   └── package.json
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── pages/           # Page components
│   │   ├── services/        # API calls
│   │   ├── utils/           # Helper functions
│   │   └── App.jsx          # Root component
│   ├── tests/               # Test files
│   ├── public/              # Static assets
│   └── package.json
└── docs/                    # Documentation
```

## Deployment Considerations
- Backend: Node.js hosting (Heroku, Railway, Render)
- Frontend: Static hosting (Vercel, Netlify)
- Database: Managed PostgreSQL (AWS RDS, Heroku Postgres)
- Environment: Separate dev/staging/production configs

---

**Generated:** 2025-11-02  
**Project:** ATGCATGC - scarf-boutique-ecommerce  
**SPEC:** spec_ecommerce_site

