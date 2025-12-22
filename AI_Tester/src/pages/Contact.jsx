import React, { useState, useEffect } from 'react';
import { useTheme } from '../context/ThemeContext';
import '../styles/Contact.css';

const Contact = () => {
  const { theme } = useTheme();
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    company: '',
    message: '',
  });
  const [submitted, setSubmitted] = useState(false);

  useEffect(() => {
    document.title = 'Contact Us - Youval AutoQA';
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // Handle form submission here
    console.log('Form submitted:', formData);
    setSubmitted(true);
    
    // Reset form after 3 seconds
    setTimeout(() => {
      setFormData({ name: '', email: '', company: '', message: '' });
      setSubmitted(false);
    }, 3000);
  };

  return (
    <div className={`contact-container ${theme}`} data-theme={theme}>
      <div className="contact-wrapper">
        {/* Header */}
        <div className="contact-header">
          <h1>Get in Touch</h1>
          <p>We'd love to hear from you. Send us a message!</p>
        </div>

        <div className="contact-content">
          {/* Contact Form */}
          <div className="contact-form-section">
            <h2>Send us a Message</h2>
            
            {submitted ? (
              <div className="success-message">
                <span className="success-icon">✓</span>
                <h3>Thank you!</h3>
                <p>Your message has been sent successfully. We'll get back to you soon.</p>
              </div>
            ) : (
              <form onSubmit={handleSubmit} className="contact-form">
                <div className="form-group">
                  <label htmlFor="name">Full Name *</label>
                  <input
                    type="text"
                    id="name"
                    name="name"
                    value={formData.name}
                    onChange={handleChange}
                    placeholder="Your full name"
                    required
                  />
                </div>

                <div className="form-group">
                  <label htmlFor="email">Email Address *</label>
                  <input
                    type="email"
                    id="email"
                    name="email"
                    value={formData.email}
                    onChange={handleChange}
                    placeholder="your@email.com"
                    required
                  />
                </div>

                <div className="form-group">
                  <label htmlFor="company">Company</label>
                  <input
                    type="text"
                    id="company"
                    name="company"
                    value={formData.company}
                    onChange={handleChange}
                    placeholder="Your company name"
                  />
                </div>

                <div className="form-group">
                  <label htmlFor="message">Message *</label>
                  <textarea
                    id="message"
                    name="message"
                    value={formData.message}
                    onChange={handleChange}
                    placeholder="Tell us how we can help..."
                    rows="6"
                    required
                  />
                </div>

                <button type="submit" className="submit-btn">
                  Send Message
                </button>
              </form>
            )}
          </div>

          {/* Contact Information */}
          <div className="contact-info-section">
            <h2>Contact Information</h2>
            
            <div className="info-card">
              <span className="info-icon">📧</span>
              <div className="info-content">
                <h3>Email</h3>
                <p><a href="mailto:support@youvalautoqa.com">support@youvalautoqa.com</a></p>
                <p><a href="mailto:sales@youvalautoqa.com">sales@youvalautoqa.com</a></p>
              </div>
            </div>

            <div className="info-card">
              <span className="info-icon">💬</span>
              <div className="info-content">
                <h3>Chat Support</h3>
                <p>Available 24/7 for urgent queries</p>
                <p>Live chat on our website</p>
              </div>
            </div>

            <div className="info-card">
              <span className="info-icon">📱</span>
              <div className="info-content">
                <h3>Phone</h3>
                <p><a href="tel:+1-800-youval1">+1 (800) YOUVAL-1</a></p>
                <p>Monday - Friday: 9 AM - 6 PM EST</p>
              </div>
            </div>

            <div className="info-card">
              <span className="info-icon">📍</span>
              <div className="info-content">
                <h3>Office</h3>
                <p>Youval AutoQA Inc.</p>
                <p>Tech Hub, Innovation District</p>
                <p>San Francisco, CA 94105, USA</p>
              </div>
            </div>

            {/* Social Links */}
            <div className="social-links">
              <h3>Follow Us</h3>
              <div className="social-icons">
                <a href="#" className="social-icon" title="LinkedIn">
                  💼
                </a>
                <a href="#" className="social-icon" title="Twitter">
                  🐦
                </a>
                <a href="#" className="social-icon" title="GitHub">
                  💻
                </a>
                <a href="#" className="social-icon" title="Facebook">
                  👥
                </a>
              </div>
            </div>
          </div>
        </div>

        {/* FAQ Section */}
        <section className="contact-faq">
          <h2>Frequently Asked Questions</h2>
          
          <div className="faq-grid">
            <div className="faq-item">
              <h3>How quickly will you respond?</h3>
              <p>
                We aim to respond to all inquiries within 24 hours. For urgent matters, 
                please use our chat support or call our hotline.
              </p>
            </div>

            <div className="faq-item">
              <h3>Do you offer trial access?</h3>
              <p>
                Yes! Sign up for a free 14-day trial of Youval AutoQA. 
                No credit card required to get started.
              </p>
            </div>

            <div className="faq-item">
              <h3>What support do you provide?</h3>
              <p>
                We offer email support, live chat, phone support, and comprehensive 
                documentation to help you succeed.
              </p>
            </div>

            <div className="faq-item">
              <h3>Can I request a demo?</h3>
              <p>
                Absolutely! We'd love to show you how Youval AutoQA can transform 
                your testing process. Request a demo in the form above.
              </p>
            </div>

            <div className="faq-item">
              <h3>What are your pricing plans?</h3>
              <p>
                We offer flexible pricing for teams of all sizes. 
                Visit our pricing page for detailed information.
              </p>
            </div>

            <div className="faq-item">
              <h3>Do you offer enterprise solutions?</h3>
              <p>
                Yes! We offer customized enterprise packages with dedicated support, 
                SLA guarantees, and on-premise deployment options.
              </p>
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="contact-cta">
          <h2>Ready to Get Started?</h2>
          <p>Transform your testing process with Youval AutoQA today</p>
          <a href="/data-input" className="cta-button">Start Free Trial</a>
        </section>
      </div>
    </div>
  );
};

export default Contact;
