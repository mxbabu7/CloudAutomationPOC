"""
Cloud Mapping Agent
Maps logical architecture to cloud-specific services
"""
import yaml
from pathlib import Path


class CloudMappingAgent:
    def __init__(self):
        # Load cloud profiles
        config_path = Path(__file__).parent.parent / "config" / "cloud_profiles.yaml"
        with open(config_path, 'r') as f:
            self.cloud_profiles = yaml.safe_load(f)
    
    def run(self, architecture: dict, target_cloud: str) -> dict:
        """
        Maps logical architecture to cloud-specific services
        
        Args:
            architecture: Logical architecture specification
            target_cloud: Target cloud provider (Azure, AWS, GCP)
            
        Returns:
            Cloud-specific architecture mapping
        """
        if target_cloud not in self.cloud_profiles:
            raise ValueError(f"Unsupported cloud provider: {target_cloud}")
        
        cloud_mapping = self.cloud_profiles[target_cloud]
        mapped_layers = []
        
        for layer in architecture.get("layers", []):
            mapped_components = []
            
            for component in layer.get("components", []):
                # Map generic components to cloud-specific services
                cloud_service = self._map_component(component, cloud_mapping)
                mapped_components.append({
                    "logical_name": component,
                    "cloud_service": cloud_service,
                    "provider": target_cloud
                })
            
            mapped_layers.append({
                "layer_name": layer["name"],
                "components": mapped_components,
                "responsibilities": layer.get("responsibilities", [])
            })
        
        return {
            "target_cloud": target_cloud,
            "mapped_layers": mapped_layers,
            "original_architecture": architecture
        }
    
    def _map_component(self, component: str, cloud_mapping: dict) -> str:
        """
        Maps a logical component to a cloud-specific service
        """
        # Simple keyword-based mapping
        component_lower = component.lower()
        
        if "web" in component_lower or "app" in component_lower:
            return cloud_mapping.get("Compute Layer", "Compute Service")
        elif "cdn" in component_lower:
            return cloud_mapping.get("CDN", "CDN Service")
        elif "api" in component_lower and "gateway" in component_lower:
            return cloud_mapping.get("API Gateway", "API Gateway Service")
        elif "load balancer" in component_lower:
            return cloud_mapping.get("Load Balancer", "Load Balancer Service")
        elif "container" in component_lower or "orchestration" in component_lower:
            return cloud_mapping.get("Container Service", "Container Service")
        elif "compute" in component_lower or "instance" in component_lower:
            return cloud_mapping.get("Compute Layer", "Compute Service")
        elif "relational" in component_lower or "database" in component_lower:
            return cloud_mapping.get("Relational Database", "Database Service")
        elif "storage" in component_lower or "object" in component_lower:
            return cloud_mapping.get("Object Storage", "Storage Service")
        elif "cache" in component_lower:
            return cloud_mapping.get("NoSQL Database", "Cache Service")
        elif "identity" in component_lower:
            return cloud_mapping.get("Identity", "Identity Service")
        elif "security" in component_lower:
            return cloud_mapping.get("Security", "Security Service")
        elif "monitoring" in component_lower:
            return cloud_mapping.get("Monitoring", "Monitoring Service")
        elif "logging" in component_lower or "log" in component_lower:
            return cloud_mapping.get("Monitoring", "Logging Service")
        else:
            return "Generic Service"
