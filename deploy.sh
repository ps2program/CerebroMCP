#!/bin/bash

# Navigate to the docs-site directory
cd "$(dirname "$0")"

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "Error: Node.js is not installed. Please install Node.js 18.0 or higher."
    exit 1
fi

# Check Node.js version
NODE_VERSION=$(node -v | cut -d'v' -f2)
REQUIRED_VERSION="18.0.0"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$NODE_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo "Error: Node.js version $NODE_VERSION is not supported. Please install Node.js 18.0 or higher."
    exit 1
fi

# Install dependencies if node_modules doesn't exist
if [ ! -d "node_modules" ]; then
    echo "Installing dependencies..."
    npm install
fi

# Build the site
echo "Building the site..."
npm run build

# Check if build was successful
if [ $? -eq 0 ]; then
    echo "Build successful!"
    echo "The site has been built in the 'build' directory."
    echo "To deploy to GitHub Pages:"
    echo "1. Commit and push your changes to GitHub"
    echo "2. The GitHub Action will automatically deploy your site"
    echo "3. Your site will be available at: https://ps2program.github.io/CerebroMCP/"
else
    echo "Build failed. Please check the error messages above."
    exit 1
fi 