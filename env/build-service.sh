#!/bin/bash
# MiniBI Service Build and Management Script
# This script is used for building, starting, stopping and managing MiniBI project services

# Set color output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Set path variables
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Check if Docker and Docker Compose are installed
check_requirements() {
    echo -e "${BLUE}Checking environment requirements...${NC}"
    if ! command -v docker &> /dev/null; then
        echo -e "${YELLOW}Warning: Docker is not installed or not found in PATH${NC}"
        echo -e "${YELLOW}This is a sample script, please ensure Docker is installed before actual use${NC}"
        # In development mode, don't exit
        # exit 1
    else
        echo -e "${GREEN}Docker is installed${NC}"
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        echo -e "${YELLOW}Warning: docker-compose command not found, will use docker compose instead${NC}"
        DOCKER_COMPOSE="docker compose"
    else
        DOCKER_COMPOSE="docker-compose"
        echo -e "${GREEN}Docker Compose is installed${NC}"
    fi
    
    echo -e "${GREEN}Environment check completed${NC}"
}

# Create external network
create_network() {
    echo -e "${BLUE}Setting up Docker network...${NC}"
    if docker network inspect minibi-network >/dev/null 2>&1; then
        echo -e "${YELLOW}Network minibi-network already exists${NC}"
    else
        docker network create minibi-network
        echo -e "${GREEN}Network minibi-network successfully created${NC}"
    fi
}

# Build services
build_services() {
    echo -e "${BLUE}Building MiniBI services...${NC}"
    cd "$SCRIPT_DIR" || exit
    $DOCKER_COMPOSE build
    echo -e "${GREEN}Service build completed${NC}"
}

# Start services
start_services() {
    echo -e "${BLUE}Starting MiniBI services...${NC}"
    cd "$SCRIPT_DIR" || exit
    $DOCKER_COMPOSE up -d
    echo -e "${GREEN}Services started in background${NC}"
    
    echo -e "${BLUE}Service status:${NC}"
    $DOCKER_COMPOSE ps
}

# Stop services
stop_services() {
    echo -e "${BLUE}Stopping MiniBI services...${NC}"
    cd "$SCRIPT_DIR" || exit
    $DOCKER_COMPOSE down
    echo -e "${GREEN}Services stopped${NC}"
}

# Restart services
restart_services() {
    stop_services
    start_services
}

# Show service logs
show_logs() {
    echo -e "${BLUE}Displaying service logs...${NC}"
    cd "$SCRIPT_DIR" || exit
    
    if [ -z "$1" ]; then
        $DOCKER_COMPOSE logs -f
    else
        $DOCKER_COMPOSE logs -f "$1"
    fi
}

# Clean up all services and data
cleanup() {
    echo -e "${RED}Warning: This operation will remove all containers, volumes, and networks${NC}"
    read -p "Continue? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        cd "$SCRIPT_DIR" || exit
        $DOCKER_COMPOSE down -v
        
        if docker network inspect minibi-network >/dev/null 2>&1; then
            docker network rm minibi-network
            echo -e "${GREEN}Network minibi-network deleted${NC}"
        fi
        
        echo -e "${GREEN}Cleanup completed${NC}"
    fi
}

# Show help information
show_help() {
    echo -e "${BLUE}MiniBI Service Management Script${NC}"
    echo "Usage: $0 [option]"
    echo
    echo "Options:"
    echo "  build       Build services"
    echo "  start       Start services"
    echo "  stop        Stop services"
    echo "  restart     Restart services"
    echo "  logs [service]  Display logs for all or specified service"
    echo "  status      Show service status"
    echo "  cleanup     Remove all containers, volumes, and networks"
    echo "  help        Display this help information"
}

# Show service status
show_status() {
    echo -e "${BLUE}MiniBI service status:${NC}"
    cd "$SCRIPT_DIR" || exit
    $DOCKER_COMPOSE ps
    
    echo -e "\n${BLUE}Container resource usage:${NC}"
    docker stats --no-stream $(docker-compose ps -q)
}

# Main function
main() {
    check_requirements
    
    # Show help when no parameters provided
    if [ $# -eq 0 ]; then
        show_help
        exit 0
    fi
    
    case "$1" in
        build)
            create_network
            build_services
            ;;
        start)
            create_network
            start_services
            ;;
        stop)
            stop_services
            ;;
        restart)
            restart_services
            ;;
        logs)
            show_logs "$2"
            ;;
        status)
            show_status
            ;;
        cleanup)
            cleanup
            ;;
        help)
            show_help
            ;;
        *)
            echo -e "${RED}Error: Unknown option $1${NC}"
            show_help
            exit 1
            ;;
    esac
}

# Execute main function
main "$@"