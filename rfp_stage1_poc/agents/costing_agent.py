"""
Stage 4: Cost Estimation Agent
Estimates cloud infrastructure costs based on architecture mappings
"""

import json
import os
from typing import List, Dict, Any, Optional
from pathlib import Path


def estimate_costs(
    architecture_mappings: List[Dict[str, Any]],
    cloud_provider: str = "azure",
    scale: str = "medium",
    llm_client: Optional[Any] = None,
    output_dir: str = "stage4_costing"
) -> Dict[str, Any]:
    """
    Estimate monthly cloud costs
    
    Args:
        architecture_mappings: Architecture mappings from Stage 2
        cloud_provider: Target cloud provider
        scale: Deployment scale (small, medium, large, enterprise)
        llm_client: Optional LLM client for intelligent cost estimation
        output_dir: Output directory for cost reports
        
    Returns:
        Dictionary with cost breakdown and estimates
    """
    
    if llm_client:
        cost_estimate = _estimate_with_llm(architecture_mappings, cloud_provider, scale, llm_client)
    else:
        cost_estimate = _estimate_with_rules(architecture_mappings, cloud_provider, scale)
    
    # Save cost estimate
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    _save_cost_estimate(cost_estimate, output_path)
    
    return cost_estimate


def _estimate_with_llm(
    mappings: List[Dict[str, Any]],
    cloud_provider: str,
    scale: str,
    client: Any
) -> Dict[str, Any]:
    """Estimate costs using LLM"""
    
    # Prepare architecture summary
    arch_summary = []
    for mapping in mappings[:15]:  # Limit context
        arch_summary.append({
            "service": mapping.get("cloud_service", ""),
            "pattern": mapping.get("architecture_pattern", ""),
            "additional": mapping.get("additional_services", [])
        })
    
    system_prompt = f"""You are a cloud financial analyst specializing in {cloud_provider.upper()} pricing.

Estimate monthly costs for the proposed architecture considering:
- Free tier where applicable
- Public pricing references
- Scale: {scale}
- Cost optimization best practices

Provide Low, Expected, and High cost ranges.

Return ONLY valid JSON with no additional text."""

    user_prompt = f"""Estimate monthly costs for this {cloud_provider.upper()} architecture (Scale: {scale}):

{json.dumps(arch_summary, indent=2)}

Return JSON following this schema:
{{
  "summary": {{
    "low": 500,
    "expected": 1200,
    "high": 2500,
    "currency": "USD",
    "period": "monthly"
  }},
  "breakdown": [
    {{
      "category": "Compute",
      "service": "Azure Virtual Machines",
      "low": 200,
      "expected": 500,
      "high": 1000,
      "assumptions": ["2 VMs", "Standard_D2s_v3", "730 hours/month"]
    }}
  ],
  "assumptions": ["Standard usage patterns", "No reserved instances"],
  "optimization_opportunities": ["Use reserved instances for 30% savings"]
}}"""

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
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            
            cost_estimate = json.loads(content)
            
            # Validate structure
            if "summary" in cost_estimate and "breakdown" in cost_estimate:
                return cost_estimate
            else:
                print("[WARN] Invalid LLM cost response, using fallback")
                return _estimate_with_rules(mappings, cloud_provider, scale)
                
        except json.JSONDecodeError:
            print("[WARN] Failed to parse LLM cost response, using fallback")
            return _estimate_with_rules(mappings, cloud_provider, scale)
            
    except Exception as e:
        print(f"[WARN] LLM cost estimation failed: {e}, using fallback")
        return _estimate_with_rules(mappings, cloud_provider, scale)


def _estimate_with_rules(
    mappings: List[Dict[str, Any]],
    cloud_provider: str,
    scale: str
) -> Dict[str, Any]:
    """Rule-based cost estimation (fallback)"""
    
    # Scale multipliers
    scale_multipliers = {
        "small": {"compute": 0.5, "storage": 0.5, "network": 0.5},
        "medium": {"compute": 1.0, "storage": 1.0, "network": 1.0},
        "large": {"compute": 2.5, "storage": 2.0, "network": 1.5},
        "enterprise": {"compute": 5.0, "storage": 4.0, "network": 3.0}
    }
    
    multiplier = scale_multipliers.get(scale.lower(), scale_multipliers["medium"])
    
    # Base cost templates (monthly USD)
    cost_templates = {
        "azure": {
            "compute": {"base": 150, "pattern": "per VM/service"},
            "storage": {"base": 50, "pattern": "per TB"},
            "database": {"base": 100, "pattern": "per instance"},
            "networking": {"base": 40, "pattern": "per vnet/gateway"},
            "security": {"base": 30, "pattern": "per service"},
            "monitoring": {"base": 25, "pattern": "per workspace"},
            "kubernetes": {"base": 200, "pattern": "per cluster"},
            "serverless": {"base": 20, "pattern": "per million requests"},
            "ha_dr": {"base": 80, "pattern": "per region pair"}
        },
        "aws": {
            "compute": {"base": 140, "pattern": "per instance"},
            "storage": {"base": 45, "pattern": "per TB"},
            "database": {"base": 95, "pattern": "per instance"},
            "networking": {"base": 35, "pattern": "per VPC"},
            "security": {"base": 25, "pattern": "per service"},
            "monitoring": {"base": 20, "pattern": "per workspace"},
            "kubernetes": {"base": 180, "pattern": "per cluster"},
            "serverless": {"base": 15, "pattern": "per million requests"},
            "ha_dr": {"base": 75, "pattern": "per region pair"}
        },
        "gcp": {
            "compute": {"base": 135, "pattern": "per instance"},
            "storage": {"base": 40, "pattern": "per TB"},
            "database": {"base": 90, "pattern": "per instance"},
            "networking": {"base": 30, "pattern": "per VPC"},
            "security": {"base": 20, "pattern": "per service"},
            "monitoring": {"base": 18, "pattern": "per workspace"},
            "kubernetes": {"base": 170, "pattern": "per cluster"},
            "serverless": {"base": 12, "pattern": "per million requests"},
            "ha_dr": {"base": 70, "pattern": "per region pair"}
        }
    }
    
    templates = cost_templates.get(cloud_provider.lower(), cost_templates["azure"])
    
    # Categorize services and estimate costs
    category_costs = {}
    breakdown = []
    
    for mapping in mappings:
        service = mapping.get("cloud_service", "").lower()
        service_name = mapping.get("cloud_service", "Unknown Service")
        pattern = mapping.get("architecture_pattern", "Standard")
        
        # Determine category
        category = "other"
        if any(word in service for word in ["vm", "app service", "container instance", "compute"]):
            category = "compute"
        elif any(word in service for word in ["storage", "blob", "disk", "file"]):
            category = "storage"
        elif any(word in service for word in ["sql", "database", "cosmos", "postgresql"]):
            category = "database"
        elif any(word in service for word in ["network", "vpn", "vnet", "gateway"]):
            category = "networking"
        elif any(word in service for word in ["security", "key vault", "firewall", "ad"]):
            category = "security"
        elif any(word in service for word in ["monitor", "insights", "log"]):
            category = "monitoring"
        elif any(word in service for word in ["kubernetes", "aks", "eks", "gke"]):
            category = "kubernetes"
        elif any(word in service for word in ["function", "lambda", "serverless"]):
            category = "serverless"
        elif any(word in service for word in ["front door", "traffic", "recovery", "backup"]):
            category = "ha_dr"
        
        # Get base cost
        if category in templates:
            base_cost = templates[category]["base"]
            cost_pattern = templates[category]["pattern"]
        else:
            base_cost = 50
            cost_pattern = "per service"
        
        # Apply scale multiplier
        category_mult = multiplier.get(category.split("_")[0], 1.0)
        
        # Pattern multipliers (multi-region, HA adds cost)
        pattern_mult = 1.0
        if "multi-region" in pattern.lower() or "active-active" in pattern.lower():
            pattern_mult = 2.0
        elif "active-passive" in pattern.lower():
            pattern_mult = 1.5
        
        expected_cost = round(base_cost * category_mult * pattern_mult, 2)
        low_cost = round(expected_cost * 0.7, 2)
        high_cost = round(expected_cost * 1.5, 2)
        
        # Track category totals
        if category not in category_costs:
            category_costs[category] = {"low": 0, "expected": 0, "high": 0, "services": []}
        
        category_costs[category]["low"] += low_cost
        category_costs[category]["expected"] += expected_cost
        category_costs[category]["high"] += high_cost
        category_costs[category]["services"].append(service_name)
        
        # Add to breakdown
        breakdown.append({
            "category": category.replace("_", " ").title(),
            "service": service_name,
            "low": low_cost,
            "expected": expected_cost,
            "high": high_cost,
            "assumptions": [
                f"Scale: {scale}",
                f"Pattern: {pattern}",
                cost_pattern
            ]
        })
    
    # Calculate totals
    total_low = sum(c["low"] for c in category_costs.values())
    total_expected = sum(c["expected"] for c in category_costs.values())
    total_high = sum(c["high"] for c in category_costs.values())
    
    # Build cost estimate
    cost_estimate = {
        "summary": {
            "low": round(total_low, 2),
            "expected": round(total_expected, 2),
            "high": round(total_high, 2),
            "currency": "USD",
            "period": "monthly",
            "scale": scale,
            "cloud_provider": cloud_provider.upper()
        },
        "breakdown": breakdown,
        "category_summary": [
            {
                "category": cat.replace("_", " ").title(),
                "low": round(costs["low"], 2),
                "expected": round(costs["expected"], 2),
                "high": round(costs["high"], 2),
                "service_count": len(costs["services"])
            }
            for cat, costs in category_costs.items()
        ],
        "assumptions": [
            f"Deployment scale: {scale}",
            "Pay-as-you-go pricing (no reservations)",
            "Standard usage patterns assumed",
            "Costs based on public pricing",
            "Free tier utilized where available",
            "No support plan costs included"
        ],
        "optimization_opportunities": [
            "Consider reserved instances for 30-50% savings on compute",
            "Use auto-scaling to optimize resource utilization",
            "Implement lifecycle policies for storage cost optimization",
            "Evaluate serverless alternatives for variable workloads",
            "Review and rightsize resources based on actual usage",
            "Consider committed use discounts for predictable workloads"
        ]
    }
    
    return cost_estimate


def _save_cost_estimate(estimate: Dict[str, Any], output_path: Path):
    """Save cost estimate to files"""
    
    import csv
    
    # Save JSON
    json_file = output_path / "cost_estimate.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(estimate, f, indent=2, ensure_ascii=False)
    
    # Save summary CSV
    csv_file = output_path / "cost_breakdown.csv"
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(
            f,
            fieldnames=['Category', 'Service', 'Low (USD)', 'Expected (USD)', 'High (USD)', 'Assumptions']
        )
        writer.writeheader()
        
        for item in estimate.get("breakdown", []):
            writer.writerow({
                'Category': item.get('category', ''),
                'Service': item.get('service', ''),
                'Low (USD)': item.get('low', 0),
                'Expected (USD)': item.get('expected', 0),
                'High (USD)': item.get('high', 0),
                'Assumptions': '; '.join(item.get('assumptions', []))
            })
    
    # Save summary markdown
    md_file = output_path / "cost_summary.md"
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write(_generate_cost_markdown(estimate))
    
    print(f"[OK] Cost estimate saved to {output_path}")


def _generate_cost_markdown(estimate: Dict[str, Any]) -> str:
    """Generate markdown cost summary"""
    
    from datetime import datetime
    
    lines = []
    summary = estimate.get("summary", {})
    
    lines.append(f"# Cloud Cost Estimate")
    lines.append("")
    lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"**Cloud Provider:** {summary.get('cloud_provider', 'N/A')}")
    lines.append(f"**Scale:** {summary.get('scale', 'N/A').title()}")
    lines.append(f"**Period:** {summary.get('period', 'monthly').title()}")
    lines.append("")
    
    lines.append("## Cost Summary")
    lines.append("")
    lines.append("| Estimate Type | Cost (USD) |")
    lines.append("|--------------|-----------|")
    lines.append(f"| **Low Estimate** | ${summary.get('low', 0):,.2f} |")
    lines.append(f"| **Expected Cost** | ${summary.get('expected', 0):,.2f} |")
    lines.append(f"| **High Estimate** | ${summary.get('high', 0):,.2f} |")
    lines.append("")
    
    # Category breakdown
    if "category_summary" in estimate:
        lines.append("## Cost Breakdown by Category")
        lines.append("")
        lines.append("| Category | Services | Low | Expected | High |")
        lines.append("|----------|----------|-----|----------|------|")
        
        for cat in estimate["category_summary"]:
            lines.append(
                f"| {cat['category']} | {cat['service_count']} | "
                f"${cat['low']:,.2f} | ${cat['expected']:,.2f} | ${cat['high']:,.2f} |"
            )
        lines.append("")
    
    # Detailed breakdown
    lines.append("## Detailed Service Costs")
    lines.append("")
    
    for item in estimate.get("breakdown", [])[:10]:  # First 10 services
        lines.append(f"### {item.get('service', 'Unknown')}")
        lines.append(f"- **Category:** {item.get('category', 'N/A')}")
        lines.append(f"- **Expected Monthly Cost:** ${item.get('expected', 0):,.2f}")
        lines.append(f"- **Range:** ${item.get('low', 0):,.2f} - ${item.get('high', 0):,.2f}")
        
        if item.get('assumptions'):
            lines.append(f"- **Assumptions:** {', '.join(item['assumptions'])}")
        lines.append("")
    
    # Assumptions
    lines.append("## Assumptions")
    lines.append("")
    for assumption in estimate.get("assumptions", []):
        lines.append(f"- {assumption}")
    lines.append("")
    
    # Optimization opportunities
    lines.append("## Cost Optimization Opportunities")
    lines.append("")
    for opp in estimate.get("optimization_opportunities", []):
        lines.append(f"- {opp}")
    lines.append("")
    
    lines.append("---")
    lines.append("")
    lines.append("*Note: Costs are estimates based on public pricing and may vary based on actual usage, region, and commitment level.*")
    
    return '\n'.join(lines)
