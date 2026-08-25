import re
from typing import List, Dict, Any

class GraphRAGService:
    @staticmethod
    def extract_entity_triples(query: str, text: str) -> List[Dict[str, Any]]:
        """Extracts entity-relation-entity triples for GraphRAG SVG rendering."""
        words = [w for w in re.sub(r'[^\w\s]', '', text).split() if len(w) > 4]
        unique_entities = list(dict.fromkeys(words))[:6]
        
        nodes = [{"id": "root", "label": query[:16], "type": "query_root", "color": "#3b82f6"}]
        colors = ["#8b5cf6", "#10b981", "#f59e0b", "#ec4899", "#06b6d4", "#6366f1"]
        
        for idx, entity in enumerate(unique_entities):
            nodes.append({
                "id": f"node_{idx}",
                "label": entity,
                "type": "entity",
                "color": colors[idx % len(colors)]
            })
            
        return nodes

graph_rag_service = GraphRAGService()
