#!/bin/bash
# setup.sh
# Unix/Linux/macOS setup script for Pattern Extraction Pipeline

echo "=== Pattern Extraction Pipeline Setup ==="

# Check if Docker is installed
echo ""
echo "Checking Docker installation..."
if command -v docker &> /dev/null; then
    echo "✓ Docker is installed"
    docker --version
else
    echo "✗ Docker is not installed"
    echo "Please install Docker from: https://www.docker.com/products/docker-desktop"
    exit 1
fi

# Check if Python is installed
echo ""
echo "Checking Python installation..."
if command -v python3 &> /dev/null; then
    echo "✓ Python is installed"
    python3 --version
else
    echo "✗ Python is not installed"
    echo "Please install Python 3.8+ from: https://www.python.org/downloads/"
    exit 1
fi

# Start Neo4j container
echo ""
echo "Starting Neo4j container..."
docker run -d \
    --name spec-engine-graph \
    -p 7474:7474 -p 7687:7687 \
    -e NEO4J_AUTH=neo4j/password \
    neo4j

if [ $? -eq 0 ]; then
    echo "✓ Neo4j container started"
    echo "  Browser UI: http://localhost:7474"
    echo "  Username: neo4j"
    echo "  Password: password"
else
    echo "⚠ Neo4j container may already exist or Docker is not running"
    echo "  Try: docker start spec-engine-graph"
fi

# Install Python dependencies
echo ""
echo "Installing Python dependencies..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✓ Python dependencies installed"
else
    echo "✗ Failed to install dependencies"
    exit 1
fi

# Check if .env exists
echo ""
echo "Checking environment configuration..."
if [ -f .env ]; then
    echo "✓ .env file exists"
else
    echo "⚠ .env file not found"
    echo "Creating .env from template..."
    cp env.template .env
    echo "✓ Created .env file"
    echo ""
    echo "IMPORTANT: Edit .env and add your credentials:"
    echo "  - GITHUB_TOKEN (get from: https://github.com/settings/tokens)"
    echo "  - OPENAI_API_KEY (get from: https://platform.openai.com/api-keys)"
fi

# Wait for Neo4j to be ready
echo ""
echo "Waiting for Neo4j to be ready (30 seconds)..."
sleep 30
echo "✓ Neo4j should be ready now"

# Final instructions
echo ""
echo "=== Setup Complete ==="
echo ""
echo "Next steps:"
echo "1. Edit .env and add your API keys"
echo "2. Run: python3 test_extraction.py (test single repo extraction)"
echo "3. Run: python3 test_query.py (test graph queries)"
echo "4. Run: python3 pattern_extractor.py (extract 20 patterns)"
echo ""
echo "To stop Neo4j: docker stop spec-engine-graph"
echo "To start Neo4j: docker start spec-engine-graph"
