import { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [apiStatus, setApiStatus] = useState('checking...');
  const [products, setProducts] = useState([]);

  useEffect(() => {
    // Check API health
    fetch('/api/')
      .then(res => res.json())
      .then(data => {
        setApiStatus(data.status === 'ok' ? 'Connected ✓' : 'Error');
      })
      .catch(() => {
        setApiStatus('Not connected - Start backend server');
      });

    // Fetch products
    fetch('/api/products')
      .then(res => res.json())
      .then(data => {
        if (data.success) {
          setProducts(data.products || []);
        }
      })
      .catch(err => console.error('Failed to fetch products:', err));
  }, []);

  return (
    <div className="App">
      <header className="header">
        <h1>Boutique Handcrafted Scarves</h1>
        <p className="tagline">Fine artisan scarves, lovingly created by hand</p>
        <div className="api-status">
          API Status: <span className={apiStatus.includes('✓') ? 'connected' : 'error'}>{apiStatus}</span>
        </div>
      </header>

      <main className="main">
        <section className="hero">
          <h2>Welcome to Our Boutique</h2>
          <p>Discover unique, handcrafted scarves made with passion and care</p>
        </section>

        <section className="features">
          <div className="feature-card">
            <h3>✨ Handcrafted Quality</h3>
            <p>Each scarf is carefully crafted by hand</p>
          </div>
          <div className="feature-card">
            <h3>🎨 Unique Designs</h3>
            <p>Original patterns you won't find elsewhere</p>
          </div>
          <div className="feature-card">
            <h3>🛍️ Secure Shopping</h3>
            <p>Safe payment processing via Stripe</p>
          </div>
        </section>

        <section className="products-section">
          <h2>Available Products</h2>
          {products.length > 0 ? (
            <div className="products-grid">
              {products.map(product => (
                <div key={product.id} className="product-card">
                  <div className="product-image-placeholder">
                    {product.images && product.images[0] ? (
                      <img src={product.images[0].url} alt={product.name} />
                    ) : (
                      <div className="no-image">No image</div>
                    )}
                  </div>
                  <h3>{product.name}</h3>
                  <p className="product-description">{product.description}</p>
                  <div className="product-footer">
                    <span className="price">£{product.price.toFixed(2)}</span>
                    <span className="stock">
                      {product.stockQuantity > 0 ? `${product.stockQuantity} in stock` : 'Out of stock'}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="empty-state">
              <p>No products available yet</p>
              <p className="hint">Admin can add products using the API</p>
            </div>
          )}
        </section>

        <section className="api-info">
          <h2>API Documentation</h2>
          <div className="api-endpoints">
            <h3>Available Endpoints:</h3>
            <ul>
              <li><code>POST /api/auth/register</code> - Create account</li>
              <li><code>POST /api/auth/login</code> - Login</li>
              <li><code>GET /api/products</code> - View products</li>
              <li><code>GET /api/cart</code> - View cart (auth required)</li>
              <li><code>POST /api/payments/create-checkout-session</code> - Checkout (auth required)</li>
            </ul>
            <p className="hint">
              See <strong>SETUP_GUIDE.md</strong> for full API documentation and testing instructions
            </p>
          </div>
        </section>

        <section className="setup-info">
          <h2>Development Status</h2>
          <div className="status-grid">
            <div className="status-item">
              <span className="status-icon">✓</span>
              <span>Backend API Complete</span>
            </div>
            <div className="status-item">
              <span className="status-icon">✓</span>
              <span>Database Schema Ready</span>
            </div>
            <div className="status-item">
              <span className="status-icon">✓</span>
              <span>Authentication Working</span>
            </div>
            <div className="status-item">
              <span className="status-icon">✓</span>
              <span>Payment Integration Ready</span>
            </div>
            <div className="status-item">
              <span className="status-icon">⚡</span>
              <span>Frontend UI (You are here!)</span>
            </div>
            <div className="status-item">
              <span className="status-icon">📝</span>
              <span>See EXECUTION_REPORT.md</span>
            </div>
          </div>
        </section>
      </main>

      <footer className="footer">
        <p>Boutique Handcrafted Scarves © 2025</p>
        <p>Built with React + Node.js + PostgreSQL + Stripe</p>
        <p className="dna">Project DNA: ATGCATGC</p>
      </footer>
    </div>
  );
}

export default App;

