# Multi-stage Docker build for Safeway MCP Server
FROM python:3.11-slim as builder

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Final stage
FROM python:3.11-slim

WORKDIR /app

# Copy dependencies from builder
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Copy application code
COPY safeway_api.py .
COPY safeway_mcp_server.py .

# Create non-root user
RUN useradd -m -u 1000 safeway && chown -R safeway:safeway /app
USER safeway

# Expose port (not used for MCP stdio but useful for future HTTP mode)
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import safeway_mcp_server" || exit 1

# Run MCP server
CMD ["python", "safeway_mcp_server.py"]
