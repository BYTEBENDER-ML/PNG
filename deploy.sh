#!/bin/bash

# Engagement Chatbot Deployment Script
# This script helps deploy the application to various platforms

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to create .env file
create_env_file() {
    if [ ! -f .env ]; then
        print_status "Creating .env file..."
        cat > .env << EOF
# Production Environment Variables
SECRET_KEY=$(openssl rand -hex 32)
DATABASE_PATH=./data/engagement_data.db
DEBUG=False
SESSION_COOKIE_SECURE=False
PORT=5000
EOF
        print_success ".env file created"
    else
        print_warning ".env file already exists"
    fi
}

# Function to create data directory
create_data_directory() {
    if [ ! -d data ]; then
        print_status "Creating data directory..."
        mkdir -p data
        print_success "Data directory created"
    fi
}

# Function to install dependencies
install_dependencies() {
    print_status "Installing Python dependencies..."
    pip install -r requirements.txt
    print_success "Dependencies installed"
}

# Function to run tests
run_tests() {
    print_status "Running tests..."
    python -c "
from chatbot import EngagementChatbot
chatbot = EngagementChatbot()
print('✅ Chatbot initialization test passed')
"
    print_success "Tests completed"
}

# Function to build Docker image
build_docker() {
    if command_exists docker; then
        print_status "Building Docker image..."
        docker build -t engagement-chatbot .
        print_success "Docker image built successfully"
    else
        print_error "Docker not found. Please install Docker first."
        exit 1
    fi
}

# Function to run with Docker Compose
run_docker_compose() {
    if command_exists docker-compose; then
        print_status "Starting with Docker Compose..."
        docker-compose up -d
        print_success "Application started with Docker Compose"
        print_status "Access the application at: http://localhost:5000"
    else
        print_error "Docker Compose not found. Please install Docker Compose first."
        exit 1
    fi
}

# Function to deploy to Heroku
deploy_heroku() {
    if command_exists heroku; then
        print_status "Deploying to Heroku..."
        
        # Check if git repository exists
        if [ ! -d .git ]; then
            print_status "Initializing git repository..."
            git init
            git add .
            git commit -m "Initial commit"
        fi
        
        # Create Heroku app if it doesn't exist
        if ! heroku apps:info >/dev/null 2>&1; then
            print_status "Creating Heroku app..."
            heroku create
        fi
        
        # Set environment variables
        print_status "Setting environment variables..."
        heroku config:set SECRET_KEY=$(openssl rand -hex 32)
        heroku config:set DEBUG=False
        heroku config:set SESSION_COOKIE_SECURE=True
        
        # Deploy
        print_status "Deploying application..."
        git push heroku main
        
        print_success "Deployed to Heroku successfully!"
        print_status "Your app URL: $(heroku info -s | grep web_url | cut -d= -f2)"
    else
        print_error "Heroku CLI not found. Please install Heroku CLI first."
        exit 1
    fi
}

# Function to deploy to Railway
deploy_railway() {
    if command_exists railway; then
        print_status "Deploying to Railway..."
        
        # Check if git repository exists
        if [ ! -d .git ]; then
            print_status "Initializing git repository..."
            git init
            git add .
            git commit -m "Initial commit"
        fi
        
        # Deploy to Railway
        railway up
        
        print_success "Deployed to Railway successfully!"
    else
        print_error "Railway CLI not found. Please install Railway CLI first."
        exit 1
    fi
}

# Function to run locally
run_local() {
    print_status "Starting local development server..."
    create_env_file
    create_data_directory
    install_dependencies
    run_tests
    
    print_status "Starting Flask application..."
    python app.py
}

# Function to show help
show_help() {
    echo "Engagement Chatbot Deployment Script"
    echo ""
    echo "Usage: $0 [OPTION]"
    echo ""
    echo "Options:"
    echo "  local           Run locally with Flask development server"
    echo "  docker          Build and run with Docker"
    echo "  docker-compose  Run with Docker Compose"
    echo "  heroku          Deploy to Heroku"
    echo "  railway         Deploy to Railway"
    echo "  setup           Setup environment (create .env, install deps)"
    echo "  test            Run tests"
    echo "  help            Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 local"
    echo "  $0 docker-compose"
    echo "  $0 heroku"
}

# Main script logic
case "${1:-help}" in
    "local")
        run_local
        ;;
    "docker")
        build_docker
        print_status "Run with: docker run -p 5000:5000 engagement-chatbot"
        ;;
    "docker-compose")
        build_docker
        run_docker_compose
        ;;
    "heroku")
        deploy_heroku
        ;;
    "railway")
        deploy_railway
        ;;
    "setup")
        create_env_file
        create_data_directory
        install_dependencies
        run_tests
        print_success "Setup completed successfully!"
        ;;
    "test")
        run_tests
        ;;
    "help"|*)
        show_help
        ;;
esac
