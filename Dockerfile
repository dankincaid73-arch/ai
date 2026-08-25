# Use a lightweight Python base image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy dependencies first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright Chromium and its OS dependencies
RUN playwright install --with-deps chromium

# Copy the rest of the project files into the container
COPY . .

# Keep the container running in the background so you can execute scripts inside it
CMD ["tail", "-f", "/dev/null"]