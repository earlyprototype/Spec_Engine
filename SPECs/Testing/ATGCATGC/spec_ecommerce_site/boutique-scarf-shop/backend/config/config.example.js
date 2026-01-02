// Configuration Template
// Copy this to config/config.js and fill in your actual values
// DO NOT commit config.js - it should be in .gitignore

module.exports = {
  database: {
    host: process.env.DB_HOST || 'localhost',
    port: process.env.DB_PORT || 5432,
    name: process.env.DB_NAME || 'boutique_scarf_shop',
    user: process.env.DB_USER || 'your_username',
    password: process.env.DB_PASSWORD || 'your_password'
  },
  server: {
    port: process.env.PORT || 3001,
    nodeEnv: process.env.NODE_ENV || 'development'
  },
  jwt: {
    secret: process.env.JWT_SECRET || 'your_jwt_secret_min_32_chars',
    expiresIn: '24h'
  },
  cloudinary: {
    cloudName: process.env.CLOUDINARY_CLOUD_NAME,
    apiKey: process.env.CLOUDINARY_API_KEY,
    apiSecret: process.env.CLOUDINARY_API_SECRET
  },
  stripe: {
    secretKey: process.env.STRIPE_SECRET_KEY,
    publishableKey: process.env.STRIPE_PUBLISHABLE_KEY,
    webhookSecret: process.env.STRIPE_WEBHOOK_SECRET
  },
  email: {
    provider: 'sendgrid', // or 'mailgun'
    sendgrid: {
      apiKey: process.env.SENDGRID_API_KEY,
      fromEmail: process.env.SENDGRID_FROM_EMAIL || 'noreply@boutique-scarves.com'
    },
    mailgun: {
      apiKey: process.env.MAILGUN_API_KEY,
      domain: process.env.MAILGUN_DOMAIN
    }
  },
  cors: {
    origin: process.env.FRONTEND_URL || 'http://localhost:5173'
  }
};

