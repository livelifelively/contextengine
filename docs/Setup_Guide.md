# Context Engine Setup Guide

This guide provides all the essential commands to get your Context Engine with Dgraph up and running quickly.

## 🎉 **Today's Accomplishments**

✅ **Dgraph Setup**: Complete Docker-based Dgraph cluster with Zero and Alpha  
✅ **Ratel GUI**: Web-based interface for database management  
✅ **GraphQL API**: Standard GraphQL endpoints for data access  
✅ **CRUD Operations**: Full Create, Read, Update, Delete functionality  
✅ **Service Layer**: Python DgraphService with both DQL and GraphQL support  
✅ **Testing Suite**: Comprehensive unit and integration tests  
✅ **Documentation**: Complete setup and GraphQL guides  

## 🚀 **Quick Start Commands**

### 1. Start Everything
```bash
# Start all services (Dgraph Zero, Alpha, Ratel, App)
docker-compose up -d

# Check status
docker-compose ps
```

### 2. Verify Services Are Running
```bash
# Check Dgraph health
curl -s http://localhost:8080/health

# Check if GraphQL is working
curl -s http://localhost:8080/graphql -H "Content-Type: application/json" \
  -d '{"query": "{ __schema { types { name } } }"}'
```

### 3. Access Interfaces
- **Ratel GUI**: http://localhost:8000
- **GraphQL API**: http://localhost:8080/graphql
- **Dgraph Admin**: http://localhost:8080/admin

## 🛠️ **Development Commands**

### Start Development Environment
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f alpha
docker-compose logs -f app
docker-compose logs -f ratel
```

### Stop Development Environment
```bash
# Stop all services
docker-compose down

# Stop and remove volumes (WARNING: deletes all data)
docker-compose down -v
```

### Rebuild and Restart
```bash
# Rebuild app container
docker-compose up --build -d app

# Rebuild all containers
docker-compose up --build -d
```

## 🧪 **Testing Commands**

### Run Unit Tests
```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_dgraph_service.py -v

# Run only unit tests (no integration)
python -m pytest tests/test_dgraph_service.py::TestDgraphServiceUnit -v
```

### Run Integration Tests
```bash
# Run integration tests with Docker
docker run --rm --network context-engine_default \
  -v "$(pwd)":/workspace -w /workspace \
  -e DGRAPH_ALPHA_HOST=alpha -e DGRAPH_ALPHA_PORT=9080 \
  python:3.12-slim bash -c "pip install pydgraph pydantic pytest && python -m pytest tests/test_dgraph_service.py -m integration -v"
```

### Test CRUD Operations
```bash
# Test basic CRUD operations
docker run --rm --network context-engine_default \
  -v "$(pwd)":/workspace -w /workspace \
  -e DGRAPH_ALPHA_HOST=alpha -e DGRAPH_ALPHA_PORT=9080 \
  python:3.12-slim bash -c "pip install pydgraph pydantic && python -c '
import sys
sys.path.insert(0, \"src\")
from context_engine.services.dgraph_service import DgraphService
from context_engine.application.knowledge_graph_loader import load_knowledge_graph_nodes
from pathlib import Path

with DgraphService(dgraph_host=\"alpha\", dgraph_port=9080) as service:
    service.setup_schema()
    nodes = load_knowledge_graph_nodes(str(Path(\"src/context_engine/application/knowledge_graph_nodes.json\")))
    for node in nodes:
        uid = service.create_node(node)
        print(f\"Created: {node.id} -> {uid}\")
'"
```

## 🌐 **GraphQL Commands**

### Set Up GraphQL Schema
```bash
# Set up the GraphQL schema
curl -X POST localhost:8080/admin/schema \
  -H "Content-Type: text/plain" \
  -d 'type KnowledgeGraphNode {
  nodeId: String! @id @search(by: [exact])
  title: String! @search(by: [fulltext, exact])
  content: [String!]!
  metadata: String
  relationships: String
  semanticTags: [String!]! @search(by: [exact])
  compositionRules: String
  sectionType: String @search(by: [exact])
  importance: String @search(by: [exact])
}'
```

### Test GraphQL Operations
```bash
# Create a node via GraphQL
curl -X POST localhost:8080/graphql \
  -H "Content-Type: application/json" \
  -d '{
    "query": "mutation { addKnowledgeGraphNode(input: [{ nodeId: \"test.1\", title: \"Test Node\", content: [\"Test content\"], semanticTags: [\"test\"] }]) { knowledgeGraphNode { nodeId title } } }"
  }'

# Query all nodes
curl -X POST localhost:8080/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "{ queryKnowledgeGraphNode { nodeId title semanticTags } }"}'

# Query by semantic tag
curl -X POST localhost:8080/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "{ queryKnowledgeGraphNode(filter: { semanticTags: { eq: \"test\" } }) { nodeId title } }"}'
```

## 🔧 **Troubleshooting Commands**

### Check Container Status
```bash
# List all containers
docker ps -a

# Check container logs
docker-compose logs

# Check specific service
docker-compose logs alpha
```

### Reset Everything
```bash
# Stop and remove everything
docker-compose down -v

# Remove all images (WARNING: will rebuild everything)
docker system prune -a

# Start fresh
docker-compose up -d
```

### Fix Common Issues
```bash
# If containers won't start, check ports
lsof -i :8080
lsof -i :9080
lsof -i :8000
lsof -i :8008

# If Dgraph won't connect, restart alpha
docker-compose restart alpha

# If app won't start, rebuild it
docker-compose up --build -d app
```

## 📊 **Data Management**

### Backup Data
```bash
# Export Dgraph data
docker-compose exec alpha dgraph export --output /dgraph/backup

# Copy backup from container
docker cp context-engine-alpha-1:/dgraph/backup ./backup
```

### Restore Data
```bash
# Copy backup to container
docker cp ./backup context-engine-alpha-1:/dgraph/backup

# Import data
docker-compose exec alpha dgraph import --files /dgraph/backup
```

### Clear All Data
```bash
# Drop all data (WARNING: irreversible)
docker run --rm --network context-engine_default \
  -v "$(pwd)":/workspace -w /workspace \
  -e DGRAPH_ALPHA_HOST=alpha -e DGRAPH_ALPHA_PORT=9080 \
  python:3.12-slim bash -c "pip install pydgraph && python -c '
import sys
sys.path.insert(0, \"src\")
from context_engine.services.dgraph_service import DgraphService
with DgraphService(dgraph_host=\"alpha\", dgraph_port=9080) as service:
    service.drop_all()
    print(\"All data cleared\")
'"
```

## 🎯 **Daily Workflow**

### Morning Setup
```bash
# 1. Start services
docker-compose up -d

# 2. Wait for services to be ready
sleep 10

# 3. Verify everything is working
curl -s http://localhost:8080/health

# 4. Open Ratel GUI
open http://localhost:8000
```

### Evening Cleanup
```bash
# Stop all services
docker-compose down

# Optional: clean up Docker system
docker system prune -f
```

## 📚 **Useful URLs**

- **Ratel GUI**: http://localhost:8000
- **GraphQL Playground**: http://localhost:8080/graphql
- **Dgraph Admin**: http://localhost:8080/admin
- **Dgraph Health**: http://localhost:8080/health
- **App MCP Server**: http://localhost:8008

## 🔍 **Monitoring**

### Check Resource Usage
```bash
# Docker resource usage
docker stats

# Container logs
docker-compose logs -f --tail=100
```

### Performance Monitoring
```bash
# Check Dgraph metrics
curl -s http://localhost:8080/metrics

# Check container health
docker-compose ps
```

---

## 🚀 **Quick Reference**

| Command | Purpose |
|---------|---------|
| `docker-compose up -d` | Start all services |
| `docker-compose down` | Stop all services |
| `docker-compose logs -f` | View live logs |
| `docker-compose ps` | Check service status |
| `curl localhost:8080/health` | Check Dgraph health |
| `open http://localhost:8000` | Open Ratel GUI |

**Remember**: Always run `docker-compose down` before shutting down your computer to properly stop all containers! 🎉
