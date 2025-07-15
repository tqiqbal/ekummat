# Ekummat REST API Setup

This document provides instructions for setting up and using the Django REST Framework API for the Ekummat Islamic content management system.

## Overview

The API provides read-only access to all Islamic content data including:
- Books and PDFs
- Quran chapters
- Hadith books, chapters, and content
- Search functionality
- Statistics

## Setup Instructions

### 1. Install Dependencies

First, install the new dependencies:

```bash
pip install -r requirements.txt
```

### 2. Run Migrations

Make sure your database is up to date:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Start the Development Server

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/`

## API Endpoints

### Base URL: `http://localhost:8000/api/`

| Endpoint | Description |
|----------|-------------|
| `/books/` | Islamic books |
| `/book-pdfs/` | Book PDF files |
| `/quran-chapters/` | Quran chapters |
| `/hadith-books/` | Hadith books |
| `/hadith-main-chapters/` | Main chapters of Hadith books |
| `/hadith-sub-chapters/` | Sub chapters of Hadith books |
| `/hadith-content/` | Actual Hadith content |
| `/hadith-excel-files/` | Excel files for data import |
| `/search/` | Global search across all content |
| `/statistics/` | Content statistics |

## Testing the API

### Using the Test Script

Run the provided test script to verify all endpoints:

```bash
python test_api.py
```

### Manual Testing

You can test endpoints manually using curl or a web browser:

```bash
# Get all books
curl http://localhost:8000/api/books/

# Get statistics
curl http://localhost:8000/api/statistics/

# Search for content
curl "http://localhost:8000/api/search/?q=faith"
```

### Using a REST Client

You can also use tools like:
- Postman
- Insomnia
- Thunder Client (VS Code extension)

## Features

### Pagination
All list endpoints support pagination:
```
GET /api/books/?page=1&page_size=20
```

### Filtering
Most endpoints support filtering:
```
GET /api/hadith-content/?grade=Sahih
GET /api/books/?category=hadith
```

### Search
Endpoints with search capability:
```
GET /api/books/?search=Bukhari
GET /api/hadith-content/?search=faith
```

### Ordering
Most endpoints support ordering:
```
GET /api/hadith-content/?ordering=-sr_no
GET /api/books/?ordering=title
```

## React Native Integration

### Example Usage

```javascript
// Fetch books
const fetchBooks = async () => {
  const response = await fetch('http://localhost:8000/api/books/');
  const data = await response.json();
  return data.results;
};

// Search hadith
const searchHadith = async (query) => {
  const response = await fetch(`http://localhost:8000/api/hadith-content/?search=${encodeURIComponent(query)}`);
  const data = await response.json();
  return data.results;
};

// Get statistics
const getStats = async () => {
  const response = await fetch('http://localhost:8000/api/statistics/');
  return await response.json();
};
```

## Configuration

### CORS Settings

The API is configured to allow all origins for development. For production, update the CORS settings in `core/settings.py`:

```python
CORS_ALLOWED_ORIGINS = [
    "https://yourdomain.com",
    "http://localhost:3000",
]
```

### Pagination Settings

Default pagination settings in `core/settings.py`:

```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}
```

## Security Considerations

1. **Read-Only Access**: All endpoints are read-only (GET requests only)
2. **No Authentication**: Currently no authentication required (public API)
3. **CORS**: Configured for cross-origin requests
4. **Rate Limiting**: Not implemented (consider adding for production)

## Production Deployment

For production deployment:

1. Update CORS settings to restrict origins
2. Consider adding rate limiting
3. Use HTTPS
4. Configure proper database settings
5. Set DEBUG=False in settings

## Troubleshooting

### Common Issues

1. **Import Errors**: Make sure all dependencies are installed
2. **Database Errors**: Run migrations if you get database-related errors
3. **CORS Errors**: Check CORS settings if accessing from a different domain
4. **404 Errors**: Ensure the API app is included in INSTALLED_APPS

### Debug Mode

For debugging, check Django's debug output and logs. The API will return detailed error messages when DEBUG=True.

## Support

For issues or questions:
1. Check the Django REST Framework documentation
2. Review the API documentation in `API_DOCUMENTATION.md`
3. Test endpoints using the provided test script 