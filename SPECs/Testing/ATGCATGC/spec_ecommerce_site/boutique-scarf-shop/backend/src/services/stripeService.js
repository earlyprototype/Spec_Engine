/**
 * Stripe Payment Service
 * Handles payment processing via Stripe API
 */

const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);

/**
 * Create Stripe checkout session
 * @param {object} data - Checkout data (userId, items, total)
 * @returns {Promise<object>} Checkout session
 */
const createCheckoutSession = async (data) => {
  const { userId, items, successUrl, cancelUrl } = data;

  // Format line items for Stripe
  const lineItems = items.map(item => ({
    price_data: {
      currency: 'gbp',
      product_data: {
        name: item.productName,
        description: item.description || 'Handcrafted boutique scarf'
      },
      unit_amount: Math.round(item.priceAtAddition * 100) // Convert to pence
    },
    quantity: item.quantity
  }));

  try {
    const session = await stripe.checkout.sessions.create({
      payment_method_types: ['card'],
      line_items: lineItems,
      mode: 'payment',
      success_url: successUrl || `${process.env.FRONTEND_URL}/checkout/success?session_id={CHECKOUT_SESSION_ID}`,
      cancel_url: cancelUrl || `${process.env.FRONTEND_URL}/checkout/cancel`,
      customer_email: data.customerEmail,
      metadata: {
        userId: userId.toString(),
        cartId: data.cartId?.toString() || 'unknown'
      },
      shipping_address_collection: {
        allowed_countries: ['GB', 'US', 'CA', 'AU', 'FR', 'DE', 'IT', 'ES']
      }
    });

    return {
      sessionId: session.id,
      url: session.url
    };

  } catch (error) {
    console.error('Stripe checkout session creation error:', error);
    throw new Error(`Payment session creation failed: ${error.message}`);
  }
};

/**
 * Create payment intent (alternative flow)
 * @param {object} data - Payment data
 * @returns {Promise<object>} Payment intent
 */
const createPaymentIntent = async (data) => {
  const { amount, currency = 'gbp', metadata = {} } = data;

  try {
    const paymentIntent = await stripe.paymentIntents.create({
      amount: Math.round(amount * 100), // Convert to pence
      currency,
      metadata,
      automatic_payment_methods: {
        enabled: true
      }
    });

    return {
      clientSecret: paymentIntent.client_secret,
      paymentIntentId: paymentIntent.id
    };

  } catch (error) {
    console.error('Stripe payment intent creation error:', error);
    throw new Error(`Payment intent creation failed: ${error.message}`);
  }
};

/**
 * Verify webhook signature
 * @param {string} payload - Webhook payload
 * @param {string} signature - Stripe signature header
 * @returns {object} Verified event
 */
const verifyWebhookSignature = (payload, signature) => {
  const webhookSecret = process.env.STRIPE_WEBHOOK_SECRET;

  if (!webhookSecret) {
    throw new Error('Webhook secret not configured');
  }

  try {
    const event = stripe.webhooks.constructEvent(payload, signature, webhookSecret);
    return event;
  } catch (error) {
    console.error('Webhook signature verification failed:', error);
    throw new Error(`Webhook verification failed: ${error.message}`);
  }
};

/**
 * Retrieve checkout session
 * @param {string} sessionId - Checkout session ID
 * @returns {Promise<object>} Session details
 */
const getCheckoutSession = async (sessionId) => {
  try {
    const session = await stripe.checkout.sessions.retrieve(sessionId, {
      expand: ['payment_intent']
    });

    return {
      id: session.id,
      paymentStatus: session.payment_status,
      paymentIntentId: session.payment_intent?.id,
      customerEmail: session.customer_email,
      amountTotal: session.amount_total / 100, // Convert from pence
      currency: session.currency,
      metadata: session.metadata
    };

  } catch (error) {
    console.error('Stripe session retrieval error:', error);
    throw new Error(`Session retrieval failed: ${error.message}`);
  }
};

/**
 * Refund payment
 * @param {string} paymentIntentId - Payment intent ID
 * @param {number} amount - Refund amount (optional, full refund if not specified)
 * @returns {Promise<object>} Refund details
 */
const createRefund = async (paymentIntentId, amount = null) => {
  try {
    const refundData = {
      payment_intent: paymentIntentId
    };

    if (amount) {
      refundData.amount = Math.round(amount * 100); // Convert to pence
    }

    const refund = await stripe.refunds.create(refundData);

    return {
      id: refund.id,
      amount: refund.amount / 100,
      status: refund.status
    };

  } catch (error) {
    console.error('Stripe refund creation error:', error);
    throw new Error(`Refund failed: ${error.message}`);
  }
};

module.exports = {
  createCheckoutSession,
  createPaymentIntent,
  verifyWebhookSignature,
  getCheckoutSession,
  createRefund
};

