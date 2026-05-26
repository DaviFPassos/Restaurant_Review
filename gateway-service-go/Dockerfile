# Stage 1: Build (Compilation)
# Compiles Go source code into a static binary
FROM golang:1.23-alpine AS builder

# Set working directory inside container
WORKDIR /app

# Copy go.mod and go.sum first to leverage Docker's build cache
# This caches dependencies separately from source code changes
COPY go.mod go.sum ./
RUN go mod download

# Copy the remaining source code
COPY . .

# Compile into static binary optimized for production
# CGO_ENABLED=0 disables external C dependencies, making the binary self-contained
# GOOS=linux targets Linux OS
# -ldflags="-w -s" strips debug symbols to reduce binary size
RUN CGO_ENABLED=0 GOOS=linux go build -ldflags="-w -s" -o gateway .

# Stage 2: Runtime (Final Minimalist Image)
# Uses Alpine Linux (very small base image) for production deployment
FROM alpine:3.20

WORKDIR /app

# Copy only the compiled binary from builder stage
# This keeps the final image small by excluding build tools
COPY --from=builder /app/gateway .

# Expose the port configured in the Gin framework
EXPOSE 8080

# Start the Gateway API server
CMD ["./gateway"]