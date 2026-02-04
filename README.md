# ai-training-data-manager
PostgreSQL data management system for AI datasets
# 🚀 AI Training Data Manager API

A production-ready REST API for managing AI training datasets, built with FastAPI and PostgreSQL.

## 📋 Features

- ✅ Complete CRUD operations for datasets
- ✅ Search functionality with case-insensitive matching
- ✅ Data validation with Pydantic
- ✅ Auto-generated interactive documentation
- ✅ PostgreSQL database integration
- ✅ Secure credential management
- ✅ Error handling and validation

## 🛠️ Tech Stack

- **Backend:** FastAPI 0.109+
- **Database:** PostgreSQL (Supabase)
- **Validation:** Pydantic
- **Python:** 3.12+

## 📚 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Welcome message |
| GET | `/datasets` | Get all datasets |
| GET | `/datasets/{id}` | Get dataset by ID |
| POST | `/datasets` | Create new dataset |
| GET | `/stats` | Database statistics |
| GET | `/search?q=keyword` | Search datasets |

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- PostgreSQL database (Supabase account)

### Installation

1. **Clone the repository**
```bash
   git clone https://github.com/YOUR_USERNAME/ai-training-data-manager.git
   cd ai-training-data-manager
```

2. **Create virtual environment**
```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # source venv/bin/activate  # Mac/Linux
```

3. **Install dependencies**
```bash
   pip install -r requirements.txt
```

4. **Configure environment variables**
   
   Create a `.env` file in the root directory:
```env
   DB_HOST=your_supabase_host
   DB_PORT=5432
   DB_NAME=postgres
   DB_USER=your_username
   DB_PASSWORD=your_password
```

5. **Run the API**
```bash
   uvicorn api.main:app --reload
```

6. **Open interactive documentation**
   
   Visit: http://localhost:8000/docs

## 📖 API Documentation

### Get All Datasets
```http
GET /datasets
```

**Response:**
```json
{
  "success": true,
  "count": 21,
  "data": [...]
}
```

### Get Dataset by ID
```http
GET /datasets/{id}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "source": "ImageNet",
    "category": "AI/ML",
    "quality_score": 9
  }
}
```

### Create Dataset
```http
POST /datasets
Content-Type: application/json

{
  "content": "Dataset description",
  "source": "Dataset name",
  "category": "AI/ML",
  "quality_score": 8,
  "word_count": 5000
}
```

**Response:**
```json
{
  "success": true,
  "message": "Dataset created successfully",
  "id": 22
}
```

### Search Datasets
```http
GET /search?q=python
```

**Response:**
```json
{
  "success": true,
  "query": "python",
  "count": 5,
  "data": [...]
}
```

## 🗂️ Database Schema
```sql
CREATE TABLE datasets (
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    source VARCHAR(255),
    category VARCHAR(100),
    quality_score INTEGER CHECK (quality_score >= 1 AND quality_score <= 10),
    word_count INTEGER,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

## 🔒 Security

- Environment variables stored in `.env` (not committed to Git)
- SQL injection protection via parameterized queries
- Input validation with Pydantic models
- Type safety with Python type hints

## 📝 License

MIT License - feel free to use for your projects!

## 👨‍💻 Author

**Nikhil**
- Portfolio: [madecard.com](https://madecard.com)
- Skills: Flutter, Node.js, Next.js, FastAPI, PostgreSQL

## 🚀 Future Enhancements

- [ ] Authentication (JWT)
- [ ] Pagination for large datasets
- [ ] Advanced filtering
- [ ] LangChain integration for AI agents
- [ ] Deployment to production