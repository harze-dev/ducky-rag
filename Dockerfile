# Use the prebuilt cs5740-base image
FROM container.cs.vt.edu/steve72/cs5740-base:latest

# Set working directory inside the container
WORKDIR /app

# Copy dependency manifests and readme first
COPY .python-version pyproject.toml uv.lock* README.md ./
RUN --mount=type=cache,target=/root/.cache/uv \
    if [ -f uv.lock ]; then uv sync --frozen --no-dev; else uv sync --no-dev; fi

# Copy project code last
COPY . .

# Expose Streamlit port
EXPOSE 8501

# Default command to start Streamlit using uv run to use the virtual environment
CMD ["uv", "run", "streamlit", "run", "🏠_Home.py", "--server.port=8501", "--server.address=0.0.0.0"]
