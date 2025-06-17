#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check if Python virtual environment exists
check_venv() {
    if [ ! -d "venv" ]; then
        echo -e "${RED}Virtual environment not found. Creating one...${NC}"
        python3 -m venv venv
        if [ $? -ne 0 ]; then
            echo -e "${RED}Failed to create virtual environment${NC}"
            exit 1
        fi
    fi
}

# Function to activate virtual environment
activate_venv() {
    if [ -f "venv/bin/activate" ]; then
        source venv/bin/activate
        # Verify Python is available after activation
        if ! command_exists python; then
            echo -e "${RED}Python not found in virtual environment${NC}"
            exit 1
        fi
        echo -e "${GREEN}Using Python from virtual environment: $(which python)${NC}"
    else
        echo -e "${RED}Virtual environment activation script not found${NC}"
        exit 1
    fi
}

# Function to install requirements
install_requirements() {
    if [ -f "requirements.txt" ]; then
        echo -e "${GREEN}Installing requirements...${NC}"
        python -m pip install --upgrade pip
        python -m pip install -r requirements.txt
        if [ $? -ne 0 ]; then
            echo -e "${RED}Failed to install requirements${NC}"
            exit 1
        fi
    else
        echo -e "${RED}requirements.txt not found${NC}"
        exit 1
    fi
}

# Function to start the persistent server
start_persistent_server() {
    echo -e "${GREEN}Starting persistent server...${NC}"
    python app/servers/persistent_server.py &
    PERSISTENT_SERVER_PID=$!
    if [ $? -ne 0 ]; then
        echo -e "${RED}Failed to start persistent server${NC}"
        exit 1
    fi
    echo -e "${GREEN}Persistent server started with PID: $PERSISTENT_SERVER_PID${NC}"
    # Give the server a moment to start
    sleep 2
}

# Function to start the main application
start_main_app() {
    echo -e "${GREEN}Starting main application...${NC}"
    python app/main.py
    MAIN_APP_STATUS=$?
    if [ $MAIN_APP_STATUS -ne 0 ]; then
        echo -e "${RED}Main application failed with status: $MAIN_APP_STATUS${NC}"
        kill $PERSISTENT_SERVER_PID 2>/dev/null
        exit 1
    fi
}

# Function to handle cleanup
cleanup() {
    echo -e "\n${GREEN}Cleaning up...${NC}"
    if [ ! -z "$PERSISTENT_SERVER_PID" ]; then
        kill $PERSISTENT_SERVER_PID 2>/dev/null
        echo -e "${GREEN}Stopped persistent server${NC}"
    fi
    exit 0
}

# Set up trap for cleanup
trap cleanup SIGINT SIGTERM

# Main execution
echo -e "${GREEN}Starting CerebroMCP...${NC}"

# Check Python installation
if ! command_exists python3; then
    echo -e "${RED}Python 3 is not installed${NC}"
    exit 1
fi

# Check and setup virtual environment
check_venv
activate_venv
install_requirements

# Start the application
start_persistent_server
start_main_app

# Cleanup will be handled by the trap 