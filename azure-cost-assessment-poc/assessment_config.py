"""
Azure Cost Assessment - Configuration and Options
Centralized configuration for cost assessment tool
"""


def get_config():
    """
    Get configuration settings for cost assessment
    
    You can modify these settings to customize the assessment behavior
    """
    return {
        # Analysis settings
        'analysis': {
            'default_days': 30,          # Default number of days to analyze
            'max_days': 365,             # Maximum days allowed
            'currency': 'USD',           # Currency for reporting
            'granularity': 'Daily',      # Daily or Monthly
        },
        
        # Cost breakdown options
        'breakdown': {
            'by_resource_group': True,   # Break down by resource group
            'by_service': True,          # Break down by Azure service
            'by_location': False,        # Break down by region (optional)
            'by_tags': False,            # Break down by tags (optional)
            'top_n_resources': 10,       # Show top N items in each category
        },
        
        # Optimization thresholds
        'optimization': {
            'enabled': True,
            'thresholds': {
                'vm_high_cost_percentage': 30,     # Alert if VMs > 30% of total
                'storage_high_cost_percentage': 20, # Alert if storage > 20%
                'database_high_cost_percentage': 15,# Alert if DB > 15%
                'minimum_cost_for_recommendations': 100,  # Don't recommend if total < $100
            }
        },
        
        # Report settings
        'reports': {
            'output_dir': './output',
            'formats': ['txt', 'json'],   # Available: txt, json, csv
            'include_charts': False,       # Set to True if you add charting
            'include_recommendations': True,
        },
        
        # Display options
        'display': {
            'show_zero_costs': False,     # Hide items with $0 cost
            'decimal_places': 2,          # Decimal places for currency
            'percentage_threshold': 1.0,  # Hide items < 1% of total
        }
    }


def get_optimization_rules():
    """
    Define optimization rules and savings estimates
    
    These are used to generate recommendations based on service costs
    """
    return {
        'compute': {
            'keywords': ['virtual machine', 'compute', 'vm', 'app service'],
            'high_percentage_threshold': 30,
            'medium_percentage_threshold': 15,
            'recommendations': {
                'high': {
                    'priority': 'High',
                    'savings_estimate': 0.30,  # 30% potential savings
                    'actions': [
                        'Review VM utilization metrics (CPU, Memory)',
                        'Downsize underutilized VMs',
                        'Purchase Reserved Instances (up to 72% savings)',
                        'Use Azure Hybrid Benefit for Windows licenses',
                        'Consider Spot VMs for non-critical workloads',
                        'Implement auto-shutdown for dev/test VMs'
                    ]
                },
                'medium': {
                    'priority': 'Medium',
                    'savings_estimate': 0.15,
                    'actions': [
                        'Implement auto-shutdown schedules',
                        'Review and rightsize based on metrics',
                        'Enable Azure Advisor recommendations'
                    ]
                }
            }
        },
        
        'storage': {
            'keywords': ['storage', 'blob', 'disk', 'file'],
            'high_percentage_threshold': 20,
            'medium_percentage_threshold': 10,
            'recommendations': {
                'high': {
                    'priority': 'Medium',
                    'savings_estimate': 0.20,
                    'actions': [
                        'Move infrequently accessed data to Cool/Archive tier',
                        'Implement lifecycle management policies',
                        'Delete unused snapshots and orphaned disks',
                        'Review blob storage access patterns',
                        'Enable soft delete with appropriate retention'
                    ]
                },
                'medium': {
                    'priority': 'Low',
                    'savings_estimate': 0.10,
                    'actions': [
                        'Review storage account redundancy settings',
                        'Clean up old snapshots',
                        'Optimize blob access tiers'
                    ]
                }
            }
        },
        
        'database': {
            'keywords': ['database', 'sql', 'cosmos', 'postgresql', 'mysql'],
            'high_percentage_threshold': 15,
            'medium_percentage_threshold': 8,
            'recommendations': {
                'high': {
                    'priority': 'Medium',
                    'savings_estimate': 0.25,
                    'actions': [
                        'Review database DTU/vCore utilization',
                        'Consider serverless tier for dev/test workloads',
                        'Implement auto-pause for inactive databases',
                        'Use Reserved Capacity for production (up to 80% savings)',
                        'Optimize database tier based on actual usage'
                    ]
                },
                'medium': {
                    'priority': 'Low',
                    'savings_estimate': 0.15,
                    'actions': [
                        'Review backup retention policies',
                        'Consider read replicas placement',
                        'Optimize query performance'
                    ]
                }
            }
        },
        
        'networking': {
            'keywords': ['bandwidth', 'network', 'vpn', 'expressroute', 'load balancer'],
            'high_percentage_threshold': 10,
            'recommendations': {
                'high': {
                    'priority': 'Low',
                    'savings_estimate': 0.10,
                    'actions': [
                        'Review data transfer patterns',
                        'Optimize data egress',
                        'Use CDN for static content',
                        'Review unnecessary load balancers'
                    ]
                }
            }
        }
    }


def get_alert_thresholds():
    """Define alert thresholds for cost anomalies"""
    return {
        'daily_increase_percentage': 50,   # Alert if daily cost increases >50%
        'weekly_increase_percentage': 30,   # Alert if weekly cost increases >30%
        'total_cost_warning': 1000,        # Warning if total cost > $1000
        'total_cost_critical': 5000,       # Critical if total cost > $5000
    }


def get_service_categories():
    """Map Azure services to categories for better reporting"""
    return {
        'Compute': [
            'virtual machines', 'app service', 'functions', 'container instances',
            'kubernetes service', 'batch', 'service fabric'
        ],
        'Storage': [
            'storage', 'blob storage', 'disk storage', 'file storage',
            'data lake storage', 'backup'
        ],
        'Database': [
            'sql database', 'cosmos db', 'database for postgresql',
            'database for mysql', 'synapse analytics', 'cache for redis'
        ],
        'Networking': [
            'bandwidth', 'vpn gateway', 'application gateway', 'load balancer',
            'traffic manager', 'expressroute', 'cdn', 'firewall'
        ],
        'AI & ML': [
            'cognitive services', 'machine learning', 'bot service',
            'databricks', 'ai services'
        ],
        'Security': [
            'security center', 'key vault', 'sentinel', 'ddos protection',
            'private link'
        ],
        'Management': [
            'monitor', 'log analytics', 'automation', 'advisor',
            'cost management'
        ]
    }


# Example: Custom configuration for different scenarios
def get_dev_test_config():
    """Configuration optimized for dev/test environments"""
    config = get_config()
    config['optimization']['thresholds']['vm_high_cost_percentage'] = 20
    config['analysis']['default_days'] = 7
    return config


def get_production_config():
    """Configuration optimized for production environments"""
    config = get_config()
    config['analysis']['default_days'] = 90
    config['optimization']['thresholds']['minimum_cost_for_recommendations'] = 500
    return config


def get_quick_scan_config():
    """Configuration for quick cost scans"""
    config = get_config()
    config['analysis']['default_days'] = 7
    config['breakdown']['by_location'] = False
    config['breakdown']['by_tags'] = False
    config['breakdown']['top_n_resources'] = 5
    return config


if __name__ == "__main__":
    """Test configuration loading"""
    import json
    
    print("Default Configuration:")
    print(json.dumps(get_config(), indent=2))
    
    print("\n\nOptimization Rules:")
    print(json.dumps(get_optimization_rules(), indent=2))
    
    print("\n\nService Categories:")
    print(json.dumps(get_service_categories(), indent=2))
