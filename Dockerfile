FROM python:3.11-slim

# Install system deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m appuser
WORKDIR /home/appuser/app
USER appuser

# Copy project files
COPY --chown=appuser:appuser . /home/appuser/app

# Install Python deps
RUN python -m pip install --upgrade pip
RUN if [ -f requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; fi

# Expose Streamlit port
EXPOSE 8501

# Use Streamlit in production mode and bind to all interfaces
ENV STREAMLIT_SERVER_HEADLESS=true

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
