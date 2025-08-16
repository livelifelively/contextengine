# GraphQL Guide for Context Engine

This guide shows you how to use GraphQL with your Dgraph setup instead of DQL (Dgraph Query Language).

## 🌐 **GraphQL Endpoints**

Your Dgraph setup now exposes the following GraphQL endpoints:

- **GraphQL API**: `http://localhost:8080/graphql`
- **GraphQL Admin**: `http://localhost:8080/admin`
- **Ratel GUI**: `http://localhost:8000` (has a GraphQL tab)

## 📊 **Current Schema**

The following GraphQL schema is active:

```graphql
type KnowledgeGraphNode {
  nodeId: String! @id @search(by: [exact])
  title: String! @search(by: [fulltext, exact])
  content: [String!]!
  metadata: String
  relationships: String
  semanticTags: [String!]! @search(by: [exact])
  compositionRules: String
  sectionType: String @search(by: [exact])
  importance: String @search(by: [exact])
}
```

## 🔧 **Setting Up GraphQL Schema**

If you need to update the schema, use:

```bash
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

## 📝 **Creating Data (Mutations)**

### Add a Knowledge Graph Node

```bash
curl -X POST localhost:8080/graphql \
  -H "Content-Type: application/json" \
  -d '{
    "query": "mutation { addKnowledgeGraphNode(input: [{ nodeId: \"example.node.1\", title: \"Example Node\", content: [\"First line\", \"Second line\"], semanticTags: [\"example\", \"demo\"], sectionType: \"example\", importance: \"high\" }]) { knowledgeGraphNode { nodeId title semanticTags } } }"
  }'
```

### Update a Node

```bash
curl -X POST localhost:8080/graphql \
  -H "Content-Type: application/json" \
  -d '{
    "query": "mutation { updateKnowledgeGraphNode(input: { filter: { nodeId: { eq: \"example.node.1\" } }, set: { title: \"Updated Example Node\" } }) { knowledgeGraphNode { nodeId title } } }"
  }'
```

### Delete a Node

```bash
curl -X POST localhost:8080/graphql \
  -H "Content-Type: application/json" \
  -d '{
    "query": "mutation { deleteKnowledgeGraphNode(filter: { nodeId: { eq: \"example.node.1\" } }) { msg numUids } }"
  }'
```

## 📖 **Querying Data**

### Get All Nodes

```bash
curl -X POST localhost:8080/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "{ queryKnowledgeGraphNode { nodeId title content semanticTags sectionType importance } }"}'
```

### Query by Semantic Tag

```bash
curl -X POST localhost:8080/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "{ queryKnowledgeGraphNode(filter: { semanticTags: { eq: \"introduction\" } }) { nodeId title semanticTags } }"}'
```

### Search by Title (Full-text)

```bash
curl -X POST localhost:8080/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "{ queryKnowledgeGraphNode(filter: { title: { anyoftext: \"Context\" } }) { nodeId title } }"}'
```

### Query by Section Type

```bash
curl -X POST localhost:8080/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "{ queryKnowledgeGraphNode(filter: { sectionType: { eq: \"introduction\" } }) { nodeId title sectionType } }"}'
```

### Query by Importance

```bash
curl -X POST localhost:8080/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "{ queryKnowledgeGraphNode(filter: { importance: { eq: \"high\" } }) { nodeId title importance } }"}'
```

### Complex Filtering

```bash
curl -X POST localhost:8080/graphql \
  -H "Content-Type: application/json" \
  -d '{
    "query": "{ queryKnowledgeGraphNode(filter: { and: [{ semanticTags: { eq: \"introduction\" } }, { importance: { eq: \"high\" } }] }) { nodeId title semanticTags importance } }"
  }'
```

## 🔍 **Introspection**

### Get Schema Types

```bash
curl -X POST localhost:8080/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "{ __schema { types { name } } }"}'
```

### Get Available Queries

```bash
curl -X POST localhost:8080/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "{ __schema { queryType { fields { name } } } }"}'
```

### Get Available Mutations

```bash
curl -X POST localhost:8080/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "{ __schema { mutationType { fields { name } } } }"}'
```

## 🌐 **Using Ratel for GraphQL**

1. Open [http://localhost:8000](http://localhost:8000)
2. Click on the **"GraphQL"** tab (not the default DQL tab)
3. You can now use the GraphQL interface to:
   - Write and execute GraphQL queries
   - Browse the schema
   - See query results in a nice format

## 🐍 **Python Example**

```python
import requests
import json

# GraphQL endpoint
url = "http://localhost:8080/graphql"
headers = {"Content-Type": "application/json"}

# Query all nodes
query = """
{
  queryKnowledgeGraphNode {
    nodeId
    title
    semanticTags
  }
}
"""

response = requests.post(url, json={"query": query}, headers=headers)
data = response.json()

if "errors" not in data:
    nodes = data["data"]["queryKnowledgeGraphNode"]
    for node in nodes:
        print(f"Node: {node['nodeId']} - {node['title']}")
else:
    print(f"Errors: {data['errors']}")
```

## 🔄 **GraphQL vs DQL**

| Feature | GraphQL | DQL |
|---------|---------|-----|
| **Endpoint** | `/graphql` | `/query` |
| **Schema Required** | ✅ Yes | ❌ No |
| **Type Safety** | ✅ Strong | ⚠️ Flexible |
| **Standard** | ✅ GraphQL Standard | ❌ Dgraph-specific |
| **Client Tools** | ✅ Many available | ⚠️ Limited |
| **Learning Curve** | ✅ Familiar if you know GraphQL | ❌ Dgraph-specific syntax |

## 🛠️ **Client Libraries**

You can use any standard GraphQL client library:

- **JavaScript**: Apollo Client, Relay, graphql-request
- **Python**: gql, graphene, strawberry
- **Go**: github.com/machinebox/graphql
- **Java**: GraphQL Java
- **C#**: GraphQL .NET

## 🎯 **Best Practices**

1. **Use GraphQL for standard operations** - mutations, queries with filtering
2. **Use DQL for complex graph traversals** - when you need Dgraph-specific features
3. **Define proper indexes** in your schema with `@search` directives
4. **Use fragments** for reusable query parts
5. **Take advantage of variables** for dynamic queries

## 🚀 **Getting Started**

1. Your GraphQL schema is already set up
2. GraphQL endpoint is available at `http://localhost:8080/graphql`
3. Try the example queries above
4. Use Ratel's GraphQL tab for interactive testing
5. Integrate with your favorite GraphQL client library

Now you have both DQL and GraphQL available - use whichever fits your needs better! 🎉
