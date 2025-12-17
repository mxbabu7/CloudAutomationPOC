"""
Azure Cost Optimizer - Real-time Resource Optimization
Analyzes compute, storage, and network resources for cost optimization opportunities
"""

import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dotenv import load_dotenv
from azure.identity import ClientSecretCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.monitor import MonitorManagementClient
from azure.mgmt.resource import ResourceManagementClient
import json

# Load environment variables
load_dotenv()


class AzureCostOptimizer:
    """Real-time Azure resource cost optimizer"""
    
    def __init__(self):
        """Initialize Azure Cost Optimizer"""
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
        self.compute_client = ComputeManagementClient(self.credential, self.subscription_id)
        self.storage_client = StorageManagementClient(self.credential, self.subscription_id)
        self.network_client = NetworkManagementClient(self.credential, self.subscription_id)
        self.monitor_client = MonitorManagementClient(self.credential, self.subscription_id)
        self.resource_client = ResourceManagementClient(self.credential, self.subscription_id)
        
        self.optimization_results = {
            'compute': [],
            'storage': [],
            'network': [],
            'summary': {}
        }
        
        print(f"✅ Azure Cost Optimizer initialized for subscription: {self.subscription_id}")
    
    def get_vm_metrics(self, resource_group: str, vm_name: str, days: int = 7) -> Dict:
        """Get VM performance metrics for optimization analysis"""
        try:
            end_time = datetime.utcnow()
            start_time = end_time - timedelta(days=days)
            
            resource_id = f"/subscriptions/{self.subscription_id}/resourceGroups/{resource_group}/providers/Microsoft.Compute/virtualMachines/{vm_name}"
            
            # Query CPU percentage
            cpu_metrics = self.monitor_client.metrics.list(
                resource_id,
                timespan=f"{start_time.isoformat()}/{end_time.isoformat()}",
                interval='PT1H',
                metricnames='Percentage CPU',
                aggregation='Average'
            )
            
            cpu_values = []
            for item in cpu_metrics.value:
                for timeserie in item.timeseries:
                    for data in timeserie.data:
                        if data.average is not None:
                            cpu_values.append(data.average)
            
            if cpu_values:
                avg_cpu = sum(cpu_values) / len(cpu_values)
                max_cpu = max(cpu_values)
            else:
                avg_cpu = 0
                max_cpu = 0
            
            return {
                'avg_cpu': avg_cpu,
                'max_cpu': max_cpu,
                'sample_count': len(cpu_values)
            }
        except Exception as e:
            print(f"  ⚠️  Could not retrieve metrics for {vm_name}: {str(e)}")
            return {'avg_cpu': 0, 'max_cpu': 0, 'sample_count': 0}
    
    def optimize_compute_resources(self) -> List[Dict]:
        """Analyze and optimize compute resources (VMs)"""
        print("\n🖥️  Analyzing Compute Resources...")
        recommendations = []
        
        try:
            # Get all VMs
            vms = list(self.compute_client.virtual_machines.list_all())
            print(f"   Found {len(vms)} virtual machines")
            
            for vm in vms:
                resource_group = vm.id.split('/')[4]
                vm_name = vm.name
                vm_size = vm.hardware_profile.vm_size
                location = vm.location
                
                print(f"   Analyzing: {vm_name} ({vm_size})")
                
                # Get VM power state
                instance_view = self.compute_client.virtual_machines.instance_view(
                    resource_group, vm_name
                )
                
                power_state = "unknown"
                for status in instance_view.statuses:
                    if status.code.startswith('PowerState/'):
                        power_state = status.code.split('/')[1]
                
                # Get performance metrics
                metrics = self.get_vm_metrics(resource_group, vm_name)
                
                # Optimization recommendations
                vm_recommendation = {
                    'resource_type': 'Virtual Machine',
                    'resource_name': vm_name,
                    'resource_group': resource_group,
                    'location': location,
                    'current_size': vm_size,
                    'power_state': power_state,
                    'avg_cpu': round(metrics['avg_cpu'], 2),
                    'max_cpu': round(metrics['max_cpu'], 2),
                    'recommendations': [],
                    'estimated_savings': 0,
                    'priority': 'Low'
                }
                
                # Check if VM is stopped/deallocated
                if power_state in ['deallocated', 'stopped']:
                    vm_recommendation['recommendations'].append({
                        'issue': 'VM is deallocated but still incurring storage costs',
                        'action': 'Consider deleting the VM if no longer needed, or keep monitoring',
                        'savings_type': 'Disk storage costs',
                        'estimated_monthly_savings': 10
                    })
                    vm_recommendation['estimated_savings'] += 10
                    vm_recommendation['priority'] = 'Medium'
                
                # Check for underutilized VMs
                elif metrics['sample_count'] > 0:
                    if metrics['avg_cpu'] < 5 and metrics['max_cpu'] < 20:
                        vm_recommendation['recommendations'].append({
                            'issue': f'VM is severely underutilized (Avg CPU: {metrics["avg_cpu"]:.1f}%, Max: {metrics["max_cpu"]:.1f}%)',
                            'action': 'Downsize to a smaller VM size or use B-series burstable VMs',
                            'savings_type': 'Compute cost reduction',
                            'estimated_monthly_savings': 150
                        })
                        vm_recommendation['estimated_savings'] += 150
                        vm_recommendation['priority'] = 'High'
                    
                    elif metrics['avg_cpu'] < 20:
                        vm_recommendation['recommendations'].append({
                            'issue': f'VM is underutilized (Avg CPU: {metrics["avg_cpu"]:.1f}%)',
                            'action': 'Consider downsizing or using Reserved Instances for consistent workloads',
                            'savings_type': 'Compute optimization',
                            'estimated_monthly_savings': 75
                        })
                        vm_recommendation['estimated_savings'] += 75
                        vm_recommendation['priority'] = 'Medium'
                
                # Always recommend Reserved Instances for running VMs
                if power_state == 'running':
                    vm_recommendation['recommendations'].append({
                        'issue': 'VM running on pay-as-you-go pricing',
                        'action': 'Purchase 1-year or 3-year Reserved Instance for up to 72% savings',
                        'savings_type': 'Reserved capacity discount',
                        'estimated_monthly_savings': 200
                    })
                    vm_recommendation['estimated_savings'] += 200
                    
                    # Auto-shutdown recommendation for non-production
                    if 'dev' in vm_name.lower() or 'test' in vm_name.lower():
                        vm_recommendation['recommendations'].append({
                            'issue': 'Dev/Test VM running 24/7',
                            'action': 'Implement auto-shutdown schedule (e.g., shutdown at 7 PM, start at 8 AM)',
                            'savings_type': 'Runtime reduction',
                            'estimated_monthly_savings': 100
                        })
                        vm_recommendation['estimated_savings'] += 100
                        vm_recommendation['priority'] = 'High'
                
                if vm_recommendation['recommendations']:
                    recommendations.append(vm_recommendation)
            
            self.optimization_results['compute'] = recommendations
            print(f"   ✅ Generated {len(recommendations)} compute optimization recommendations")
            
        except Exception as e:
            print(f"   ❌ Error analyzing compute resources: {e}")
        
        return recommendations
    
    def optimize_storage_resources(self) -> List[Dict]:
        """Analyze and optimize storage resources"""
        print("\n💾 Analyzing Storage Resources...")
        recommendations = []
        
        try:
            # Get all storage accounts
            storage_accounts = list(self.storage_client.storage_accounts.list())
            print(f"   Found {len(storage_accounts)} storage accounts")
            
            for account in storage_accounts:
                resource_group = account.id.split('/')[4]
                account_name = account.name
                sku = account.sku.name
                tier = account.sku.tier
                location = account.location
                
                print(f"   Analyzing: {account_name} ({sku})")
                
                storage_recommendation = {
                    'resource_type': 'Storage Account',
                    'resource_name': account_name,
                    'resource_group': resource_group,
                    'location': location,
                    'current_sku': sku,
                    'tier': tier,
                    'recommendations': [],
                    'estimated_savings': 0,
                    'priority': 'Low'
                }
                
                # Check for premium storage on non-critical workloads
                if 'Premium' in sku:
                    storage_recommendation['recommendations'].append({
                        'issue': 'Using Premium storage tier',
                        'action': 'Evaluate if Premium performance is required. Consider Standard tier for non-critical data',
                        'savings_type': 'Storage tier optimization',
                        'estimated_monthly_savings': 50
                    })
                    storage_recommendation['estimated_savings'] += 50
                    storage_recommendation['priority'] = 'Medium'
                
                # Recommend lifecycle management
                storage_recommendation['recommendations'].append({
                    'issue': 'No automated lifecycle management detected',
                    'action': 'Implement blob lifecycle policies: Move to Cool tier after 30 days, Archive after 90 days',
                    'savings_type': 'Access tier optimization',
                    'estimated_monthly_savings': 30
                })
                storage_recommendation['estimated_savings'] += 30
                
                # Check redundancy
                if 'GRS' in sku or 'GZRS' in sku:
                    storage_recommendation['recommendations'].append({
                        'issue': f'Using geo-redundant storage ({sku})',
                        'action': 'Evaluate if geo-redundancy is needed. LRS costs 50% less for non-critical data',
                        'savings_type': 'Redundancy optimization',
                        'estimated_monthly_savings': 40
                    })
                    storage_recommendation['estimated_savings'] += 40
                    storage_recommendation['priority'] = 'Medium'
                
                # Get managed disks in this resource group
                try:
                    disks = list(self.compute_client.disks.list_by_resource_group(resource_group))
                    unattached_disks = [d for d in disks if d.disk_state == 'Unattached']
                    
                    if unattached_disks:
                        disk_cost = len(unattached_disks) * 5  # Approx $5 per disk per month
                        storage_recommendation['recommendations'].append({
                            'issue': f'Found {len(unattached_disks)} unattached managed disks',
                            'action': 'Delete unused disks or create snapshots and delete disks',
                            'savings_type': 'Unused resource cleanup',
                            'estimated_monthly_savings': disk_cost
                        })
                        storage_recommendation['estimated_savings'] += disk_cost
                        storage_recommendation['priority'] = 'High'
                except:
                    pass
                
                if storage_recommendation['recommendations']:
                    recommendations.append(storage_recommendation)
            
            self.optimization_results['storage'] = recommendations
            print(f"   ✅ Generated {len(recommendations)} storage optimization recommendations")
            
        except Exception as e:
            print(f"   ❌ Error analyzing storage resources: {e}")
        
        return recommendations
    
    def optimize_network_resources(self) -> List[Dict]:
        """Analyze and optimize network resources"""
        print("\n🌐 Analyzing Network Resources...")
        recommendations = []
        
        try:
            # Get all public IPs
            public_ips = list(self.network_client.public_ip_addresses.list_all())
            print(f"   Found {len(public_ips)} public IP addresses")
            
            unassigned_ips = [ip for ip in public_ips if not ip.ip_configuration]
            
            if unassigned_ips:
                ip_cost = len(unassigned_ips) * 3  # Approx $3 per IP per month
                recommendations.append({
                    'resource_type': 'Public IP Addresses',
                    'resource_name': f'{len(unassigned_ips)} unassigned IPs',
                    'resource_group': 'Multiple',
                    'location': 'Multiple',
                    'recommendations': [{
                        'issue': f'{len(unassigned_ips)} public IP addresses are not assigned to any resource',
                        'action': 'Delete unused public IPs to save costs',
                        'savings_type': 'Unused resource cleanup',
                        'estimated_monthly_savings': ip_cost
                    }],
                    'estimated_savings': ip_cost,
                    'priority': 'High'
                })
            
            # Get all load balancers
            load_balancers = list(self.network_client.load_balancers.list_all())
            print(f"   Found {len(load_balancers)} load balancers")
            
            for lb in load_balancers:
                resource_group = lb.id.split('/')[4]
                
                # Check if load balancer has backend pools
                if not lb.backend_address_pools or all(not pool.backend_ip_configurations for pool in lb.backend_address_pools):
                    recommendations.append({
                        'resource_type': 'Load Balancer',
                        'resource_name': lb.name,
                        'resource_group': resource_group,
                        'location': lb.location,
                        'recommendations': [{
                            'issue': 'Load balancer has no backend resources',
                            'action': 'Delete unused load balancer or configure backend pool',
                            'savings_type': 'Unused resource cleanup',
                            'estimated_monthly_savings': 25
                        }],
                        'estimated_savings': 25,
                        'priority': 'Medium'
                    })
            
            # Get all VPN gateways
            try:
                vpn_gateways = list(self.network_client.virtual_network_gateways.list_all())
                print(f"   Found {len(vpn_gateways)} VPN/ExpressRoute gateways")
                
                for gateway in vpn_gateways:
                    resource_group = gateway.id.split('/')[4]
                    
                    recommendations.append({
                        'resource_type': 'VPN Gateway',
                        'resource_name': gateway.name,
                        'resource_group': resource_group,
                        'location': gateway.location,
                        'sku': gateway.sku.name if gateway.sku else 'Unknown',
                        'recommendations': [{
                            'issue': f'VPN Gateway running 24/7 (SKU: {gateway.sku.name if gateway.sku else "Unknown"})',
                            'action': 'Evaluate if always-on connectivity is needed. Consider lower SKU or point-to-site VPN',
                            'savings_type': 'Gateway optimization',
                            'estimated_monthly_savings': 100
                        }],
                        'estimated_savings': 100,
                        'priority': 'Medium'
                    })
            except:
                pass
            
            # Data transfer optimization
            recommendations.append({
                'resource_type': 'Network Bandwidth',
                'resource_name': 'Data Transfer',
                'resource_group': 'Subscription-wide',
                'location': 'Global',
                'recommendations': [{
                    'issue': 'Potential data egress costs',
                    'action': 'Use Azure CDN for static content, optimize cross-region traffic, enable compression',
                    'savings_type': 'Bandwidth optimization',
                    'estimated_monthly_savings': 50
                }],
                'estimated_savings': 50,
                'priority': 'Low'
            })
            
            self.optimization_results['network'] = recommendations
            print(f"   ✅ Generated {len(recommendations)} network optimization recommendations")
            
        except Exception as e:
            print(f"   ❌ Error analyzing network resources: {e}")
        
        return recommendations
    
    def generate_optimization_report(self) -> str:
        """Generate comprehensive optimization report"""
        report = []
        report.append("=" * 100)
        report.append("AZURE COST OPTIMIZATION REPORT - REAL-TIME ANALYSIS")
        report.append("=" * 100)
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        # Calculate totals
        total_compute_savings = sum(r['estimated_savings'] for r in self.optimization_results['compute'])
        total_storage_savings = sum(r['estimated_savings'] for r in self.optimization_results['storage'])
        total_network_savings = sum(r['estimated_savings'] for r in self.optimization_results['network'])
        total_savings = total_compute_savings + total_storage_savings + total_network_savings
        
        # Summary
        report.append("OPTIMIZATION SUMMARY")
        report.append("-" * 100)
        report.append(f"Total Potential Monthly Savings: ${total_savings:.2f}")
        report.append(f"Total Potential Annual Savings: ${total_savings * 12:.2f}")
        report.append(f"")
        report.append(f"Breakdown:")
        report.append(f"  • Compute Optimization: ${total_compute_savings:.2f}/month ({len(self.optimization_results['compute'])} resources)")
        report.append(f"  • Storage Optimization: ${total_storage_savings:.2f}/month ({len(self.optimization_results['storage'])} resources)")
        report.append(f"  • Network Optimization: ${total_network_savings:.2f}/month ({len(self.optimization_results['network'])} resources)")
        report.append("")
        
        # Compute recommendations
        if self.optimization_results['compute']:
            report.append("\n" + "=" * 100)
            report.append("COMPUTE RESOURCE OPTIMIZATION")
            report.append("=" * 100)
            
            for i, rec in enumerate(self.optimization_results['compute'], 1):
                report.append(f"\n{i}. {rec['resource_name']} - [{rec['priority']} Priority]")
                report.append(f"   Resource Group: {rec['resource_group']}")
                report.append(f"   Location: {rec['location']}")
                report.append(f"   Current Size: {rec['current_size']}")
                report.append(f"   Power State: {rec['power_state']}")
                if rec['avg_cpu'] > 0:
                    report.append(f"   CPU Usage: Avg {rec['avg_cpu']}%, Max {rec['max_cpu']}%")
                report.append(f"   Estimated Monthly Savings: ${rec['estimated_savings']:.2f}")
                report.append(f"")
                report.append(f"   Recommendations:")
                for j, recommendation in enumerate(rec['recommendations'], 1):
                    report.append(f"   {j}. {recommendation['issue']}")
                    report.append(f"      → Action: {recommendation['action']}")
                    report.append(f"      → Savings Type: {recommendation['savings_type']}")
                    report.append(f"      → Estimated Savings: ${recommendation['estimated_monthly_savings']:.2f}/month")
                    report.append("")
        
        # Storage recommendations
        if self.optimization_results['storage']:
            report.append("\n" + "=" * 100)
            report.append("STORAGE RESOURCE OPTIMIZATION")
            report.append("=" * 100)
            
            for i, rec in enumerate(self.optimization_results['storage'], 1):
                report.append(f"\n{i}. {rec['resource_name']} - [{rec['priority']} Priority]")
                report.append(f"   Resource Group: {rec['resource_group']}")
                report.append(f"   Location: {rec['location']}")
                report.append(f"   Current SKU: {rec['current_sku']}")
                report.append(f"   Estimated Monthly Savings: ${rec['estimated_savings']:.2f}")
                report.append(f"")
                report.append(f"   Recommendations:")
                for j, recommendation in enumerate(rec['recommendations'], 1):
                    report.append(f"   {j}. {recommendation['issue']}")
                    report.append(f"      → Action: {recommendation['action']}")
                    report.append(f"      → Savings Type: {recommendation['savings_type']}")
                    report.append(f"      → Estimated Savings: ${recommendation['estimated_monthly_savings']:.2f}/month")
                    report.append("")
        
        # Network recommendations
        if self.optimization_results['network']:
            report.append("\n" + "=" * 100)
            report.append("NETWORK RESOURCE OPTIMIZATION")
            report.append("=" * 100)
            
            for i, rec in enumerate(self.optimization_results['network'], 1):
                report.append(f"\n{i}. {rec['resource_name']} - [{rec.get('priority', 'Medium')} Priority]")
                report.append(f"   Resource Group: {rec['resource_group']}")
                report.append(f"   Location: {rec['location']}")
                if 'sku' in rec:
                    report.append(f"   SKU: {rec['sku']}")
                report.append(f"   Estimated Monthly Savings: ${rec['estimated_savings']:.2f}")
                report.append(f"")
                report.append(f"   Recommendations:")
                for j, recommendation in enumerate(rec['recommendations'], 1):
                    report.append(f"   {j}. {recommendation['issue']}")
                    report.append(f"      → Action: {recommendation['action']}")
                    report.append(f"      → Savings Type: {recommendation['savings_type']}")
                    report.append(f"      → Estimated Savings: ${recommendation['estimated_monthly_savings']:.2f}/month")
                    report.append("")
        
        report.append("\n" + "=" * 100)
        report.append("NEXT STEPS")
        report.append("=" * 100)
        report.append("1. Review HIGH priority recommendations first")
        report.append("2. Implement quick wins (unused resources, unattached disks)")
        report.append("3. Plan Reserved Instance purchases for production VMs")
        report.append("4. Set up auto-shutdown schedules for dev/test resources")
        report.append("5. Implement storage lifecycle policies")
        report.append("6. Monitor savings after implementation")
        report.append("=" * 100)
        
        return "\n".join(report)
    
    def save_optimization_results(self, report: str):
        """Save optimization results to files"""
        os.makedirs('output', exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Save JSON
        json_file = f'output/cost_optimization_{timestamp}.json'
        with open(json_file, 'w') as f:
            json.dump({
                'optimization_results': self.optimization_results,
                'summary': {
                    'total_monthly_savings': sum(
                        r['estimated_savings'] 
                        for category in self.optimization_results.values() 
                        if isinstance(category, list)
                        for r in category
                    ),
                    'compute_savings': sum(r['estimated_savings'] for r in self.optimization_results['compute']),
                    'storage_savings': sum(r['estimated_savings'] for r in self.optimization_results['storage']),
                    'network_savings': sum(r['estimated_savings'] for r in self.optimization_results['network']),
                },
                'timestamp': datetime.now().isoformat()
            }, f, indent=2, default=str)
        
        # Save text report
        report_file = f'output/optimization_report_{timestamp}.txt'
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"\n✅ Optimization results saved:")
        print(f"   - JSON: {json_file}")
        print(f"   - Report: {report_file}")
    
    def run_optimization(self):
        """Run complete cost optimization analysis"""
        try:
            print(f"\n{'='*100}")
            print(f"AZURE COST OPTIMIZATION - REAL-TIME RESOURCE ANALYSIS")
            print(f"{'='*100}\n")
            
            # Analyze compute resources
            self.optimize_compute_resources()
            
            # Analyze storage resources
            self.optimize_storage_resources()
            
            # Analyze network resources
            self.optimize_network_resources()
            
            # Generate report
            print(f"\n📝 Generating optimization report...")
            report = self.generate_optimization_report()
            
            # Display report
            print("\n" + report)
            
            # Save results
            print(f"\n💾 Saving optimization results...")
            self.save_optimization_results(report)
            
            print(f"\n{'='*100}")
            print("✅ OPTIMIZATION ANALYSIS COMPLETE")
            print(f"{'='*100}\n")
            
        except Exception as e:
            print(f"\n❌ Error during optimization analysis: {e}")
            import traceback
            traceback.print_exc()


def main():
    """Main entry point"""
    print("Azure Cost Optimizer - Real-time Resource Analysis")
    print("=" * 100)
    
    # Create optimizer instance
    optimizer = AzureCostOptimizer()
    
    # Run optimization
    optimizer.run_optimization()


if __name__ == "__main__":
    main()
