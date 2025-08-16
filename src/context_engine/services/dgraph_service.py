"""
Dgraph Service Layer
Provides CRUD operations for the knowledge graph using Dgraph
"""

import json
import logging
from typing import List, Optional, Dict, Any
from contextlib import asynccontextmanager

import pydgraph
from pydantic import BaseModel

from ..application.knowledge_graph_loader import KnowledgeGraphNode

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

logger = logging.getLogger(__name__)


class DgraphService:
    """Service class for Dgraph operations"""
    
    def __init__(self, dgraph_host: str = "localhost", dgraph_port: int = 9080):
        self.dgraph_host = dgraph_host
        self.dgraph_port = dgraph_port
        self._client_stub = None
        self._client = None
    
    def __enter__(self):
        """Context manager entry"""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.disconnect()
    
    def connect(self):
        """Establish connection to Dgraph"""
        try:
            self._client_stub = pydgraph.DgraphClientStub(f"{self.dgraph_host}:{self.dgraph_port}")
            self._client = pydgraph.DgraphClient(self._client_stub)
            logger.info(f"Connected to Dgraph at {self.dgraph_host}:{self.dgraph_port}")
        except Exception as e:
            logger.error(f"Failed to connect to Dgraph: {e}")
            raise
    
    def disconnect(self):
        """Close connection to Dgraph"""
        if self._client_stub:
            self._client_stub.close()
            logger.info("Disconnected from Dgraph")
    
    def setup_schema(self):
        """Set up the Dgraph schema for knowledge graph nodes"""
        schema = """
        <node_id>: string @index(exact) .
        <title>: string @index(term) .
        <content>: [string] .
        <metadata>: string .
        <relationships>: string .
        <semantic_tags>: [string] @index(exact) .
        <composition_rules>: string .
        <section_type>: string @index(exact) .
        <importance>: string @index(exact) .
        
        type KnowledgeGraphNode {
            node_id: string
            title: string
            content: [string]
            metadata: string
            relationships: string
            semantic_tags: [string]
            composition_rules: string
            section_type: string
            importance: string
        }
        """
        
        try:
            op = pydgraph.Operation(schema=schema)
            self._client.alter(op)
            logger.info("Schema setup completed successfully")
        except Exception as e:
            logger.error(f"Failed to setup schema: {e}")
            raise
    
    def create_node(self, node: KnowledgeGraphNode) -> str:
        """
        Create a new knowledge graph node in Dgraph
        
        Args:
            node: KnowledgeGraphNode object to create
            
        Returns:
            str: UID of the created node
        """
        txn = self._client.txn()
        try:
            # Convert node to Dgraph format
            dgraph_node = {
                "uid": "_:node",
                "dgraph.type": "KnowledgeGraphNode",
                "node_id": node.id,
                "title": node.title,
                "content": node.content,
                "metadata": json.dumps(node.metadata),
                "relationships": json.dumps(node.relationships),
                "semantic_tags": node.semantic_tags,
                "composition_rules": json.dumps(node.composition_rules),
                "section_type": node.metadata.get("section_type", ""),
                "importance": node.metadata.get("importance", ""),
            }
            
            # Create mutation using set_json with proper JSON string
            mu = pydgraph.Mutation()
            mu.set_json = json.dumps(dgraph_node).encode('utf-8')
            response = txn.mutate(mu)
            txn.commit()
            
            # Extract UID from response
            uid = response.uids.get("node", "")
            logger.info(f"Created node with UID: {uid}")
            return uid
            
        except Exception as e:
            logger.error(f"Failed to create node: {e}")
            txn.discard()
            raise
        finally:
            txn.discard()
    
    def get_node_by_id(self, node_id: str) -> Optional[KnowledgeGraphNode]:
        """
        Retrieve a node by its ID
        
        Args:
            node_id: ID of the node to retrieve
            
        Returns:
            KnowledgeGraphNode if found, None otherwise
        """
        query = """
        query getNode($nodeId: string) {
            node(func: eq(node_id, $nodeId)) {
                uid
                node_id
                title
                content
                metadata
                relationships
                semantic_tags
                composition_rules
            }
        }
        """
        
        try:
            variables = {"$nodeId": node_id}
            txn = self._client.txn(read_only=True)
            try:
                response = txn.query(query, variables=variables)
                data = json.loads(response.json)
            finally:
                txn.discard()
            
            if not data.get("node"):
                return None
            
            node_data = data["node"][0]
            
            # Convert back to KnowledgeGraphNode
            return KnowledgeGraphNode(
                id=node_data["node_id"],
                title=node_data["title"],
                content=node_data["content"],
                metadata=json.loads(node_data["metadata"]) if node_data.get("metadata") else {},
                relationships=json.loads(node_data["relationships"]) if node_data.get("relationships") else {},
                semantic_tags=node_data.get("semantic_tags", []),
                composition_rules=json.loads(node_data["composition_rules"]) if node_data.get("composition_rules") else {}
            )
            
        except Exception as e:
            logger.error(f"Failed to retrieve node {node_id}: {e}")
            return None
    
    def get_nodes_by_semantic_tag(self, tag: str) -> List[KnowledgeGraphNode]:
        """
        Retrieve nodes by semantic tag
        
        Args:
            tag: Semantic tag to search for
            
        Returns:
            List of KnowledgeGraphNode objects
        """
        query = """
        query getNodesByTag($tag: string) {
            nodes(func: eq(semantic_tags, $tag)) {
                uid
                node_id
                title
                content
                metadata
                relationships
                semantic_tags
                composition_rules
            }
        }
        """
        
        try:
            variables = {"$tag": tag}
            txn = self._client.txn(read_only=True)
            try:
                response = txn.query(query, variables=variables)
                data = json.loads(response.json)
            finally:
                txn.discard()
            
            nodes = []
            for node_data in data.get("nodes", []):
                node = KnowledgeGraphNode(
                    id=node_data["node_id"],
                    title=node_data["title"],
                    content=node_data["content"],
                    metadata=json.loads(node_data["metadata"]) if node_data.get("metadata") else {},
                    relationships=json.loads(node_data["relationships"]) if node_data.get("relationships") else {},
                    semantic_tags=node_data.get("semantic_tags", []),
                    composition_rules=json.loads(node_data["composition_rules"]) if node_data.get("composition_rules") else {}
                )
                nodes.append(node)
            
            return nodes
            
        except Exception as e:
            logger.error(f"Failed to retrieve nodes by tag {tag}: {e}")
            return []
    
    def update_node(self, node: KnowledgeGraphNode) -> bool:
        """
        Update an existing node
        
        Args:
            node: KnowledgeGraphNode object with updated data
            
        Returns:
            bool: True if successful, False otherwise
        """
        # First, find the node's UID
        existing_node_data = self._get_node_uid_by_id(node.id)
        if not existing_node_data:
            logger.warning(f"Node {node.id} not found for update")
            return False
        
        txn = self._client.txn()
        try:
            # Update the node
            dgraph_node = {
                "uid": existing_node_data["uid"],
                "node_id": node.id,
                "title": node.title,
                "content": node.content,
                "metadata": json.dumps(node.metadata),
                "relationships": json.dumps(node.relationships),
                "semantic_tags": node.semantic_tags,
                "composition_rules": json.dumps(node.composition_rules),
                "section_type": node.metadata.get("section_type", ""),
                "importance": node.metadata.get("importance", ""),
            }
            
            mu = pydgraph.Mutation()
            mu.set_json = json.dumps(dgraph_node).encode('utf-8')
            txn.mutate(mu)
            txn.commit()
            
            logger.info(f"Updated node {node.id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to update node {node.id}: {e}")
            txn.discard()
            return False
        finally:
            txn.discard()
    
    def delete_node(self, node_id: str) -> bool:
        """
        Delete a node by its ID
        
        Args:
            node_id: ID of the node to delete
            
        Returns:
            bool: True if successful, False otherwise
        """
        # First, find the node's UID
        existing_node_data = self._get_node_uid_by_id(node_id)
        if not existing_node_data:
            logger.warning(f"Node {node_id} not found for deletion")
            return False
        
        txn = self._client.txn()
        try:
            mu = pydgraph.Mutation()
            mu.delete_json = json.dumps({"uid": existing_node_data["uid"]}).encode('utf-8')
            txn.mutate(mu)
            txn.commit()
            
            logger.info(f"Deleted node {node_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to delete node {node_id}: {e}")
            txn.discard()
            return False
        finally:
            txn.discard()
    
    def get_all_nodes(self) -> List[KnowledgeGraphNode]:
        """
        Retrieve all knowledge graph nodes
        
        Returns:
            List of all KnowledgeGraphNode objects
        """
        query = """
        {
            nodes(func: type(KnowledgeGraphNode)) {
                uid
                node_id
                title
                content
                metadata
                relationships
                semantic_tags
                composition_rules
            }
        }
        """
        
        try:
            txn = self._client.txn(read_only=True)
            try:
                response = txn.query(query)
                data = json.loads(response.json)
            finally:
                txn.discard()
            
            nodes = []
            for node_data in data.get("nodes", []):
                node = KnowledgeGraphNode(
                    id=node_data["node_id"],
                    title=node_data["title"],
                    content=node_data["content"],
                    metadata=json.loads(node_data["metadata"]) if node_data.get("metadata") else {},
                    relationships=json.loads(node_data["relationships"]) if node_data.get("relationships") else {},
                    semantic_tags=node_data.get("semantic_tags", []),
                    composition_rules=json.loads(node_data["composition_rules"]) if node_data.get("composition_rules") else {}
                )
                nodes.append(node)
            
            return nodes
            
        except Exception as e:
            logger.error(f"Failed to retrieve all nodes: {e}")
            return []
    
    def _get_node_uid_by_id(self, node_id: str) -> Optional[Dict[str, Any]]:
        """
        Get node UID by ID (internal helper method)
        
        Args:
            node_id: ID of the node
            
        Returns:
            Dict with uid and other data if found, None otherwise
        """
        query = """
        query getNodeUID($nodeId: string) {
            node(func: eq(node_id, $nodeId)) {
                uid
            }
        }
        """
        
        try:
            variables = {"$nodeId": node_id}
            txn = self._client.txn(read_only=True)
            try:
                response = txn.query(query, variables=variables)
                data = json.loads(response.json)
            finally:
                txn.discard()
            
            if data.get("node"):
                return data["node"][0]
            return None
            
        except Exception as e:
            logger.error(f"Failed to get UID for node {node_id}: {e}")
            return None
    
    def drop_all(self):
        """
        Drop all data (useful for testing)
        """
        try:
            op = pydgraph.Operation(drop_all=True)
            self._client.alter(op)
            logger.info("Dropped all data")
        except Exception as e:
            logger.error(f"Failed to drop all data: {e}")
            raise
    
    def setup_graphql_schema(self, schema: str = None):
        """
        Set up GraphQL schema for the knowledge graph
        
        Args:
            schema: GraphQL schema string. If None, uses default schema.
        """
        if not REQUESTS_AVAILABLE:
            raise ImportError("requests library is required for GraphQL operations. Install with: pip install requests")
        
        if schema is None:
            schema = """
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
            """
        
        try:
            import requests
            url = f"http://{self.dgraph_host}:8080/admin/schema"
            headers = {"Content-Type": "text/plain"}
            
            response = requests.post(url, data=schema, headers=headers)
            if response.status_code == 200:
                result = response.json()
                if result.get("data", {}).get("code") == "Success":
                    logger.info("GraphQL schema set up successfully")
                    return True
                else:
                    logger.error(f"Failed to set up GraphQL schema: {result}")
                    return False
            else:
                logger.error(f"HTTP error setting up GraphQL schema: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            logger.error(f"Error setting up GraphQL schema: {e}")
            return False
    
    def graphql_query(self, query: str, variables: Dict[str, Any] = None):
        """
        Execute a GraphQL query
        
        Args:
            query: GraphQL query string
            variables: Optional variables for the query
            
        Returns:
            Query result or None if error
        """
        if not REQUESTS_AVAILABLE:
            raise ImportError("requests library is required for GraphQL operations. Install with: pip install requests")
        
        try:
            import requests
            url = f"http://{self.dgraph_host}:8080/graphql"
            headers = {"Content-Type": "application/json"}
            
            payload = {"query": query}
            if variables:
                payload["variables"] = variables
            
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                result = response.json()
                if "errors" in result:
                    logger.error(f"GraphQL errors: {result['errors']}")
                    return None
                return result.get("data")
            else:
                logger.error(f"HTTP error in GraphQL query: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            logger.error(f"Error executing GraphQL query: {e}")
            return None
    
    def create_node_graphql(self, node: KnowledgeGraphNode):
        """
        Create a node using GraphQL mutation
        
        Args:
            node: KnowledgeGraphNode to create
            
        Returns:
            Created node data or None if error
        """
        mutation = """
        mutation CreateNode($input: [AddKnowledgeGraphNodeInput!]!) {
          addKnowledgeGraphNode(input: $input) {
            knowledgeGraphNode {
              nodeId
              title
              semanticTags
            }
          }
        }
        """
        
        variables = {
            "input": [{
                "nodeId": node.id,
                "title": node.title,
                "content": node.content,
                "metadata": json.dumps(node.metadata),
                "relationships": json.dumps(node.relationships),
                "semanticTags": node.semantic_tags,
                "compositionRules": json.dumps(node.composition_rules),
                "sectionType": node.metadata.get("section_type", ""),
                "importance": node.metadata.get("importance", "")
            }]
        }
        
        result = self.graphql_query(mutation, variables)
        if result and "addKnowledgeGraphNode" in result:
            return result["addKnowledgeGraphNode"]["knowledgeGraphNode"]
        return None
    
    def get_nodes_by_tag_graphql(self, tag: str):
        """
        Get nodes by semantic tag using GraphQL
        
        Args:
            tag: Semantic tag to search for
            
        Returns:
            List of nodes or empty list if error
        """
        query = """
        query GetNodesByTag($tag: String!) {
          queryKnowledgeGraphNode(filter: { semanticTags: { eq: $tag } }) {
            nodeId
            title
            content
            semanticTags
            sectionType
            importance
          }
        }
        """
        
        variables = {"tag": tag}
        result = self.graphql_query(query, variables)
        
        if result and "queryKnowledgeGraphNode" in result:
            return result["queryKnowledgeGraphNode"]
        return []


# Helper function to get service instance
def get_dgraph_service(dgraph_host: str = "localhost", dgraph_port: int = 9080) -> DgraphService:
    """
    Create and return a DgraphService instance
    
    Args:
        dgraph_host: Dgraph host (default: localhost)
        dgraph_port: Dgraph port (default: 9080)
        
    Returns:
        DgraphService instance
    """
    return DgraphService(dgraph_host=dgraph_host, dgraph_port=dgraph_port)