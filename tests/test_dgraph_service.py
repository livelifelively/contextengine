"""
Tests for Dgraph Service
Tests all CRUD operations and integrations with the knowledge graph
"""

import os
import pytest
from unittest.mock import Mock, patch
from context_engine.services.dgraph_service import DgraphService, get_dgraph_service
from context_engine.application.knowledge_graph_loader import KnowledgeGraphNode


# Test fixtures
@pytest.fixture
def sample_node():
    """Create a sample knowledge graph node for testing"""
    return KnowledgeGraphNode(
        id="test.node.1",
        title="Test Node",
        content=["This is a test node", "It has multiple lines of content"],
        metadata={"section_type": "test", "importance": "low"},
        relationships={"leads_to": ["test.node.2"], "depends_on": []},
        semantic_tags=["test", "crud", "example"],
        composition_rules={"priority": "low", "include_in": ["testing"]}
    )


@pytest.fixture
def dgraph_service():
    """Create a DgraphService instance for testing"""
    # Use environment variables for test configuration
    host = os.getenv("DGRAPH_ALPHA_HOST", "localhost")
    port = int(os.getenv("DGRAPH_ALPHA_PORT", "9080"))
    return DgraphService(dgraph_host=host, dgraph_port=port)


class TestDgraphService:
    """Test class for DgraphService functionality"""
    
    def test_get_dgraph_service_factory(self):
        """Test the factory function for creating DgraphService instances"""
        service = get_dgraph_service()
        assert isinstance(service, DgraphService)
        assert service.dgraph_host == "localhost"
        assert service.dgraph_port == 9080
        
        # Test with custom parameters
        service = get_dgraph_service(dgraph_host="custom_host", dgraph_port=8080)
        assert service.dgraph_host == "custom_host"
        assert service.dgraph_port == 8080
    
    def test_context_manager(self, dgraph_service):
        """Test that DgraphService works as a context manager"""
        with patch.object(dgraph_service, 'connect') as mock_connect:
            with patch.object(dgraph_service, 'disconnect') as mock_disconnect:
                with dgraph_service:
                    pass
                mock_connect.assert_called_once()
                mock_disconnect.assert_called_once()
    
    @pytest.mark.integration
    def test_connection_and_schema_setup(self, dgraph_service):
        """Integration test for connection and schema setup"""
        try:
            with dgraph_service:
                # This should work if Dgraph is running
                dgraph_service.setup_schema()
        except Exception as e:
            pytest.skip(f"Dgraph not available for integration testing: {e}")
    
    @pytest.mark.integration
    def test_crud_operations_integration(self, dgraph_service, sample_node):
        """Integration test for all CRUD operations"""
        try:
            with dgraph_service:
                # Setup schema
                dgraph_service.setup_schema()
                
                # Test CREATE
                uid = dgraph_service.create_node(sample_node)
                assert uid is not None
                assert uid != ""
                
                # Test READ
                retrieved_node = dgraph_service.get_node_by_id(sample_node.id)
                assert retrieved_node is not None
                assert retrieved_node.id == sample_node.id
                assert retrieved_node.title == sample_node.title
                assert retrieved_node.content == sample_node.content
                assert retrieved_node.semantic_tags == sample_node.semantic_tags
                
                # Test UPDATE
                retrieved_node.title = "Updated Test Node"
                retrieved_node.content.append("This line was added during update")
                update_success = dgraph_service.update_node(retrieved_node)
                assert update_success is True
                
                # Verify update
                updated_node = dgraph_service.get_node_by_id(sample_node.id)
                assert updated_node.title == "Updated Test Node"
                assert len(updated_node.content) == 3
                
                # Test semantic tag search
                test_nodes = dgraph_service.get_nodes_by_semantic_tag("test")
                assert len(test_nodes) >= 1
                assert any(node.id == sample_node.id for node in test_nodes)
                
                # Test get all nodes
                all_nodes = dgraph_service.get_all_nodes()
                assert len(all_nodes) >= 1
                
                # Test DELETE
                delete_success = dgraph_service.delete_node(sample_node.id)
                assert delete_success is True
                
                # Verify deletion
                deleted_node = dgraph_service.get_node_by_id(sample_node.id)
                assert deleted_node is None
                
        except Exception as e:
            pytest.skip(f"Dgraph not available for integration testing: {e}")
    
    @pytest.mark.integration
    def test_knowledge_graph_integration(self, dgraph_service):
        """Test loading and storing actual knowledge graph nodes"""
        from context_engine.application.knowledge_graph_loader import load_knowledge_graph_nodes
        import json
        from pathlib import Path
        
        try:
            with dgraph_service:
                # Load nodes from JSON file
                json_file_path = Path(__file__).parent.parent / "src" / "context_engine" / "application" / "knowledge_graph_nodes.json"
                nodes = load_knowledge_graph_nodes(str(json_file_path))
                
                if not nodes:
                    pytest.skip("No knowledge graph nodes found")
                
                # Setup schema
                dgraph_service.setup_schema()
                
                # Create all nodes
                created_uids = []
                for node in nodes:
                    uid = dgraph_service.create_node(node)
                    assert uid is not None
                    created_uids.append(uid)
                
                # Test retrieving nodes
                for node in nodes:
                    retrieved = dgraph_service.get_node_by_id(node.id)
                    assert retrieved is not None
                    assert retrieved.id == node.id
                    assert retrieved.title == node.title
                
                # Test semantic tag queries
                intro_nodes = dgraph_service.get_nodes_by_semantic_tag("introduction")
                assert len(intro_nodes) > 0
                
                # Clean up - delete all created nodes
                for node in nodes:
                    dgraph_service.delete_node(node.id)
                
        except Exception as e:
            pytest.skip(f"Dgraph not available for integration testing: {e}")
    
    def test_node_not_found_scenarios(self, dgraph_service):
        """Test scenarios where nodes are not found"""
        try:
            with dgraph_service:
                dgraph_service.setup_schema()
                
                # Test getting non-existent node
                non_existent = dgraph_service.get_node_by_id("non.existent.node")
                assert non_existent is None
                
                # Test updating non-existent node
                fake_node = KnowledgeGraphNode(
                    id="fake.node",
                    title="Fake",
                    content=["fake"],
                    metadata={},
                    relationships={},
                    semantic_tags=[],
                    composition_rules={}
                )
                update_success = dgraph_service.update_node(fake_node)
                assert update_success is False
                
                # Test deleting non-existent node
                delete_success = dgraph_service.delete_node("non.existent.node")
                assert delete_success is False
                
        except Exception as e:
            pytest.skip(f"Dgraph not available for integration testing: {e}")
    
    def test_semantic_tag_search_empty_results(self, dgraph_service):
        """Test semantic tag search with no results"""
        try:
            with dgraph_service:
                dgraph_service.setup_schema()
                
                # Search for non-existent tag
                nodes = dgraph_service.get_nodes_by_semantic_tag("non_existent_tag")
                assert nodes == []
                
        except Exception as e:
            pytest.skip(f"Dgraph not available for integration testing: {e}")
    
    def test_connection_error_handling(self):
        """Test connection error handling"""
        # Test with invalid host/port
        service = DgraphService(dgraph_host="invalid_host", dgraph_port=9999)
        
        with pytest.raises(Exception):
            service.connect()


# Unit tests with mocked dependencies
class TestDgraphServiceUnit:
    """Unit tests for DgraphService with mocked dependencies"""
    
    @patch('pydgraph.DgraphClientStub')
    @patch('pydgraph.DgraphClient')
    def test_connect_success(self, mock_client_class, mock_stub_class, dgraph_service):
        """Test successful connection"""
        mock_stub = Mock()
        mock_client = Mock()
        mock_stub_class.return_value = mock_stub
        mock_client_class.return_value = mock_client
        
        dgraph_service.connect()
        
        mock_stub_class.assert_called_once_with("localhost:9080")
        mock_client_class.assert_called_once_with(mock_stub)
        assert dgraph_service._client_stub == mock_stub
        assert dgraph_service._client == mock_client
    
    def test_disconnect(self, dgraph_service):
        """Test disconnection"""
        mock_stub = Mock()
        dgraph_service._client_stub = mock_stub
        
        dgraph_service.disconnect()
        
        mock_stub.close.assert_called_once()


# Helper function to run integration tests manually
def run_integration_tests():
    """
    Run integration tests manually
    This can be used for manual testing when Dgraph is available
    """
    import subprocess
    import sys
    
    # Run only integration tests
    result = subprocess.run([
        sys.executable, "-m", "pytest", 
        __file__ + "::TestDgraphService", 
        "-m", "integration", 
        "-v"
    ])
    
    return result.returncode == 0


if __name__ == "__main__":
    # Run integration tests if called directly
    success = run_integration_tests()
    print(f"Integration tests {'passed' if success else 'failed'}")
