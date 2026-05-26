# Step 1: Use an official Node runtime as a base image
FROM node:20-alpine

# Step 2: Set the working directory inside the container
WORKDIR /app

# Step 3: Copy package.json and package-lock.json to install dependencies first
# This leverages Docker's cache layer for faster subsequent builds
COPY package*.json ./

# Step 4: Install local dependencies
RUN npm install

# Step 5: Copy the rest of the application source code
COPY . .

# Step 6: Expose the default Vite development port
EXPOSE 5173

# Step 7: Run the application in development mode with the --host flag
# The --host flag is critical to allow external connections from the Docker host machine
CMD ["npm", "run", "dev", "--", "--host"]