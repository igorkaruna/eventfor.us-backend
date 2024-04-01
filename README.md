
![eventfor.us-backend](https://github.com/igorkaruna/eventfor.us-backend/assets/88438873/3af683ca-c695-4f13-a57e-242cd9ee88f1)

## Overview

eventfor.us offers a robust backend solution for managing events seamlessly. Designed with flexibility in mind, it supports a wide range of event management tasks from creation to execution. Built using DRF, it ensures high performance, reliability, and scalability for event organizers and participants alike.

## Features

- **Event Management**: Easily create, update, and delete events.
- **Advanced Filtering**: Utilize django-filter for refined search capabilities.
- **Debugging Tools**: Integrated with Django Debug Toolbar for efficient debugging.
- **Caching Mechanism**: django-redis setup for enhanced performance.
- **Logging Requests**: django-request-logging for thorough request monitoring.
- **JWT Authentication**: Secure your application with JWT-based authentication.

## CI/CD Pipeline

The project utilizes GitHub Actions for automating Continuous Integration (CI) and Continuous Deployment (CD) workflows, ensuring that each pull request and merge into the master branch is seamlessly tested and deployed.

### Continuous Integration (CI)

The CI workflow triggers on every pull request to the master branch, encompassing the following steps:

- **Setup**: Environment initialization and dependency installations using Poetry.
- **Linting**: Code quality checks with flake8 to ensure adherence to Python coding standards.
- **Testing**: Database migrations application and test execution using pytest to identify any issues early.

This approach aids in maintaining code quality and reliability throughout the project's lifecycle.

### Continuous Deployment (CD)

Following a successful merge into the master branch, the CD workflow automatically deploys the latest version of the application. The steps include:

- **Building Docker Image**: Production-ready Docker image construction.
- **Authenticating with Google Cloud**: Secure Google Cloud Platform login for project resource access.
- **Pushing Docker Image**: Docker image upload to the Google Cloud Container Registry.
- **Deploying to Virtual Machine**: Utilization of Docker Compose on the virtual machine for the deployment of the updated application.

These automated workflows facilitate efficient deployments, ensuring that the project remains up-to-date with the latest changes and improvements.

## Getting Started

### Prerequisites

- Docker & Docker Compose
- Python 3.11

### Installation

1. Clone the repository:
   ```sh
   git clone git@github.com:igorkaruna/eventfor.us-backend.git
   cd eventfor.us-backend

2. Set up your environment variables:
   ```sh
   cp .env.example .env

3. Start the development server using Docker Compose:
   ```sh
   docker-compose -f docker-compose.dev.yaml up --build

4. Verify the installation by accessing the application at http://127.0.0.1:8000.
