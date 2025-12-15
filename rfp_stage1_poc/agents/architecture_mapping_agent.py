"""
Stage 2: Architecture Mapping Agent
Maps requirements to cloud services, architecture patterns, and compliance levels
"""

import json
import os
from typing import List, Dict, Any, Optional


def map_architecture(
    requirements: List[Dict[str, Any]], 
    cloud_provider: str = "azure",
    llm_client: Optional[Any] = None
) -> List[Dict[str, Any]]:
    """
    Map requirements to cloud architecture solutions
    
    Args:
        requirements: List of requirements from Stage 1
        cloud_provider: Target cloud provider (azure, aws, gcp)
        llm_client: Optional LLM client for intelligent mapping
        
    Returns:
        List of architecture mappings with services, patterns, and compliance
    """
    
    if llm_client:
        return _map_with_llm(requirements, cloud_provider, llm_client)
    else:
        # Fallback to rule-based mapping
        return _map_with_rules(requirements, cloud_provider)


def _map_with_llm(
    requirements: List[Dict[str, Any]], 
    cloud_provider: str,
    client: Any
) -> List[Dict[str, Any]]:
    """Map requirements to architecture using LLM"""
    
    # Prepare requirements summary for LLM
    req_summary = []
    for req in requirements[:20]:  # Limit to first 20 for context
        req_summary.append({
            "id": req.get("id", ""),
            "text": req.get("text", ""),
            "type": req.get("type", "")
        })
    
    system_prompt = f"""You are a senior cloud solution architect specializing in {cloud_provider.upper()}.

For each requirement, recommend:
1. Cloud service(s) to fulfill the requirement
2. Architecture pattern (e.g., Active-Active, Active-Passive, Microservices, etc.)
3. Compliance level: "Fully Compliant", "Partially Compliant", or "Not Compliant"
4. Assumptions or dependencies
5. Implementation notes

Return ONLY valid JSON array with no additional text."""

    user_prompt = f"""Map these requirements to {cloud_provider.upper()} architecture:

{json.dumps(req_summary, indent=2)}

Return JSON array following this schema:
[
  {{
    "req_id": "M-001",
    "requirement": "Brief requirement text",
    "cloud_service": "Azure Front Door",
    "additional_services": ["Azure Traffic Manager", "Azure Load Balancer"],
    "architecture_pattern": "Active-Active Multi-Region",
    "compliance_level": "Fully Compliant",
    "assumptions": ["Multi-region deployment", "Health monitoring configured"],
    "implementation_notes": "Use Front Door for global load balancing with backend pools in multiple regions"
  }}
]"""

    try:
        response = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o-mini")),
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.1
        )
        
        content = response.choices[0].message.content
        
        # Parse JSON
        try:
            # Try to extract JSON from code blocks if present
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            
            mappings = json.loads(content)
            
            # Validate structure
            if isinstance(mappings, list) and len(mappings) > 0:
                return mappings
            else:
                print("[WARN] Invalid LLM response structure, using fallback")
                return _map_with_rules(requirements, cloud_provider)
                
        except json.JSONDecodeError:
            print("[WARN] Failed to parse LLM response, using fallback")
            return _map_with_rules(requirements, cloud_provider)
            
    except Exception as e:
        print(f"[WARN] LLM mapping failed: {e}, using fallback")
        return _map_with_rules(requirements, cloud_provider)


def _map_with_rules(
    requirements: List[Dict[str, Any]], 
    cloud_provider: str
) -> List[Dict[str, Any]]:
    """Rule-based architecture mapping (fallback)"""
    
    # Cloud service mappings
    service_map = {
        "azure": {
            "availability": ["Azure Front Door", "Azure Traffic Manager", "Availability Zones"],
            "disaster recovery": ["Azure Site Recovery", "Geo-redundant Storage", "Azure Backup"],
            "compute": ["Azure Virtual Machines", "Azure App Service", "Azure Container Instances"],
            "storage": ["Azure Blob Storage", "Azure Files", "Azure Disk Storage"],
            "database": ["Azure SQL Database", "Azure Cosmos DB", "Azure Database for PostgreSQL"],
            "networking": ["Azure Virtual Network", "Azure VPN Gateway", "Azure ExpressRoute"],
            "security": ["Azure Key Vault", "Azure AD", "Azure Security Center"],
            "monitoring": ["Azure Monitor", "Application Insights", "Log Analytics"],
            "kubernetes": ["Azure Kubernetes Service (AKS)", "Azure Container Registry"],
            "serverless": ["Azure Functions", "Azure Logic Apps", "Azure Event Grid"]
        },
        "aws": {
            "availability": ["AWS CloudFront", "Route 53", "Multi-AZ"],
            "disaster recovery": ["AWS Backup", "S3 Cross-Region Replication", "AWS DRS"],
            "compute": ["EC2", "ECS", "Lambda"],
            "storage": ["S3", "EBS", "EFS"],
            "database": ["RDS", "DynamoDB", "Aurora"],
            "networking": ["VPC", "Direct Connect", "VPN"],
            "security": ["IAM", "KMS", "Security Hub"],
            "monitoring": ["CloudWatch", "X-Ray", "CloudTrail"],
            "kubernetes": ["EKS", "ECR"],
            "serverless": ["Lambda", "API Gateway", "EventBridge"]
        },
        "gcp": {
            "availability": ["Cloud CDN", "Cloud DNS", "Multi-Region"],
            "disaster recovery": ["Cloud Backup", "Cross-Region Replication"],
            "compute": ["Compute Engine", "Cloud Run", "GKE"],
            "storage": ["Cloud Storage", "Persistent Disk", "Filestore"],
            "database": ["Cloud SQL", "Firestore", "Spanner"],
            "networking": ["VPC", "Cloud VPN", "Cloud Interconnect"],
            "security": ["IAM", "Cloud KMS", "Security Command Center"],
            "monitoring": ["Cloud Monitoring", "Cloud Logging", "Cloud Trace"],
            "kubernetes": ["GKE", "Artifact Registry"],
            "serverless": ["Cloud Functions", "Cloud Run", "Eventarc"]
        }
    }
    
    mappings = []
    services = service_map.get(cloud_provider.lower(), service_map["azure"])
    
    for req in requirements:
        req_text = req.get("text", "").lower()
        req_id = req.get("id", "")
        req_type = req.get("type", "")
        
        # Simple keyword matching for demo
        service = "To Be Determined"
        pattern = "Standard"
        compliance = "Fully Compliant" if req_type == "Mandatory" else "Compliant"
        additional = []
        assumptions = []
        notes = ""
        
        # Match keywords to services
        if any(word in req_text for word in ["availability", "ha", "high availability", "uptime"]):
            service = services["availability"][0]
            additional = services["availability"][1:]
            pattern = "Active-Active Multi-Region"
            assumptions = ["Multi-region deployment", "Health monitoring configured"]
            notes = "Implement global load balancing with automated failover"
            
        elif any(word in req_text for word in ["disaster recovery", "dr", "backup", "failover"]):
            service = services["disaster recovery"][0]
            additional = services["disaster recovery"][1:]
            pattern = "Pilot Light / Warm Standby"
            assumptions = ["RTO/RPO requirements defined", "Regular backup testing"]
            notes = "Configure automated replication and recovery procedures"
            
        elif any(word in req_text for word in ["compute", "vm", "server", "instance"]):
            service = services["compute"][0]
            additional = services["compute"][1:2]
            pattern = "Auto-scaling Groups"
            assumptions = ["Load patterns understood", "Scaling policies defined"]
            notes = "Use managed compute services with auto-scaling"
            
        elif any(word in req_text for word in ["storage", "data", "file"]):
            service = services["storage"][0]
            additional = services["storage"][1:2]
            pattern = "Tiered Storage"
            assumptions = ["Data lifecycle policies", "Access patterns analyzed"]
            notes = "Implement appropriate storage tier based on access frequency"
            
        elif any(word in req_text for word in ["database", "sql", "nosql", "data store"]):
            service = services["database"][0]
            additional = services["database"][1:2]
            pattern = "Managed Database Service"
            assumptions = ["Database requirements specified", "Backup strategy defined"]
            notes = "Use fully managed database with automatic backups"
            
        elif any(word in req_text for word in ["network", "vpn", "connectivity"]):
            service = services["networking"][0]
            additional = services["networking"][1:2]
            pattern = "Hub-Spoke Topology"
            assumptions = ["Network segmentation required", "Security policies defined"]
            notes = "Implement secure network architecture with proper isolation"
            
        elif any(word in req_text for word in ["security", "encryption", "compliance", "authentication"]):
            service = services["security"][0]
            additional = services["security"][1:2]
            pattern = "Zero Trust Architecture"
            assumptions = ["Security requirements documented", "Compliance standards identified"]
            notes = "Implement defense-in-depth security strategy"
            
        elif any(word in req_text for word in ["monitor", "logging", "observability", "telemetry"]):
            service = services["monitoring"][0]
            additional = services["monitoring"][1:2]
            pattern = "Centralized Monitoring"
            assumptions = ["Monitoring requirements defined", "Alert thresholds configured"]
            notes = "Implement comprehensive monitoring and alerting"
            
        elif any(word in req_text for word in ["kubernetes", "k8s", "container orchestration"]):
            service = services["kubernetes"][0]
            additional = services["kubernetes"][1:]
            pattern = "Microservices on Kubernetes"
            assumptions = ["Container strategy defined", "DevOps processes in place"]
            notes = "Use managed Kubernetes for container orchestration"
            
        elif any(word in req_text for word in ["serverless", "function", "event-driven"]):
            service = services["serverless"][0]
            additional = services["serverless"][1:2]
            pattern = "Event-Driven Serverless"
            assumptions = ["Event sources identified", "Function boundaries defined"]
            notes = "Leverage serverless for event-driven workloads"
        
        mappings.append({
            "req_id": req_id,
            "requirement": req.get("text", "")[:100] + "...",  # Truncate for readability
            "cloud_service": service,
            "additional_services": additional,
            "architecture_pattern": pattern,
            "compliance_level": compliance,
            "assumptions": assumptions if assumptions else ["Standard implementation"],
            "implementation_notes": notes if notes else "Standard implementation using cloud best practices"
        })
    
    return mappings


def save_architecture_mappings(mappings: List[Dict[str, Any]], output_dir: str = "stage2_architecture"):
    """Save architecture mappings to JSON and CSV"""
    
    import csv
    from pathlib import Path
    
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    # Save JSON
    json_file = output_path / "architecture_mappings.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(mappings, f, indent=2, ensure_ascii=False)
    
    # Save CSV
    csv_file = output_path / "architecture_mappings.csv"
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        if mappings:
            fieldnames = [
                'req_id', 'requirement', 'cloud_service', 'additional_services',
                'architecture_pattern', 'compliance_level', 'assumptions', 'implementation_notes'
            ]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for mapping in mappings:
                # Convert lists to strings for CSV
                row = mapping.copy()
                row['additional_services'] = ', '.join(mapping.get('additional_services', []))
                row['assumptions'] = ', '.join(mapping.get('assumptions', []))
                writer.writerow(row)
    
    print(f"[OK] Architecture mappings saved to {output_dir}")
    return str(json_file), str(csv_file)
