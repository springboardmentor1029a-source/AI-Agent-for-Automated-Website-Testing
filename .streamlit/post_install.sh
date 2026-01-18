#!/bin/bash
# Post-install script for Streamlit Cloud
# This installs Playwright browsers after pip install completes

echo "Installing Playwright browsers..."
playwright install chromium --with-deps || playwright install chromium
echo "Playwright installation complete"
