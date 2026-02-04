from fastapi import FastAPI, HTTPException
from api.db_manager import DatabaseManager
from pydantic import BaseModel, Field

app = FastAPI(
    title="AI Training Data Manager API",
    description="REST API for managing AI training datasets",
    version="1.0.0"
)

db = DatabaseManager()

class DatasetCreate(BaseModel):
    """
    Model for creating a new dataset
    Defines what data is required and its types
    """
    content: str
    source: str
    category: str
    quality_score: int = Field(..., ge=1, le=10, description="Quality score between 1-10")
    word_count: int = Field(..., gt=0, description="Word count must be positive")

@app.on_event("startup")
def startup_event():
    if db.connect():
        print("✅ Database connected!")
    else:
        print("❌ Database connection failed!")


@app.get("/")
def read_root():
    return {
        "message": "Welcome to AI Training Data Manager API!",
        "status": "running",
        "version": "1.0.0"
    }


@app.get("/datasets")
def get_all_datasets():
    try:
        datasets = db.get_all_datasets()
        return {
            "success": True,
            "count": len(datasets) if datasets else 0,
            "data": datasets if datasets else []
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/stats")
def get_stats():
    try:
        stats = db.get_statistics()
        return {
            "success": True,
            "data": stats
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/datasets/{dataset_id}")  
def get_dataset_by_id(dataset_id: int):
    """
    Get a single dataset by ID
    
    Args:
        dataset_id (int): The ID of the dataset (must be a number)
        
    Returns:
        dict: Single dataset details or 404 error if not found
    """
    try:
        # Query to get one dataset by ID
        query = """
        SELECT id, source, category, quality_score, word_count
        FROM datasets
        WHERE id = %s;
        """
        result = db.execute_query(query, (dataset_id,))
        
        # Check if dataset exists
        if not result or len(result) == 0:
            # Return 404 Not Found
            raise HTTPException(
                status_code=404,
                detail=f"Dataset with ID {dataset_id} not found"
            )
        
        # Return the dataset (first item in results)
        return {
            "success": True,
            "data": result[0]
        }
    
    except HTTPException:
        # Re-raise HTTP exceptions (like 404)
        raise
    except Exception as e:
        # Handle other errors
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/datasets")
def create_dataset(dataset: DatasetCreate):
    """
    Create a new dataset
    
    Args:
        dataset (DatasetCreate): Dataset data from request body
        
    Returns:
        dict: Success message with new dataset ID
    """
    try:
        # SQL query to insert new dataset
        query = """
        INSERT INTO datasets (content, source, category, quality_score, word_count)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id;
        """
        
        # Execute the insert query with parameters as a tuple
        result = db.execute_query(
            query,
            (
                dataset.content,
                dataset.source,
                dataset.category,
                dataset.quality_score,
                dataset.word_count
            )
        )
        
        # Get the ID of the newly created dataset
        if not result or len(result) == 0:
            raise HTTPException(
                status_code=500,
                detail="Failed to create dataset - no ID returned"
            )
        
        new_id = result[0]['id']
        
        # Return success response
        return {
            "success": True,
            "message": "Dataset created successfully",
            "id": new_id,
            "data": {
                "content": dataset.content,
                "source": dataset.source,
                "category": dataset.category,
                "quality_score": dataset.quality_score,
                "word_count": dataset.word_count
            }
        }
    
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Catch all other errors
        raise HTTPException(
            status_code=500,
            detail=f"Error creating dataset: {str(e)}"
        )  
    
@app.get("/search")
def search_datasets(q: str):
    """
    Search datasets by keyword
    
    Args:
        q (str): Search keyword (searches in source, category, and content)
        
    Returns:
        dict: List of matching datasets
        
    Example:
        /search?q=python → Finds datasets with "python" in name/content
    """
    try:
        # SQL query with ILIKE for case-insensitive search
        # %{keyword}% means: anything + keyword + anything
        query = """
        SELECT id, content, source, category, quality_score, word_count
        FROM datasets
        WHERE source ILIKE %s
            OR category ILIKE %s
            OR content ILIKE %s
        ORDER BY quality_score DESC;
        """
        
        # Create search pattern: %keyword%
        search_pattern = f"%{q}%"
        
        # Execute query (same pattern for all 3 fields)
        results = db.execute_query(
            query,
            (search_pattern, search_pattern, search_pattern)
        )
        
        # Return results
        return {
            "success": True,
            "query": q,
            "count": len(results) if results else 0,
            "data": results if results else []
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Search error: {str(e)}"
        )


@app.on_event("shutdown")
def shutdown_event():
    db.disconnect()
    print("🔌 Database disconnected")