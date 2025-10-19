# CrUX Analyzer - Django Backend API

A lightweight Django REST API for analyzing website performance using Google's Chrome User Experience Report (CrUX) data. This API provides real-time Core Web Vitals metrics for multiple URLs with built-in validation, error handling, and CORS support.

## Features

- **Real-time CrUX Data**: Fetch live performance metrics from Google's CrUX API
- **Core Web Vitals**: LCP, CLS, FCP metrics with percentile data
- **Smart URL Handling**: Automatically adds protocol (https://) if missing
- **Error Handling**: Comprehensive error reporting for failed requests
- **CORS Ready**: Pre-configured for frontend integration
- **Lightweight**: No database required, minimal dependencies

## Core Web Vitals Metrics

| Metric | Description | Good | Needs Improvement | Poor |
|--------|-------------|------|-------------------|------|
| **LCP** | Largest Contentful Paint | ≤ 2.5s | 2.5s - 4.0s | > 4.0s |
| **CLS** | Cumulative Layout Shift | ≤ 0.1 | 0.1 - 0.25 | > 0.25 |
| **FCP** | First Contentful Paint | ≤ 1.8s | 1.8s - 3.0s | > 3.0s |

## Project Structure

```
crux_analyzer
├── analysis/                    # Main Django app
│   ├── crux_service.py         # CrUX API integration
│   ├── serializers.py          # Request/response validation
│   ├── views.py                # API endpoints
│   ├── urls.py                 # URL routing
│   └── apps.py                 # App configuration
├── crux_analyzer/              # Django project settings
│   ├── settings.py             # Configuration
│   ├── urls.py                 # Main URL routing
│   └── wsgi.py                 # WSGI deployment
├── requirements.txt            # Python dependencies
├── manage.py                   # Django management
├── .env                        # Environment variables (create this)
├── .gitignore                  # Git ignore rules
└── README.md                   # This file
```

## Installation & Setup

### Prerequisites

- Python 3.8+
- Google CrUX API Key ([Get one here](https://developers.google.com/web/tools/chrome-user-experience-report/api/reference))

### 1. Clone the Repository

```bash
git clone <repository-url>
cd crux_analyzer
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

Create a `.env` file in the project root:

```bash
# .env
SECRET_KEY=your-secret-key-here
DEBUG=True
CRUX_API_KEY=your-crux-api-key-here
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

**Important**: Replace `your-crux-api-key-here` with your actual Google CrUX API key.

### 5. Run Database Migrations

```bash
python manage.py migrate
```

### 6. Start the Development Server

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000`

## 📡 API Endpoints

### 1. Analyze URLs

Analyze multiple URLs for Core Web Vitals performance data.

**Endpoint**: `POST /api/analyze-url`

**Request Body**:
```json
{
  "urls": [
    "www.google.com",
    "https://github.com",
    "example.com"
  ]
}
```

**Response**:
```json
{
  "results": [
    {
      "url": "https://www.google.com",
      "fetchTime": "2025-10-18T12:00:00.000000",
      "metrics": {
        "lcp": {
          "p75": 1200,
          "p90": 1800,
          "p99": 3000,
          "status": "available",
          "distribution": [...]
        },
        "cls": {
          "p75": 0.05,
          "p90": 0.12,
          "p99": 0.25,
          "status": "available",
          "distribution": [...]
        },
        "fcp": {
          "p75": 900,
          "p90": 1400,
          "p99": 2200,
          "status": "available",
          "distribution": [...]
        }
      },
      "collectionPeriod": {
        "firstDate": {"year": 2025, "month": 9, "day": 1},
        "lastDate": {"year": 2025, "month": 9, "day": 30}
      }
    }
  ],
  "summary": {
    "lcp": {"avg": 1200.0, "min": 1200, "max": 1200, "count": 1},
    "cls": {"avg": 0.05, "min": 0.05, "max": 0.05, "count": 1},
    "fcp": {"avg": 900.0, "min": 900, "max": 900, "count": 1}
  },
  "errors": [],
  "totalUrls": 1,
  "successCount": 1,
  "timestamp": "2025-10-18T12:00:00.000000"
}
```

### 2. Health Check

Check API status and configuration.

**Endpoint**: `GET /api/health/`

**Response**:
```json
{
  "status": "ok",
  "apiConfigured": true,
  "timestamp": "2025-10-18T12:00:00.000000",
  "version": "1.0.0"
}
```

## 🔧 Usage Examples

### cURL Examples

```bash
# Health check
curl -X GET http://localhost:8000/api/health/

# Analyze URLs
curl -X POST http://localhost:8000/api/analyze-url \
  -H "Content-Type: application/json" \
  -d '{
    "urls": ["www.google.com", "github.com"]
  }'
```

### JavaScript/Fetch Example

```javascript
// Analyze URLs
const response = await fetch('http://localhost:8000/api/analyze-url', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    urls: ['www.google.com', 'github.com', 'stackoverflow.com']
  })
});

const data = await response.json();
console.log(data);
```

### Python Requests Example

```python
import requests

# Analyze URLs
response = requests.post('http://localhost:8000/api/analyze-url', json={
    'urls': ['www.google.com', 'github.com']
})

data = response.json()
print(data)
```

## Key Features Explained

### Smart URL Handling

The API automatically handles various URL formats:

- `google.com` → `https://google.com`
- `www.google.com` → `https://www.google.com`
- `https://google.com` → `https://google.com` (unchanged)
- `//google.com` → `https://google.com`

### Error Handling

The API provides detailed error information:

```json
{
  "results": [...],
  "errors": [
    {
      "url": "invalid-url",
      "error": "Failed to fetch CrUX data: HTTP 404"
    }
  ],
  "totalUrls": 2,
  "successCount": 1
}
```

### CORS Configuration

Pre-configured for frontend integration with customizable origins via environment variables.

## Deployment

### Production Settings

1. Set `DEBUG=False` in your `.env` file
2. Add your production domain to `ALLOWED_HOSTS` in `settings.py`
3. Use a production WSGI server like Gunicorn:

```bash
pip install gunicorn
gunicorn crux_analyzer.wsgi:application
```

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `SECRET_KEY` | Django secret key | Generated | Yes |
| `DEBUG` | Debug mode | `True` | No |
| `CRUX_API_KEY` | Google CrUX API key | None | Yes |
| `CORS_ALLOWED_ORIGINS` | Allowed CORS origins | `http://localhost:3000` | No |

## Testing

### Manual Testing

```bash
# Test health endpoint
curl http://localhost:8000/api/health/

# Test analysis endpoint
curl -X POST http://localhost:8000/api/analyze-url \
  -H "Content-Type: application/json" \
  -d '{"urls": ["google.com"]}'
```

### System Check

```bash
python manage.py check
```

## 🔍 Troubleshooting

### Common Issues

1. **"CrUX API key not configured"**
   - Ensure `CRUX_API_KEY` is set in your `.env` file
   - Verify the API key is valid

2. **CORS errors in browser**
   - Add your frontend URL to `CORS_ALLOWED_ORIGINS`
   - Ensure the frontend is making requests to the correct backend URL

3. **"No CrUX data available"**
   - The URL might not have sufficient traffic for CrUX data
   - Try testing with popular websites like `google.com`

### Logs

Check Django logs for detailed error information:

```bash
python manage.py runserver --verbosity=2
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
