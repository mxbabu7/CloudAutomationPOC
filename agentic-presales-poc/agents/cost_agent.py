"""
Cost Agent
Generates cloud cost estimates based on mapped architecture
"""


class CostAgent:
    def __init__(self):
        # Simple pricing models (placeholder values)
        self.pricing = {
            "Azure": {
                "Azure Virtual Machines": 100,
                "Azure Kubernetes Service (AKS)": 150,
                "Azure Functions": 50,
                "Azure Blob Storage": 20,
                "Azure SQL Database": 200,
                "Azure Cosmos DB": 100,
                "Azure VNet": 10,
                "Azure Load Balancer": 25,
                "Azure CDN": 30,
                "Azure API Management": 75,
                "Azure Service Bus": 15,
                "Azure Active Directory": 5,
                "Azure Monitor": 40,
                "Azure Security Center": 50,
                "Generic Service": 50
            },
            "AWS": {
                "EC2": 95,
                "Amazon EKS": 145,
                "AWS Lambda": 45,
                "S3": 18,
                "Amazon RDS": 190,
                "DynamoDB": 95,
                "VPC": 8,
                "Elastic Load Balancing": 23,
                "CloudFront": 28,
                "Amazon API Gateway": 70,
                "Amazon SQS": 12,
                "AWS IAM": 0,
                "CloudWatch": 38,
                "AWS Security Hub": 48,
                "Generic Service": 50
            },
            "GCP": {
                "Google Compute Engine": 90,
                "Google Kubernetes Engine (GKE)": 140,
                "Cloud Functions": 43,
                "Cloud Storage": 17,
                "Cloud SQL": 185,
                "Firestore": 90,
                "VPC": 7,
                "Cloud Load Balancing": 22,
                "Cloud CDN": 27,
                "API Gateway": 68,
                "Cloud Pub/Sub": 11,
                "Cloud IAM": 0,
                "Cloud Monitoring": 36,
                "Security Command Center": 45,
                "Generic Service": 50
            }
        }
    
    def run(self, cloud_mapping: dict) -> dict:
        """
        Generates cost estimates based on cloud mapping
        
        Args:
            cloud_mapping: Cloud-specific architecture mapping
            
        Returns:
            Detailed cost estimate
        """
        target_cloud = cloud_mapping["target_cloud"]
        cloud_pricing = self.pricing.get(target_cloud, {})
        
        components = []
        total_monthly = 0
        
        for layer in cloud_mapping.get("mapped_layers", []):
            for component in layer.get("components", []):
                service_name = component["cloud_service"]
                monthly_cost = cloud_pricing.get(service_name, 50)
                annual_cost = monthly_cost * 12
                
                components.append({
                    "service_name": service_name,
                    "service_type": component["logical_name"],
                    "monthly_cost": monthly_cost,
                    "annual_cost": annual_cost,
                    "notes": f"Deployed in {layer['layer_name']}"
                })
                
                total_monthly += monthly_cost
        
        total_annual = total_monthly * 12
        
        return {
            "cloud_provider": target_cloud,
            "components": components,
            "summary": {
                "total_monthly": total_monthly,
                "total_annual": total_annual,
                "currency": "USD"
            },
            "assumptions": [
                "Based on standard tier pricing",
                "Includes basic support plan",
                "Assumes moderate usage patterns",
                "Does not include data transfer costs",
                "Reserved instances not considered"
            ]
        }
