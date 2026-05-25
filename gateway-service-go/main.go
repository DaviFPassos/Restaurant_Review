package main

import (
	"bytes"
	"encoding/json"
	"io"
	"net/http"
	"os"
	"strings"
	"time"

	"github.com/gin-gonic/gin"
)

// getMLServiceURL retrieves the ML service endpoint from environment variables
// Defaults to localhost:8000 for development, but allows override via ML_SERVICE_URL env var
func getMLServiceURL() string {
    if url := os.Getenv("ML_SERVICE_URL"); url != "" {
        return url
    }
    return "http://localhost:8000/v1/predict"
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

func main() {
	// Set Gin framework to release mode for maximum performance and minimal logging
	gin.SetMode(gin.ReleaseMode)

	r := gin.Default()

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

		// Step 7: Return successful response with prediction data
		c.JSON(http.StatusOK, gin.H{
			"status": "success",
			"data":   mlResponse,
		})
	})

	// Start the Gateway API server on port 8080
	r.Run(":8080")
}