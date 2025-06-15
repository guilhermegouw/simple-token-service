# Simple Token Service

A Django REST API service for company registration and token-based authentication. This service provides secure token generation and validation for companies.

## Features

- **Company Registration**: Secure company registration with auto-generated passwords
- **Token Generation**: UUID-based token creation with company authentication
- **Token Validation**: Secure token verification system
- **REST API**: Clean JSON API endpoints
- **Security**: Password hashing with SHA-256, non-root container execution
- **Docker Ready**: Containerized for easy deployment

## Requirements

- Python 3.12+
- Poetry (for dependency management)
- Django 5.2+
- Django REST Framework 3.16+

## Local Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd simple-token-service
```

### 2. Install Poetry (if not already installed)

```bash
# On Linux/macOS
curl -sSL https://install.python-poetry.org | python3 -

# On Windows (PowerShell)
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
```

### 3. Install Dependencies

```bash
# Install all dependencies (including dev dependencies)
poetry install

# Or install only production dependencies
poetry install --only=main
```

### 4. Activate Virtual Environment

```bash
poetry shell
```

### 5. Run Database Migrations

```bash
python manage.py migrate
```

### 6. Start the Development Server

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000`

## Docker Installation

### Build and Run with Docker

```bash
# Build the Docker image
docker build -t token-service .

# Run the container
docker run -p 8000:8000 token-service
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Base URL
```
http://localhost:8000/api
```

### 1. Company Registration

Register a new company and receive an auto-generated password.

**Endpoint:** `POST /companies/register/`

**Request:**
```bash
curl -X POST http://localhost:8000/api/companies/register/ \
  -H "Content-Type: application/json" \
  -d '{"company_name": "my-company"}'
```

**Success Response (201):**
```json
{
  "company_name": "my-company",
  "password": "0NLQCCRmpq_qP2v_sfWfWA",
  "created_at": "2025-06-15T21:03:09.972062Z",
  "message": "Company registered successfully. Please save your password - it will not be shown again."
}
```

**Error Response (400) - Company already exists:**
```json
{
  "company_name": ["Company name already exists"]
}
```

### 2. Token Generation

Generate a new authentication token using company credentials.

**Endpoint:** `POST /tokens/`

**Request:**
```bash
curl -X POST http://localhost:8000/api/tokens/ \
  -H "Content-Type: application/json" \
  -d '{
    "company_name": "my-company",
    "password": "0NLQCCRmpq_qP2v_sfWfWA"
  }'
```

**Success Response (201):**
```json
{
  "token": "e881044c-96d1-458a-918c-66f0d5bd8272",
  "company_name": "my-company",
  "created_at": "2025-06-15T21:04:04.765766Z",
  "message": "Token generated successfully. Please save your token - it will not be shown again."
}
```

**Error Response (400) - Invalid credentials:**
```json
{
  "non_field_errors": ["Invalid credentials"]
}
```

### 3. Token Validation

Validate if a token is active and valid.

**Endpoint:** `POST /tokens/validate/`

**Request:**
```bash
curl -X POST http://localhost:8000/api/tokens/validate/ \
  -H "Content-Type: application/json" \
  -d '{"token": "e881044c-96d1-458a-918c-66f0d5bd8272"}'
```

**Success Response (200) - Valid token:**
```json
{
  "valid": true,
  "message": "Token is valid"
}
```

**Error Response (400) - Invalid token:**
```json
{
  "valid": false,
  "message": "Token is invalid or inactive"
}
```

## Complete Workflow Example

Here's a complete example of the authentication flow:

```bash
# 1. Register a company
RESPONSE=$(curl -s -X POST http://localhost:8000/api/companies/register/ \
  -H "Content-Type: application/json" \
  -d '{"company_name": "test-company"}')

echo "Registration: $RESPONSE"

# Extract password from response (requires jq)
PASSWORD=$(echo $RESPONSE | jq -r '.password')

# 2. Generate a token
TOKEN_RESPONSE=$(curl -s -X POST http://localhost:8000/api/tokens/ \
  -H "Content-Type: application/json" \
  -d "{\"company_name\": \"test-company\", \"password\": \"$PASSWORD\"}")

echo "Token Generation: $TOKEN_RESPONSE"

# Extract token from response
TOKEN=$(echo $TOKEN_RESPONSE | jq -r '.token')

# 3. Validate the token
VALIDATION=$(curl -s -X POST http://localhost:8000/api/tokens/validate/ \
  -H "Content-Type: application/json" \
  -d "{\"token\": \"$TOKEN\"}")

echo "Token Validation: $VALIDATION"
```

## Development

### Running Tests

```bash
# Run all tests
poetry run pytest

# Run tests with coverage
poetry run pytest --cov=.

# Run specific app tests
poetry run pytest companies/tests/
poetry run pytest tokens/tests/
```

### Code Formatting

```bash
# Format code with black
poetry run black .

# Sort imports with isort
poetry run isort .

# Check code style with flake8
poetry run flake8 .
```

### Project Structure

```
simple-token-service/
├── companies/          # Company registration app
│   ├── models.py      # Company model
│   ├── serializers.py # Company serializers
│   ├── views.py       # Company registration view
│   └── tests/         # Company tests
├── tokens/            # Token management app
│   ├── models.py      # Token model
│   ├── serializers.py # Token serializers
│   ├── views.py       # Token generation/validation views
│   └── tests/         # Token tests
├── core/              # Django project settings
│   ├── settings.py    # Main settings
│   └── urls.py        # URL configuration
├── manage.py          # Django management script
├── pyproject.toml     # Poetry configuration
├── Dockerfile         # Docker configuration
└── README.md          # This file
```

## Security Considerations

- **Password Hashing**: All passwords are hashed using SHA-256
- **Token Security**: Tokens are stored as hashes in the database
- **No Root Access**: Docker container runs as non-root user
- **Input Validation**: All endpoints validate input data
- **Unique Constraints**: Company names and token hashes are unique

## License

This project is licensed under the terms specified in the LICENSE file.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Support

For questions or issues, please open an issue in the repository.
