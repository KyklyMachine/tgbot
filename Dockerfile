# Use a lightweight Python base image
FROM python:3.12-slim-bookworm

# Copy uv from the official image for fast package management
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set working directory
WORKDIR /app

# Set environment variables
# UV_COMPILE_BYTECODE=1: Compile Python source files to bytecode for faster startup
# PYTHONUNBUFFERED=1: Force stdout/stderr to be unbuffered (logs show up immediately)
ENV UV_COMPILE_BYTECODE=1 \
    PYTHONUNBUFFERED=1

# Copy dependency files first to leverage Docker cache
COPY pyproject.toml uv.lock ./

# Install dependencies
# --frozen: Sync with the exact versions in uv.lock
# --no-install-project: Don't install the project itself (useful if it's not a package)
# --no-cache: Keep image size small
RUN uv sync --frozen --no-install-project --no-cache

# Copy the rest of the application code
COPY . .

# Run the application
CMD ["uv", "run", "main.py"]
