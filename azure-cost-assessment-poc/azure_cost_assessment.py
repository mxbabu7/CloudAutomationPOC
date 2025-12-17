"""
Azure Cost Assessment - Simplified Single File
Performs Azure cost analysis, optimization recommendations, and reporting
"""

import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dotenv import load_dotenv
from azure.identity import ClientSecretCredential
from azure.mgmt.costmanagement import CostManagementClient
from azure.mgmt.resource import SubscriptionClient
import json

# Load environment variables
load_dotenv()


class AzureCostAssessment:
    """Single class to handle all Azure cost assessment operations"""
    
    def __init__(self, config: Dict):
        """Initialize with configuration from config file"""
        self.config = config
        
        # Get Azure credentials
        self.subscription_id = os.getenv('AZURE_SUBSCRIPTION_ID')
        tenant_id = os.getenv('AZURE_TENANT_ID')
        client_id = os.getenv('AZURE_CLIENT_ID')
        client_secret = os.getenv('AZURE_CLIENT_SECRET')
        
        if not all([self.subscription_id, tenant_id, client_id, client_secret]):
            raise ValueError("Missing Azure credentials. Check your .env file")
        
        # Authenticate
        self.credential = ClientSecretCredential(
            tenant_id=tenant_id,
            client_id=client_id,
            client_secret=client_secret
        )
        
        # Initialize clients
        self.cost_client = CostManagementClient(self.credential)
        self.subscription_client = SubscriptionClient(self.credential)
        
        print(f"✅ Authenticated to Azure subscription: {self.subscription_id}")
    
    def get_subscription_info(self) -> Dict:
        """Get subscription details"""
        try:
            subscription = self.subscription_client.subscriptions.get(self.subscription_id)
            return {
                'subscription_id': subscription.subscription_id,
                'display_name': subscription.display_name,
                'state': subscription.state
            }
        except Exception as e:
            print(f"❌ Error retrieving subscription info: {e}")
            return {}
    
    def get_cost_data(self, days: int = 30) -> List[Dict]:
        """Retrieve cost data for specified number of days"""
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            scope = f"/subscriptions/{self.subscription_id}"
            
            # Build query
            query_definition = {
                "type": "ActualCost",
                "timeframe": "Custom",
                "time_period": {
                    "from": start_date.strftime("%Y-%m-%dT00:00:00Z"),
                    "to": end_date.strftime("%Y-%m-%dT23:59:59Z")
                },
                "dataset": {
                    "granularity": "Daily",
                    "aggregation": {
                        "totalCost": {
                            "name": "Cost",
                            "function": "Sum"
                        }
                    },
                    "grouping": [
                        {
                            "type": "Dimension",
                            "name": "ServiceName"
                        },
                        {
                            "type": "Dimension",
                            "name": "ResourceGroupName"
                        }
                    ]
                }
            }
            
            print(f"📊 Fetching cost data for last {days} days...")
            result = self.cost_client.query.usage(scope=scope, parameters=query_definition)
            
            # Parse results
            cost_data = []
            if hasattr(result, 'rows') and result.rows:
                columns = [col.name for col in result.columns]
                for row in result.rows:
                    record = dict(zip(columns, row))
                    cost_data.append(record)
            
            print(f"✅ Retrieved {len(cost_data)} cost records")
            return cost_data
            
        except Exception as e:
            print(f"❌ Error retrieving cost data: {e}")
            return []
    
    def analyze_costs(self, cost_data: List[Dict]) -> Dict:
        """Analyze cost data and generate insights"""
        if not cost_data:
            return {
                'total_cost': 0,
                'daily_average': 0,
                'by_service': [],
                'by_resource_group': [],
                'summary': 'No cost data available'
            }
        
        # Calculate totals
        total_cost = sum(float(record.get('Cost', 0)) for record in cost_data)
        
        # Group by service
        services = {}
        for record in cost_data:
            service = record.get('ServiceName', 'Unknown')
            cost = float(record.get('Cost', 0))
            services[service] = services.get(service, 0) + cost
        
        # Group by resource group
        resource_groups = {}
        for record in cost_data:
            rg = record.get('ResourceGroupName', 'Unknown')
            cost = float(record.get('Cost', 0))
            resource_groups[rg] = resource_groups.get(rg, 0) + cost
        
        # Sort and get top items
        top_services = sorted(
            [{'name': k, 'cost': v, 'percentage': (v/total_cost*100) if total_cost > 0 else 0} 
             for k, v in services.items()],
            key=lambda x: x['cost'],
            reverse=True
        )[:10]
        
        top_rgs = sorted(
            [{'name': k, 'cost': v, 'percentage': (v/total_cost*100) if total_cost > 0 else 0} 
             for k, v in resource_groups.items()],
            key=lambda x: x['cost'],
            reverse=True
        )[:10]
        
        # Calculate daily average
        unique_dates = set(record.get('UsageDate', '') for record in cost_data if record.get('UsageDate'))
        daily_average = total_cost / len(unique_dates) if unique_dates else total_cost / 30
        
        return {
            'total_cost': total_cost,
            'daily_average': daily_average,
            'by_service': top_services,
            'by_resource_group': top_rgs,
            'summary': f'Total cost: ${total_cost:.2f} over {len(unique_dates)} days'
        }
    
    def generate_recommendations(self, analysis: Dict) -> List[Dict]:
        """Generate cost optimization recommendations"""
        recommendations = []
        total_cost = analysis.get('total_cost', 0)
        services = analysis.get('by_service', [])
        
        if total_cost == 0:
            return [{
                'priority': 'Info',
                'category': 'General',
                'recommendation': 'No significant costs detected in the analysis period'
            }]
        
        # Check for high-cost services
        for service in services:
            service_name = service['name']
            cost = service['cost']
            percentage = service['percentage']
            
            # Virtual Machines / Compute
            if any(keyword in service_name.lower() for keyword in ['virtual machine', 'compute', 'vm']):
                if percentage > 30:
                    recommendations.append({
                        'priority': 'High',
                        'category': 'Compute',
                        'service': service_name,
                        'current_cost': f"${cost:.2f}",
                        'percentage': f"{percentage:.1f}%",
                        'recommendation': 'Consider rightsizing VMs or using Reserved Instances',
                        'actions': [
                            'Review VM utilization metrics',
                            'Downsize underutilized VMs',
                            'Purchase Reserved Instances (up to 72% savings)',
                            'Use Azure Hybrid Benefit for Windows licenses',
                            'Implement auto-shutdown for dev/test VMs'
                        ],
                        'estimated_savings': f"${cost * 0.30:.2f} (30%)"
                    })
            
            # Storage
            elif any(keyword in service_name.lower() for keyword in ['storage', 'blob', 'disk']):
                if percentage > 20:
                    recommendations.append({
                        'priority': 'Medium',
                        'category': 'Storage',
                        'service': service_name,
                        'current_cost': f"${cost:.2f}",
                        'percentage': f"{percentage:.1f}%",
                        'recommendation': 'Optimize storage tiers and lifecycle policies',
                        'actions': [
                            'Move infrequently accessed data to Cool/Archive tier',
                            'Implement lifecycle management policies',
                            'Delete unused snapshots and disks',
                            'Review blob storage access patterns'
                        ],
                        'estimated_savings': f"${cost * 0.20:.2f} (20%)"
                    })
            
            # Database
            elif any(keyword in service_name.lower() for keyword in ['database', 'sql', 'cosmos']):
                if percentage > 15:
                    recommendations.append({
                        'priority': 'Medium',
                        'category': 'Database',
                        'service': service_name,
                        'current_cost': f"${cost:.2f}",
                        'percentage': f"{percentage:.1f}%",
                        'recommendation': 'Optimize database tier and configuration',
                        'actions': [
                            'Review database DTU/vCore utilization',
                            'Consider serverless tier for dev/test',
                            'Implement auto-pause for inactive databases',
                            'Use Reserved Capacity for production'
                        ],
                        'estimated_savings': f"${cost * 0.25:.2f} (25%)"
                    })
        
        # General recommendations
        if total_cost > 1000:
            recommendations.append({
                'priority': 'High',
                'category': 'General',
                'recommendation': 'Implement cost management best practices',
                'actions': [
                    'Set up Azure Budgets and Alerts',
                    'Tag all resources for better cost tracking',
                    'Enable Azure Advisor recommendations',
                    'Review and remove unused resources regularly',
                    'Implement resource locks on critical resources'
                ],
                'estimated_savings': 'Ongoing monitoring and optimization'
            })
        
        if not recommendations:
            recommendations.append({
                'priority': 'Low',
                'category': 'General',
                'recommendation': 'Continue monitoring costs and follow Azure best practices'
            })
        
        return recommendations
    
    def generate_report(self, analysis: Dict, recommendations: List[Dict]) -> str:
        """Generate text report"""
        report = []
        report.append("=" * 80)
        report.append("AZURE COST ASSESSMENT REPORT")
        report.append("=" * 80)
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        # Summary
        report.append("COST SUMMARY")
        report.append("-" * 80)
        report.append(f"Total Cost: ${analysis['total_cost']:.2f}")
        report.append(f"Daily Average: ${analysis['daily_average']:.2f}")
        report.append(f"Summary: {analysis['summary']}\n")
        
        # Top services
        report.append("TOP SERVICES BY COST")
        report.append("-" * 80)
        for i, service in enumerate(analysis['by_service'][:10], 1):
            report.append(f"{i}. {service['name']}: ${service['cost']:.2f} ({service['percentage']:.1f}%)")
        report.append("")
        
        # Top resource groups
        report.append("TOP RESOURCE GROUPS BY COST")
        report.append("-" * 80)
        for i, rg in enumerate(analysis['by_resource_group'][:10], 1):
            report.append(f"{i}. {rg['name']}: ${rg['cost']:.2f} ({rg['percentage']:.1f}%)")
        report.append("")
        
        # Recommendations
        report.append("COST OPTIMIZATION RECOMMENDATIONS")
        report.append("-" * 80)
        for i, rec in enumerate(recommendations, 1):
            report.append(f"\n{i}. [{rec['priority']}] {rec.get('category', 'General')}")
            report.append(f"   Recommendation: {rec['recommendation']}")
            
            if 'service' in rec:
                report.append(f"   Service: {rec['service']}")
                report.append(f"   Current Cost: {rec['current_cost']} ({rec['percentage']})")
            
            if 'actions' in rec:
                report.append(f"   Actions:")
                for action in rec['actions']:
                    report.append(f"   - {action}")
            
            if 'estimated_savings' in rec:
                report.append(f"   Estimated Savings: {rec['estimated_savings']}")
        
        report.append("\n" + "=" * 80)
        
        return "\n".join(report)
    
    def save_results(self, analysis: Dict, recommendations: List[Dict], report: str):
        """Save results to files"""
        os.makedirs('output', exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Save JSON
        json_file = f'output/cost_assessment_{timestamp}.json'
        with open(json_file, 'w') as f:
            json.dump({
                'analysis': analysis,
                'recommendations': recommendations,
                'timestamp': datetime.now().isoformat()
            }, f, indent=2, default=str)
        
        # Save text report
        report_file = f'output/cost_report_{timestamp}.txt'
        with open(report_file, 'w') as f:
            f.write(report)
        
        print(f"\n✅ Results saved:")
        print(f"   - JSON: {json_file}")
        print(f"   - Report: {report_file}")
    
    def run_assessment(self, days: int = None):
        """Run complete cost assessment"""
        try:
            # Use config default if days not specified
            if days is None:
                days = self.config.get('analysis', {}).get('default_days', 30)
            
            print(f"\n{'='*80}")
            print(f"AZURE COST ASSESSMENT - {days} Day Analysis")
            print(f"{'='*80}\n")
            
            # Step 1: Get subscription info
            print("📋 Step 1: Retrieving subscription information...")
            sub_info = self.get_subscription_info()
            if sub_info:
                print(f"   Subscription: {sub_info.get('display_name', 'Unknown')}")
                print(f"   State: {sub_info.get('state', 'Unknown')}")
            
            # Step 2: Get cost data
            print(f"\n📊 Step 2: Collecting cost data...")
            cost_data = self.get_cost_data(days)
            
            if not cost_data:
                print("⚠️  No cost data retrieved. Check permissions.")
                return
            
            # Step 3: Analyze costs
            print(f"\n🔍 Step 3: Analyzing costs...")
            analysis = self.analyze_costs(cost_data)
            
            # Step 4: Generate recommendations
            print(f"\n💡 Step 4: Generating optimization recommendations...")
            recommendations = self.generate_recommendations(analysis)
            print(f"   Generated {len(recommendations)} recommendations")
            
            # Step 5: Generate report
            print(f"\n📝 Step 5: Creating report...")
            report = self.generate_report(analysis, recommendations)
            
            # Display report
            print("\n" + report)
            
            # Step 6: Save results
            print(f"\n💾 Step 6: Saving results...")
            self.save_results(analysis, recommendations, report)
            
            print(f"\n{'='*80}")
            print("✅ ASSESSMENT COMPLETE")
            print(f"{'='*80}\n")
            
        except Exception as e:
            print(f"\n❌ Error during assessment: {e}")
            import traceback
            traceback.print_exc()


def main():
    """Main entry point"""
    # Import config
    from assessment_config import get_config
    
    config = get_config()
    
    print("Azure Cost Assessment Tool")
    print("=" * 80)
    
    # Create assessment instance
    assessment = AzureCostAssessment(config)
    
    # Run assessment with default settings
    assessment.run_assessment()


if __name__ == "__main__":
    main()
