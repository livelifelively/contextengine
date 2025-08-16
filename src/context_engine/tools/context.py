"""
Context Engine Tool - Knowledge Graph Integration
Provides the init_context_engine tool using knowledge graph composition
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


def load_knowledge_graph_nodes() -> List[KnowledgeGraphNode]:
    """Load knowledge graph nodes from JSON file"""
    try:
        current_dir = Path(__file__).parent.parent
        json_file_path = current_dir / "application" / "knowledge_graph_nodes.json"
        
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        nodes = []
        for node_data in data.get("nodes", []):
            node = KnowledgeGraphNode(**node_data)
            nodes.append(node)
        
        return nodes
        
    except Exception as e:
        print(f"Error loading knowledge graph nodes: {e}")
        return []


def compose_context_from_knowledge_graph() -> str:
    """
    Compose context from knowledge graph nodes for initialization
    Returns the full methodology context using knowledge graph composition
    """
    # Load all nodes
    nodes = load_knowledge_graph_nodes()
    if not nodes:
        return "Error: No knowledge graph nodes found. Please check the knowledge_graph_nodes.json file."
    
    # For initialization, include all nodes in order of importance
    sorted_nodes = sorted(nodes, key=lambda x: (
        _get_priority_score(x.composition_rules.get("priority", "low")),
        _get_importance_score(x.metadata.get("importance", "supporting"))
    ), reverse=True)
    
    # Compose the full context - ONLY content from nodes
    composed_parts = []
    
    # Add each node's content directly
    for node in sorted_nodes:
        for line in node.content:
            composed_parts.append(line)
        composed_parts.append("")  # Add spacing between nodes
    
    return "\n".join(composed_parts)


def _get_priority_score(priority: str) -> int:
    """Convert priority string to numeric score"""
    priority_scores = {
        "high": 3,
        "medium": 2,
        "low": 1
    }
    return priority_scores.get(priority.lower(), 1)


def _get_importance_score(importance: str) -> int:
    """Convert importance string to numeric score"""
    importance_scores = {
        "foundational": 3,
        "core": 3,
        "operational": 2,
        "supporting": 1
    }
    return importance_scores.get(importance.lower(), 1)


def init_context_engine(random_string: str = "") -> str:
    """
    Initializes the conversation by providing the full context of the Context Engine's principles and methodology.
    Now uses knowledge graph composition instead of static file loading.
    
    Args:
        random_string: Dummy parameter for no-parameter tools
        
    Returns:
        String containing the composed methodology context from knowledge graph nodes
    """
    try:
        # Use knowledge graph composition
        context = compose_context_from_knowledge_graph()
        
        if context.startswith("Error:"):
            return f"❌ Context Engine Initialization Failed:\n{context}"
        
        return context
        
    except Exception as e:
        return f"❌ Error initializing Context Engine: {str(e)}"
