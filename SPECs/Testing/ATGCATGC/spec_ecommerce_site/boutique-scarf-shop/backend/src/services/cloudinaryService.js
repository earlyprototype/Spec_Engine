/**
 * Cloudinary Service
 * Image upload and management
 */

const cloudinary = require('cloudinary').v2;

// Configure Cloudinary
cloudinary.config({
  cloud_name: process.env.CLOUDINARY_CLOUD_NAME,
  api_key: process.env.CLOUDINARY_API_KEY,
  api_secret: process.env.CLOUDINARY_API_SECRET
});

/**
 * Upload image to Cloudinary
 * @param {string} imagePath - Local file path or base64 data URI
 * @param {object} options - Upload options
 * @returns {Promise<object>} Upload result with URL and public_id
 */
const uploadImage = async (imagePath, options = {}) => {
  try {
    const uploadOptions = {
      folder: 'boutique-scarves',
      resource_type: 'image',
      transformation: [
        { width: 1000, height: 1000, crop: 'limit' }, // Max dimensions
        { quality: 'auto' }, // Auto quality optimization
        { fetch_format: 'auto' } // Auto format (WebP when supported)
      ],
      ...options
    };

    const result = await cloudinary.uploader.upload(imagePath, uploadOptions);

    return {
      publicId: result.public_id,
      url: result.secure_url,
      width: result.width,
      height: result.height,
      format: result.format
    };
  } catch (error) {
    console.error('Cloudinary upload error:', error);
    throw new Error(`Image upload failed: ${error.message}`);
  }
};

/**
 * Delete image from Cloudinary
 * @param {string} publicId - Cloudinary public ID
 * @returns {Promise<object>} Deletion result
 */
const deleteImage = async (publicId) => {
  try {
    const result = await cloudinary.uploader.destroy(publicId);
    return result;
  } catch (error) {
    console.error('Cloudinary delete error:', error);
    throw new Error(`Image deletion failed: ${error.message}`);
  }
};

/**
 * Get image URL with transformations
 * @param {string} publicId - Cloudinary public ID
 * @param {object} transformations - Transformation options
 * @returns {string} Transformed image URL
 */
const getImageUrl = (publicId, transformations = {}) => {
  return cloudinary.url(publicId, {
    transformation: [transformations],
    secure: true
  });
};

/**
 * Test Cloudinary connection
 * @returns {Promise<boolean>} True if connection successful
 */
const testConnection = async () => {
  try {
    // Attempt to get account details as connection test
    await cloudinary.api.ping();
    return true;
  } catch (error) {
    console.error('Cloudinary connection failed:', error);
    return false;
  }
};

module.exports = {
  uploadImage,
  deleteImage,
  getImageUrl,
  testConnection
};

