"""
Knowledge Graph Loader
Utility to load and validate knowledge graph nodes from JSON
"""

import json
from pathlib import Path
from typing import List
from pydantic import BaseModel, Field


# Minimal schema definition for this module
class KnowledgeGraphNode(BaseModel):
    """A node in the knowledge graph representing a section of methodology"""
    id: str = Field(..., description="Unique identifier for the node")
    title: str = Field(..., description="Title of the section")
    content: List[str] = Field(..., description="The actual content of the section as array of lines")
    metadata: dict = Field(..., description="Metadata about the node")
    relationships: dict = Field(..., description="Relationships to other nodes")
    semantic_tags: List[str] = Field(..., description="Semantic tags for search and composition")
    composition_rules: dict = Field(..., description="Rules for context composition")


def load_knowledge_graph_nodes(json_file_path: str = None) -> List[KnowledgeGraphNode]:
    """
    Load knowledge graph nodes from JSON file
    
    Args:
        json_file_path: Path to JSON file, defaults to knowledge_graph_nodes.json in same directory
        
    Returns:
        List of validated KnowledgeGraphNode objects
    """
    if json_file_path is None:
        # Default to the JSON file in the same directory
        current_dir = Path(__file__).parent
        json_file_path = current_dir / "knowledge_graph_nodes.json"
    
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Validate each node
        nodes = []
        for node_data in data.get("nodes", []):
            node = KnowledgeGraphNode(**node_data)
            nodes.append(node)
        
        print(f"✅ Successfully loaded {len(nodes)} knowledge graph nodes")
        return nodes
        
    except FileNotFoundError:
        print(f"❌ JSON file not found: {json_file_path}")
        return []
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON format: {e}")
        return []
    except Exception as e:
        print(f"❌ Error loading nodes: {e}")
        return []


def get_node_by_id(nodes: List[KnowledgeGraphNode], node_id: str) -> KnowledgeGraphNode:
    """
    Get a specific node by its ID
    
    Args:
        nodes: List of knowledge graph nodes
        node_id: ID of the node to find
        
    Returns:
        KnowledgeGraphNode if found, None otherwise
    """
    for node in nodes:
        if node.id == node_id:
            return node
    return None


def get_nodes_by_semantic_tag(nodes: List[KnowledgeGraphNode], tag: str) -> List[KnowledgeGraphNode]:
    """
    Get nodes that have a specific semantic tag
    
    Args:
        nodes: List of knowledge graph nodes
        tag: Semantic tag to search for
        
    Returns:
        List of nodes that have the specified tag
    """
    matching_nodes = []
    for node in nodes:
        if tag in node.semantic_tags:
            matching_nodes.append(node)
    return matching_nodes


def get_nodes_by_type(nodes: List[KnowledgeGraphNode], section_type: str) -> List[KnowledgeGraphNode]:
    """
    Get nodes by section type
    
    Args:
        nodes: List of knowledge graph nodes
        section_type: Type of section to filter by
        
    Returns:
        List of nodes of the specified type
    """
    matching_nodes = []
    for node in nodes:
        if node.metadata.get("section_type") == section_type:
            matching_nodes.append(node)
    return matching_nodes


def content_to_string(node: KnowledgeGraphNode) -> str:
    """
    Convert node content array to string with newline separators
    
    Args:
        node: KnowledgeGraphNode object
        
    Returns:
        Content as string with newlines
    """
    return "\n".join(node.content)


def content_to_markdown(node: KnowledgeGraphNode) -> str:
    """
    Convert node content to markdown format with title
    
    Args:
        node: KnowledgeGraphNode object
        
    Returns:
        Content as markdown string
    """
    markdown_lines = [f"# {node.title}", ""]
    markdown_lines.extend(node.content)
    return "\n".join(markdown_lines)


# Test the loader
if __name__ == "__main__":
    print("Testing Knowledge Graph Loader...")
    print("=" * 50)
    
    # Load nodes
    nodes = load_knowledge_graph_nodes()
    
    if nodes:
        print(f"\n📊 Loaded {len(nodes)} nodes:")
        for node in nodes:
            print(f"  • {node.id}: {node.title} ({node.metadata.get('section_type', 'unknown')})")
            print(f"    Content lines: {len(node.content)}")
        
        # Test getting node by ID
        print(f"\n🔍 Testing get_node_by_id:")
        node = get_node_by_id(nodes, "context_engine.1.document_objective")
        if node:
            print(f"  ✅ Found node: {node.title}")
            print(f"  Content lines: {len(node.content)}")
        else:
            print(f"  ❌ Node not found")
        
        # Test getting nodes by semantic tag
        print(f"\n🏷️ Testing get_nodes_by_semantic_tag:")
        intro_nodes = get_nodes_by_semantic_tag(nodes, "introduction")
        print(f"  Found {len(intro_nodes)} nodes with 'introduction' tag")
        
        # Test getting nodes by type
        print(f"\n📋 Testing get_nodes_by_type:")
        intro_type_nodes = get_nodes_by_type(nodes, "introduction")
        print(f"  Found {len(intro_type_nodes)} nodes of type 'introduction'")
        
        # Show relationships
        print(f"\n🔗 Node relationships:")
        for node in nodes:
            print(f"  {node.id} leads to: {node.relationships.get('leads_to', [])}")
        
        # Test content conversion
        print(f"\n📝 Testing content conversion:")
        if nodes:
            node = nodes[0]
            print(f"  Content as string (first 100 chars): {content_to_string(node)[:100]}...")
            print(f"  Content as markdown (first 100 chars): {content_to_markdown(node)[:100]}...")
    else:
        print("❌ No nodes loaded")
