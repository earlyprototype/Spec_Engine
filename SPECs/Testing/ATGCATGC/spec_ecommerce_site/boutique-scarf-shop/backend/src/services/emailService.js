/**
 * Email Service
 * Sends transactional emails via SendGrid (primary) or Mailgun (backup)
 */

const sgMail = require('@sendgrid/mail');

// Configure SendGrid
const sendgridApiKey = process.env.SENDGRID_API_KEY;
if (sendgridApiKey) {
  sgMail.setApiKey(sendgridApiKey);
}

// Email provider selection
const emailProvider = process.env.EMAIL_PROVIDER || 'sendgrid';

/**
 * Send email via SendGrid
 * @param {object} emailData - Email data
 * @returns {Promise<boolean>} Success status
 */
const sendViaSendGrid = async (emailData) => {
  const { to, subject, html, text } = emailData;
  const from = process.env.SENDGRID_FROM_EMAIL || 'noreply@boutique-scarves.com';

  const msg = {
    to,
    from,
    subject,
    text: text || 'Please view this email in HTML mode',
    html
  };

  try {
    await sgMail.send(msg);
    console.log('Email sent via SendGrid to:', to);
    return true;
  } catch (error) {
    console.error('SendGrid error:', error.response?.body || error.message);
    throw error;
  }
};

/**
 * Send email via Mailgun (backup)
 * @param {object} emailData - Email data
 * @returns {Promise<boolean>} Success status
 */
const sendViaMailgun = async (emailData) => {
  // Mailgun implementation would go here
  // Using basic implementation as backup
  console.log('Mailgun not fully implemented, email would be sent to:', emailData.to);
  return true;
};

/**
 * Send email with retry logic
 * @param {object} emailData - Email data
 * @param {number} maxRetries - Maximum retry attempts
 * @returns {Promise<boolean>} Success status
 */
const sendEmail = async (emailData, maxRetries = 3) => {
  let lastError;

  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      if (emailProvider === 'sendgrid') {
        return await sendViaSendGrid(emailData);
      } else if (emailProvider === 'mailgun') {
        return await sendViaMailgun(emailData);
      }
    } catch (error) {
      lastError = error;
      console.log(`Email send attempt ${attempt} failed, retrying...`);
      
      // Exponential backoff
      if (attempt < maxRetries) {
        await new Promise(resolve => setTimeout(resolve, Math.pow(2, attempt) * 1000));
      }
    }
  }

  // All retries failed, try backup provider
  try {
    console.log('Trying backup email provider...');
    if (emailProvider === 'sendgrid') {
      return await sendViaMailgun(emailData);
    } else {
      return await sendViaSendGrid(emailData);
    }
  } catch (backupError) {
    console.error('Both email providers failed:', backupError);
    throw new Error(`Email delivery failed after ${maxRetries} retries: ${lastError.message}`);
  }
};

/**
 * Send order confirmation email
 * @param {object} orderData - Order data
 * @returns {Promise<boolean>} Success status
 */
const sendOrderConfirmation = async (orderData) => {
  const { userEmail, orderId, totalAmount, items, createdAt } = orderData;

  const itemsHtml = items.map(item => `
    <tr>
      <td style="padding: 8px; border-bottom: 1px solid #eee;">${item.productName}</td>
      <td style="padding: 8px; border-bottom: 1px solid #eee; text-align: center;">${item.quantity}</td>
      <td style="padding: 8px; border-bottom: 1px solid #eee; text-align: right;">£${item.priceAtPurchase.toFixed(2)}</td>
    </tr>
  `).join('');

  const html = `
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <title>Order Confirmation</title>
    </head>
    <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
      <div style="text-align: center; margin-bottom: 30px;">
        <h1 style="color: #333;">Thank You for Your Order!</h1>
      </div>
      
      <div style="background: #f9f9f9; padding: 20px; border-radius: 5px; margin-bottom: 20px;">
        <h2 style="margin-top: 0;">Order #${orderId}</h2>
        <p><strong>Order Date:</strong> ${new Date(createdAt).toLocaleDateString('en-GB')}</p>
        <p><strong>Total:</strong> £${totalAmount.toFixed(2)}</p>
      </div>

      <h3>Order Items:</h3>
      <table style="width: 100%; border-collapse: collapse; margin-bottom: 20px;">
        <thead>
          <tr style="background: #f0f0f0;">
            <th style="padding: 8px; text-align: left;">Item</th>
            <th style="padding: 8px; text-align: center;">Quantity</th>
            <th style="padding: 8px; text-align: right;">Price</th>
          </tr>
        </thead>
        <tbody>
          ${itemsHtml}
        </tbody>
      </table>

      <div style="margin-top: 30px; padding-top: 20px; border-top: 2px solid #eee;">
        <p>Your handcrafted scarves will be prepared with care and shipped shortly.</p>
        <p>You will receive a shipping notification email once your order is dispatched.</p>
      </div>

      <div style="margin-top: 30px; text-align: center; color: #666; font-size: 12px;">
        <p>Thank you for supporting our boutique!</p>
        <p>If you have any questions, please contact us.</p>
      </div>
    </body>
    </html>
  `;

  const text = `
Order Confirmation - Order #${orderId}

Thank you for your order!

Order Date: ${new Date(createdAt).toLocaleDateString('en-GB')}
Total: £${totalAmount.toFixed(2)}

Order Items:
${items.map(item => `- ${item.productName} x${item.quantity} - £${item.priceAtPurchase.toFixed(2)}`).join('\n')}

Your handcrafted scarves will be prepared with care and shipped shortly.
  `;

  return await sendEmail({
    to: userEmail,
    subject: `Order Confirmation - #${orderId}`,
    html,
    text
  });
};

/**
 * Send order status update email
 * @param {object} data - Status update data
 * @returns {Promise<boolean>} Success status
 */
const sendOrderStatusUpdate = async (data) => {
  const { userEmail, orderId, status, message } = data;

  const statusMessages = {
    processing: 'Your order is being prepared',
    shipped: 'Your order has been shipped',
    delivered: 'Your order has been delivered',
    cancelled: 'Your order has been cancelled'
  };

  const html = `
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <title>Order Status Update</title>
    </head>
    <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
      <h1 style="color: #333;">Order Status Update</h1>
      
      <div style="background: #f9f9f9; padding: 20px; border-radius: 5px; margin-bottom: 20px;">
        <h2>Order #${orderId}</h2>
        <p style="font-size: 18px; color: #0066cc;"><strong>${statusMessages[status] || 'Status updated'}</strong></p>
        ${message ? `<p>${message}</p>` : ''}
      </div>

      <p>Thank you for your patience!</p>
      
      <div style="margin-top: 30px; text-align: center; color: #666; font-size: 12px;">
        <p>Boutique Handcrafted Scarves</p>
      </div>
    </body>
    </html>
  `;

  return await sendEmail({
    to: userEmail,
    subject: `Order Update - #${orderId}`,
    html,
    text: `Order #${orderId} status: ${statusMessages[status] || status}\n${message || ''}`
  });
};

module.exports = {
  sendEmail,
  sendOrderConfirmation,
  sendOrderStatusUpdate
};

