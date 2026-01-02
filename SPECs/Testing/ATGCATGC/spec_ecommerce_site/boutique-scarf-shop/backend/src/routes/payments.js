/**
 * Payment Routes
 * Stripe payment processing endpoints
 */

const express = require('express');
const stripeService = require('../services/stripeService');
const cartService = require('../services/cartService');
const orderService = require('../services/orderService');
const emailService = require('../services/emailService');
const authMiddleware = require('../middleware/auth');
const db = require('../utils/database');

const router = express.Router();

/**
 * POST /api/payments/create-checkout-session
 * Create Stripe checkout session (protected)
 */
router.post('/create-checkout-session', authMiddleware, async (req, res) => {
  try {
    // Get user's cart
    const cart = await cartService.getCart(req.user.userId);

    if (cart.items.length === 0) {
      return res.status(400).json({
        success: false,
        message: 'Cart is empty'
      });
    }

    // Validate cart
    const validation = await cartService.validateCart(req.user.userId);
    if (!validation.valid) {
      return res.status(400).json({
        success: false,
        message: 'Cart validation failed',
        errors: validation.errors
      });
    }

    // Create checkout session
    const session = await stripeService.createCheckoutSession({
      userId: req.user.userId,
      items: cart.items,
      cartId: cart.cartId,
      customerEmail: req.user.email,
      successUrl: req.body.successUrl,
      cancelUrl: req.body.cancelUrl
    });

    res.status(200).json({
      success: true,
      sessionId: session.sessionId,
      url: session.url
    });

  } catch (error) {
    console.error('Create checkout session error:', error);
    res.status(500).json({
      success: false,
      message: error.message || 'Server error'
    });
  }
});

/**
 * POST /api/payments/webhook
 * Stripe webhook handler (public - verified by signature)
 * Handles payment success and creates order
 */
router.post('/webhook', express.raw({ type: 'application/json' }), async (req, res) => {
  const signature = req.headers['stripe-signature'];

  try {
    // Verify webhook signature
    const event = stripeService.verifyWebhookSignature(req.body, signature);

    // Handle different event types
    switch (event.type) {
      case 'checkout.session.completed': {
        const session = event.data.object;

        // Get full session details
        const sessionDetails = await stripeService.getCheckoutSession(session.id);

        if (sessionDetails.paymentStatus === 'paid') {
          const userId = parseInt(sessionDetails.metadata.userId);

          // Get cart items
          const cart = await cartService.getCart(userId);

          // Create order
          const order = await orderService.createOrder({
            userId,
            stripePaymentIntentId: sessionDetails.paymentIntentId,
            totalAmount: sessionDetails.amountTotal,
            items: cart.items,
            shippingAddressId: null // Will be enhanced in Task 6
          });

          // Clear cart
          await cartService.clearCart(userId);

          console.log('Order created successfully:', order.id);

          // Send order confirmation email
          try {
            const userQuery = 'SELECT email FROM users WHERE id = $1';
            const userResult = await db.query(userQuery, [userId]);
            const userEmail = userResult.rows[0]?.email;

            if (userEmail) {
              await emailService.sendOrderConfirmation({
                userEmail,
                orderId: order.id,
                totalAmount: order.totalAmount,
                items: cart.items,
                createdAt: order.createdAt
              });
              console.log('Order confirmation email sent to:', userEmail);
            }
          } catch (emailError) {
            console.error('Failed to send confirmation email:', emailError);
            // Don't fail the webhook if email fails
          }
        }
        break;
      }

      case 'payment_intent.payment_failed': {
        const paymentIntent = event.data.object;
        console.error('Payment failed:', paymentIntent.id);
        // Could send notification to user
        break;
      }

      default:
        console.log(`Unhandled event type: ${event.type}`);
    }

    // Return 200 to acknowledge receipt
    res.status(200).json({ received: true });

  } catch (error) {
    console.error('Webhook error:', error);
    res.status(400).json({
      success: false,
      message: `Webhook error: ${error.message}`
    });
  }
});

/**
 * GET /api/payments/session/:sessionId
 * Get checkout session details (protected)
 */
router.get('/session/:sessionId', authMiddleware, async (req, res) => {
  try {
    const sessionDetails = await stripeService.getCheckoutSession(req.params.sessionId);

    res.status(200).json({
      success: true,
      session: sessionDetails
    });

  } catch (error) {
    console.error('Get session error:', error);
    res.status(500).json({
      success: false,
      message: error.message || 'Server error'
    });
  }
});

module.exports = router;

