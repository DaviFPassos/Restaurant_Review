package main

import (
	"bytes"
	"context"
	"encoding/json"
	"io"
	"log"
	"net/http"
	"os"
	"strings"
	"time"

	"github.com/gin-gonic/gin"

	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

var mongoCollection *mongo.Collection

// getMLServiceURL retrieves the ML service endpoint from environment variables
// Defaults to localhost:8000 for development, but allows override via ML_SERVICE_URL env var
func getMLServiceURL() string {
    if url := os.Getenv("ML_SERVICE_URL"); url != "" {
        return url
    }
    return "http://localhost:8000/v1/predict"
}

func getMongoURI() string {
	if uri:= os.Getenv("MONGO_URI"); uri != "" {
		return uri
	}
	return "mongo;//localhost:27017"
}

// ReviewRequest represents the JSON payload sent by clients to this API
// The binding:"required" tag ensures the field is validated and non-empty
type ReviewRequest struct {
	ReviewText string `json:"review_text" binding:"required"`
}

// MLResponse represents the JSON structure returned by the Python ML service
// Includes: prediction class code, human-readable sentiment, and confidence score
type MLResponse struct {
	PredictionCode int     `json:"prediction_code"`
	Sentiment      string  `json:"sentiment"`
	Confidence     float64 `json:"confidence"`
}

// initMongoDB to initialize database connection

func initMongoDB() {
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	clientOptions := options.Client().ApplyURI(getMongoURI())
	client, err := mongo.Connect(ctx, clientOptions)
	if err != nil {
		log.Fatalf("Failed to connnect to MOngoDB: %v", err)
	}

	// Look if connection is actually activated (PING)
	err = client.Ping(ctx, nil)
	if err != nil {
		log.Fatalf("MongoDB ping faield: %v", err)
	}

	// Defines database 'restaurant_db' and collection 'reviews'
	mongoCollection = client.Database("restaurant_db").Collection("reviews")
	log.Println("Successfully connected to MongoDB!")
}

func main() {
	// Initialize databank before upload API
	initMongoDB()

	// Set Gin framework to release mode for maximum performance and minimal logging
	gin.SetMode(gin.ReleaseMode)
	r := gin.Default()

	r.Use(func(c *gin.Context) {
		c.Writer.Header().Set("Access-Control-Allow-Origin", "*")
		c.Writer.Header().Set("Access-Control-Allow-Credentials", "true")
		c.Writer.Header().Set("Access-Control-Allow-Headers", "Content-Type, Content-Length, Accept-Encoding, X-CSRF-Token, Authorization, accept, origin, Cache-Control, X-Requested-With")
		c.Writer.Header().Set("Access-Control-Allow-Methods", "POST, OPTIONS, GET, PUT")

		if c.Request.Method == "OPTIONS" {
			c.AbortWithStatus(204)
			return
		}
		c.Next()
	})

	// Configure optimized HTTP client with 5-second timeout
	// This is a DevOps best practice to prevent hanging connections
	httpClient := &http.Client{
		Timeout: 5 * time.Second,
	}

	r.POST("/api/review", func(c *gin.Context) {
		var req ReviewRequest

		// Step 1: Validate incoming JSON structure and required fields
		if err := c.ShouldBindJSON(&req); err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": "The 'review_text' field is required and must be valid JSON."})
			return
		}

		// Step 2: Edge protection - prevent empty or whitespace-only requests from reaching the ML model
		textClean := strings.TrimSpace(req.ReviewText)
		if textClean == "" {
			c.JSON(http.StatusBadRequest, gin.H{"error": "Review text cannot contain only whitespace."})
			return
		}

		// Step 3: Serialize request data to JSON for transmission to Python service
		jsonData, err := json.Marshal(req)
		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": "Internal error while preparing request data."})
			return
		}

		// Step 4: Forward request to ML microservice via HTTP POST
		resp, err := httpClient.Post(getMLServiceURL(), "application/json", bytes.NewBuffer(jsonData))
		if err != nil {
			c.JSON(http.StatusServiceUnavailable, gin.H{"error": "Machine Learning service is currently unavailable."})
			return
		}
		defer resp.Body.Close()

		// Step 5: Handle HTTP error responses from FastAPI
		if resp.StatusCode != http.StatusOK {
			c.JSON(resp.StatusCode, gin.H{"error": "Error from ML service."})
			return
		}

		// Step 6: Read the ML inference response from Python service
		body, err := io.ReadAll(resp.Body)
		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": "Error reading model response."})
			return
		}

		var mlResponse MLResponse
		if err := json.Unmarshal(body, &mlResponse); err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": "Error parsing AI prediction."})
			return
		}
		
		// Asynchronous Record on MOngoDB
		go func (text string, res MLResponse)  {
			dbCtx, dbCancel := context.WithTimeout(context.Background(), 2*time.Second)
			defer dbCancel()

			document := bson.M{
				"review_text": text,
				"prediction_code": res.PredictionCode,
				"sentiment": res.Sentiment,
				"confidence": res.Confidence,
				"created_at": time.Now(),
			}
			
			_, insertErr := mongoCollection.InsertOne(dbCtx, document)
			if insertErr != nil {
				log.Printf("[MLOps Error] Failed to log review to MongoDB: %v", insertErr)
			}
		}(textClean, mlResponse)

		// Step 7: Return successful response with prediction data
		c.JSON(http.StatusOK, gin.H{
			"status": "success",
			"data":   mlResponse,
		})
	})

	// Start the Gateway API server on port 8080
	r.Run(":8080")
}