"""
Stage 5: Proposal Pack Agent
Generates executive-ready proposal documents and artifacts
"""

import json
import os
from typing import Dict, Any, List, Optional
from pathlib import Path
from datetime import datetime


def generate_proposal_pack(
    stage1_results: Dict[str, Any],
    architecture_mappings: List[Dict[str, Any]],
    cost_estimate: Dict[str, Any],
    cloud_provider: str = "azure",
    llm_client: Optional[Any] = None,
    output_dir: str = "stage5_proposal"
) -> Dict[str, str]:
    """
    Generate complete proposal pack with all artifacts
    
    Args:
        stage1_results: Results from Stage 1 (requirements, evaluation, risks, strategy)
        architecture_mappings: Architecture mappings from Stage 2
        cost_estimate: Cost estimate from Stage 4
        cloud_provider: Target cloud provider
        llm_client: Optional LLM client for enhanced proposal generation
        output_dir: Output directory for proposal artifacts
        
    Returns:
        Dictionary with paths to generated artifacts
    """
    
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    artifacts = {}
    
    # 1. Executive Summary
    print("[1/5] Generating executive summary...")
    exec_summary = _generate_executive_summary(
        stage1_results, architecture_mappings, cost_estimate, cloud_provider, llm_client
    )
    exec_file = output_path / "executive_summary.md"
    with open(exec_file, 'w', encoding='utf-8') as f:
        f.write(exec_summary)
    artifacts['executive_summary'] = str(exec_file)
    
    # 2. Technical Proposal
    print("[2/5] Generating technical proposal...")
    tech_proposal = _generate_technical_proposal(
        stage1_results, architecture_mappings, cloud_provider
    )
    tech_file = output_path / "technical_proposal.md"
    with open(tech_file, 'w', encoding='utf-8') as f:
        f.write(tech_proposal)
    artifacts['technical_proposal'] = str(tech_file)
    
    # 3. Risks and Assumptions Register
    print("[3/5] Generating risks and assumptions...")
    risks_doc = _generate_risks_register(stage1_results, architecture_mappings)
    risks_file = output_path / "risks_and_assumptions.md"
    with open(risks_file, 'w', encoding='utf-8') as f:
        f.write(risks_doc)
    artifacts['risks_register'] = str(risks_file)
    
    # 4. Pricing Proposal
    print("[4/5] Generating pricing proposal...")
    pricing_doc = _generate_pricing_proposal(cost_estimate, cloud_provider)
    pricing_file = output_path / "pricing_proposal.md"
    with open(pricing_file, 'w', encoding='utf-8') as f:
        f.write(pricing_doc)
    artifacts['pricing_proposal'] = str(pricing_file)
    
    # 5. Master Proposal Index
    print("[5/5] Generating master proposal document...")
    master_doc = _generate_master_proposal(
        stage1_results, architecture_mappings, cost_estimate, cloud_provider, artifacts
    )
    master_file = output_path / "MASTER_PROPOSAL.md"
    with open(master_file, 'w', encoding='utf-8') as f:
        f.write(master_doc)
    artifacts['master_proposal'] = str(master_file)
    
    print(f"[OK] Proposal pack generated in {output_dir}")
    
    return artifacts


def _generate_executive_summary(
    stage1: Dict[str, Any],
    arch_mappings: List[Dict[str, Any]],
    costs: Dict[str, Any],
    cloud_provider: str,
    llm_client: Optional[Any]
) -> str:
    """Generate executive summary (2-3 pages)"""
    
    if llm_client:
        return _generate_executive_with_llm(stage1, arch_mappings, costs, cloud_provider, llm_client)
    else:
        return _generate_executive_with_template(stage1, arch_mappings, costs, cloud_provider)


def _generate_executive_with_template(
    stage1: Dict[str, Any],
    arch_mappings: List[Dict[str, Any]],
    costs: Dict[str, Any],
    cloud_provider: str
) -> str:
    """Generate executive summary using template"""
    
    lines = []
    
    # Header
    lines.append("# Executive Summary")
    lines.append("## Cloud Solution Proposal")
    lines.append("")
    lines.append(f"**Date:** {datetime.now().strftime('%B %d, %Y')}")
    lines.append(f"**Cloud Platform:** {cloud_provider.upper()}")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # Overview
    lines.append("## 1. Solution Overview")
    lines.append("")
    
    req_count = len(stage1.get("requirements", []))
    mandatory_count = sum(1 for r in stage1.get("requirements", []) if r.get("type") == "Mandatory")
    
    lines.append(f"This proposal presents a comprehensive {cloud_provider.upper()}-based cloud solution designed to meet "
                 f"the requirements outlined in your RFP. Our solution addresses **{req_count} requirements** "
                 f"({mandatory_count} mandatory, {req_count - mandatory_count} optional) through a modern, "
                 f"scalable architecture leveraging best-in-class cloud services.")
    lines.append("")
    
    lines.append("### Key Highlights")
    lines.append("")
    lines.append(f"- **{len(arch_mappings)} cloud services** strategically selected for optimal performance")
    lines.append("- **Enterprise-grade** architecture patterns ensuring high availability and disaster recovery")
    lines.append("- **Cost-effective** solution with transparent pricing and optimization opportunities")
    lines.append("- **Compliance-focused** design addressing all mandatory requirements")
    lines.append("")
    
    # Architecture Highlights
    lines.append("## 2. Architecture Highlights")
    lines.append("")
    
    # Get unique patterns
    patterns = set(m.get("architecture_pattern", "Standard") for m in arch_mappings)
    
    lines.append("Our proposed architecture leverages proven cloud-native patterns:")
    lines.append("")
    for pattern in sorted(patterns)[:5]:
        lines.append(f"- **{pattern}** - Ensuring resilience and scalability")
    lines.append("")
    
    # Service categories
    lines.append("### Core Service Categories")
    lines.append("")
    
    # Categorize services
    categories = {}
    for mapping in arch_mappings:
        service = mapping.get("cloud_service", "")
        if service:
            # Simple categorization
            if any(word in service.lower() for word in ["vm", "app", "container", "function"]):
                cat = "Compute & Application Services"
            elif any(word in service.lower() for word in ["storage", "database", "sql"]):
                cat = "Data & Storage"
            elif any(word in service.lower() for word in ["network", "vpn", "security"]):
                cat = "Networking & Security"
            elif any(word in service.lower() for word in ["monitor", "insights"]):
                cat = "Monitoring & Observability"
            else:
                cat = "Infrastructure Services"
            
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(service)
    
    for cat, services in sorted(categories.items()):
        lines.append(f"**{cat}** ({len(services)} services)")
        for service in services[:3]:
            lines.append(f"  - {service}")
        if len(services) > 3:
            lines.append(f"  - *... and {len(services) - 3} more*")
        lines.append("")
    
    # Compliance Posture
    lines.append("## 3. Compliance Posture")
    lines.append("")
    
    compliance_counts = {}
    for mapping in arch_mappings:
        level = mapping.get("compliance_level", "Compliant")
        compliance_counts[level] = compliance_counts.get(level, 0) + 1
    
    lines.append("| Compliance Level | Count | Percentage |")
    lines.append("|-----------------|-------|------------|")
    total = sum(compliance_counts.values())
    for level in ["Fully Compliant", "Partially Compliant", "Compliant"]:
        count = compliance_counts.get(level, 0)
        pct = (count / total * 100) if total > 0 else 0
        lines.append(f"| {level} | {count} | {pct:.1f}% |")
    lines.append("")
    
    lines.append("Our solution demonstrates strong compliance with RFP requirements, with strategies "
                 "in place to address any partial compliance areas through phased implementation.")
    lines.append("")
    
    # Cost Summary
    lines.append("## 4. Investment Summary")
    lines.append("")
    
    cost_summary = costs.get("summary", {})
    expected = cost_summary.get("expected", 0)
    low = cost_summary.get("low", 0)
    high = cost_summary.get("high", 0)
    
    lines.append(f"**Estimated Monthly Investment:** ${expected:,.2f} USD")
    lines.append("")
    lines.append(f"- **Conservative Estimate:** ${low:,.2f}")
    lines.append(f"- **Expected Cost:** ${expected:,.2f}")
    lines.append(f"- **Maximum Estimate:** ${high:,.2f}")
    lines.append("")
    
    lines.append("This investment includes all core infrastructure services with room for growth. "
                 "Our proposal includes multiple cost optimization strategies that can reduce ongoing "
                 "expenses by 30-50% through reserved capacity and right-sizing.")
    lines.append("")
    
    # Risk Management
    lines.append("## 5. Risk Management")
    lines.append("")
    
    risks = stage1.get("risks", [])
    high_risks = [r for r in risks if r.get("severity") == "High"]
    
    lines.append(f"We have identified and assessed **{len(risks)} potential risks**, including "
                 f"{len(high_risks)} high-priority items. Each risk includes:")
    lines.append("")
    lines.append("- Detailed impact analysis")
    lines.append("- Mitigation strategies")
    lines.append("- Contingency plans")
    lines.append("- Monitoring and control measures")
    lines.append("")
    
    if high_risks:
        lines.append("### Top Priority Risks")
        lines.append("")
        for risk in high_risks[:3]:
            lines.append(f"**{risk.get('category', 'General')}**: {risk.get('description', '')[:100]}...")
            lines.append(f"  - *Mitigation:* {risk.get('mitigation', 'See detailed risk register')[:80]}...")
            lines.append("")
    
    # Strategic Advantages
    lines.append("## 6. Strategic Advantages")
    lines.append("")
    
    strategy = stage1.get("strategy", {})
    differentiators = strategy.get("differentiators", [])
    
    if differentiators:
        lines.append("Our solution provides unique strategic advantages:")
        lines.append("")
        for diff in differentiators:
            # Handle both string and dict formats
            if isinstance(diff, dict):
                lines.append(f"- **{diff.get('area', 'Advantage')}**: {diff.get('description', '')}")
            else:
                lines.append(f"- {diff}")
        lines.append("")
    else:
        lines.append("- Cloud-native architecture for maximum agility")
        lines.append("- Comprehensive automation reducing operational overhead")
        lines.append("- Built-in security and compliance controls")
        lines.append("- Scalable design supporting future growth")
        lines.append("")
    
    # Next Steps
    lines.append("## 7. Next Steps")
    lines.append("")
    lines.append("We recommend the following timeline for engagement:")
    lines.append("")
    lines.append("1. **Week 1-2:** Detailed requirements validation and architecture refinement")
    lines.append("2. **Week 3-4:** Proof of concept development for critical components")
    lines.append("3. **Week 5-8:** Pilot deployment in non-production environment")
    lines.append("4. **Week 9-12:** Production rollout with phased migration")
    lines.append("")
    lines.append("Our team is ready to begin immediately upon contract execution.")
    lines.append("")
    
    # Conclusion
    lines.append("## Conclusion")
    lines.append("")
    lines.append(f"This {cloud_provider.upper()}-based solution represents the optimal balance of performance, "
                 f"reliability, security, and cost-effectiveness. We are confident in our ability to deliver "
                 f"a solution that not only meets but exceeds your requirements.")
    lines.append("")
    lines.append("We look forward to partnering with you on this transformative cloud journey.")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("*For detailed technical specifications, compliance matrices, and cost breakdowns, "
                 "please refer to the accompanying proposal documents.*")
    
    return '\n'.join(lines)


def _generate_executive_with_llm(
    stage1: Dict[str, Any],
    arch_mappings: List[Dict[str, Any]],
    costs: Dict[str, Any],
    cloud_provider: str,
    client: Any
) -> str:
    """Generate executive summary using LLM"""
    
    # Prepare context
    context = {
        "requirements_count": len(stage1.get("requirements", [])),
        "mandatory_count": sum(1 for r in stage1.get("requirements", []) if r.get("type") == "Mandatory"),
        "services_count": len(arch_mappings),
        "expected_cost": costs.get("summary", {}).get("expected", 0),
        "cloud_provider": cloud_provider.upper(),
        "risks_count": len(stage1.get("risks", []))
    }
    
    system_prompt = """You are an expert proposal writer specializing in cloud solutions.

Create an executive-ready proposal summary that is:
- Professional and presales-ready
- 2-3 pages maximum
- Focused on business value
- Clear and concise
- Compelling but honest

Include: Solution overview, architecture highlights, compliance posture, cost summary, risk management, and next steps."""

    user_prompt = f"""Generate an executive summary for a {cloud_provider.upper()} cloud solution proposal with:

- {context['requirements_count']} requirements ({context['mandatory_count']} mandatory)
- {context['services_count']} cloud services in proposed architecture
- ${context['expected_cost']:,.2f} monthly estimated cost
- {context['risks_count']} identified risks with mitigation plans

Make it compelling, professional, and executive-ready."""

    try:
        response = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o-mini")),
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        print(f"[WARN] LLM executive summary failed: {e}, using template")
        return _generate_executive_with_template(stage1, arch_mappings, costs, cloud_provider)


def _generate_technical_proposal(
    stage1: Dict[str, Any],
    arch_mappings: List[Dict[str, Any]],
    cloud_provider: str
) -> str:
    """Generate detailed technical proposal"""
    
    lines = []
    
    lines.append("# Technical Proposal")
    lines.append(f"## {cloud_provider.upper()} Cloud Solution")
    lines.append("")
    lines.append(f"**Date:** {datetime.now().strftime('%B %d, %Y')}")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    lines.append("## 1. Technical Architecture")
    lines.append("")
    lines.append("### 1.1 Architecture Overview")
    lines.append("")
    lines.append(f"The proposed solution leverages {len(arch_mappings)} {cloud_provider.upper()} services "
                 f"configured in enterprise-grade architecture patterns to ensure high availability, "
                 f"disaster recovery, security, and scalability.")
    lines.append("")
    
    lines.append("### 1.2 Service Mappings")
    lines.append("")
    lines.append("| Requirement ID | Cloud Service | Architecture Pattern | Compliance |")
    lines.append("|---------------|---------------|---------------------|------------|")
    
    for mapping in arch_mappings[:15]:  # First 15 for brevity
        lines.append(
            f"| {mapping.get('req_id', '')} | "
            f"{mapping.get('cloud_service', '')} | "
            f"{mapping.get('architecture_pattern', '')} | "
            f"{mapping.get('compliance_level', '')} |"
        )
    
    if len(arch_mappings) > 15:
        lines.append(f"| ... | *{len(arch_mappings) - 15} more services* | ... | ... |")
    
    lines.append("")
    lines.append("*See architecture_mappings.csv for complete service details*")
    lines.append("")
    
    lines.append("## 2. Implementation Approach")
    lines.append("")
    lines.append("### 2.1 Phased Deployment")
    lines.append("")
    lines.append("**Phase 1: Foundation (Weeks 1-4)**")
    lines.append("- Network and security infrastructure")
    lines.append("- Identity and access management")
    lines.append("- Monitoring and logging setup")
    lines.append("")
    lines.append("**Phase 2: Core Services (Weeks 5-8)**")
    lines.append("- Compute and storage provisioning")
    lines.append("- Database deployment")
    lines.append("- Application migration")
    lines.append("")
    lines.append("**Phase 3: Advanced Features (Weeks 9-12)**")
    lines.append("- High availability configuration")
    lines.append("- Disaster recovery testing")
    lines.append("- Performance optimization")
    lines.append("")
    
    lines.append("## 3. Security & Compliance")
    lines.append("")
    lines.append("- End-to-end encryption for data in transit and at rest")
    lines.append("- Multi-factor authentication and role-based access control")
    lines.append("- Continuous security monitoring and threat detection")
    lines.append("- Compliance with industry standards (ISO 27001, SOC 2, etc.)")
    lines.append("")
    
    lines.append("## 4. Support & Maintenance")
    lines.append("")
    lines.append("- 24/7 monitoring and alerting")
    lines.append("- Automated backup and recovery procedures")
    lines.append("- Regular security patching and updates")
    lines.append("- Quarterly architecture reviews")
    lines.append("")
    
    return '\n'.join(lines)


def _generate_risks_register(
    stage1: Dict[str, Any],
    arch_mappings: List[Dict[str, Any]]
) -> str:
    """Generate risks and assumptions register"""
    
    lines = []
    
    lines.append("# Risks and Assumptions Register")
    lines.append("")
    lines.append(f"**Date:** {datetime.now().strftime('%B %d, %Y')}")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # Risks
    lines.append("## Identified Risks")
    lines.append("")
    
    risks = stage1.get("risks", [])
    
    if risks:
        lines.append("| ID | Category | Severity | Description | Mitigation |")
        lines.append("|----|----------|----------|-------------|------------|")
        
        for i, risk in enumerate(risks, 1):
            lines.append(
                f"| R-{i:03d} | {risk.get('category', 'General')} | "
                f"{risk.get('severity', 'Medium')} | "
                f"{risk.get('description', '')[:50]}... | "
                f"{risk.get('mitigation', '')[:50]}... |"
            )
        lines.append("")
    else:
        lines.append("No specific risks identified at this stage. Standard cloud migration risks apply.")
        lines.append("")
    
    # Assumptions
    lines.append("## Key Assumptions")
    lines.append("")
    
    # Collect assumptions from architecture mappings
    all_assumptions = set()
    for mapping in arch_mappings:
        for assumption in mapping.get("assumptions", []):
            all_assumptions.add(assumption)
    
    if all_assumptions:
        for i, assumption in enumerate(sorted(all_assumptions), 1):
            lines.append(f"{i}. {assumption}")
        lines.append("")
    
    # Standard assumptions
    lines.append("### Standard Project Assumptions")
    lines.append("")
    lines.append("1. Customer provides timely access to existing systems and documentation")
    lines.append("2. Network connectivity and bandwidth requirements are met")
    lines.append("3. Required cloud subscriptions and permissions are provisioned")
    lines.append("4. Stakeholders are available for design reviews and approvals")
    lines.append("5. Data classification and compliance requirements are documented")
    lines.append("")
    
    return '\n'.join(lines)


def _generate_pricing_proposal(costs: Dict[str, Any], cloud_provider: str) -> str:
    """Generate pricing proposal"""
    
    lines = []
    
    lines.append("# Pricing Proposal")
    lines.append(f"## {cloud_provider.upper()} Cloud Solution")
    lines.append("")
    lines.append(f"**Date:** {datetime.now().strftime('%B %d, %Y')}")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    summary = costs.get("summary", {})
    
    lines.append("## Investment Summary")
    lines.append("")
    lines.append(f"**Expected Monthly Cost:** ${summary.get('expected', 0):,.2f} USD")
    lines.append("")
    lines.append("| Estimate Type | Monthly Cost |")
    lines.append("|--------------|-------------|")
    lines.append(f"| Low Estimate | ${summary.get('low', 0):,.2f} |")
    lines.append(f"| Expected Cost | ${summary.get('expected', 0):,.2f} |")
    lines.append(f"| High Estimate | ${summary.get('high', 0):,.2f} |")
    lines.append("")
    
    # Category breakdown
    if "category_summary" in costs:
        lines.append("## Cost Breakdown by Category")
        lines.append("")
        lines.append("| Category | Expected Monthly Cost |")
        lines.append("|----------|--------------------|")
        
        for cat in costs["category_summary"]:
            lines.append(f"| {cat['category']} | ${cat['expected']:,.2f} |")
        lines.append("")
    
    # Assumptions
    lines.append("## Pricing Assumptions")
    lines.append("")
    for assumption in costs.get("assumptions", []):
        lines.append(f"- {assumption}")
    lines.append("")
    
    # Optimization
    lines.append("## Cost Optimization Opportunities")
    lines.append("")
    for opp in costs.get("optimization_opportunities", []):
        lines.append(f"- {opp}")
    lines.append("")
    
    return '\n'.join(lines)


def _generate_master_proposal(
    stage1: Dict[str, Any],
    arch_mappings: List[Dict[str, Any]],
    costs: Dict[str, Any],
    cloud_provider: str,
    artifacts: Dict[str, str]
) -> str:
    """Generate master proposal index document"""
    
    lines = []
    
    lines.append("# RFP Response - Master Proposal")
    lines.append(f"## {cloud_provider.upper()} Cloud Solution")
    lines.append("")
    lines.append(f"**Date:** {datetime.now().strftime('%B %d, %Y')}")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    lines.append("## Proposal Package Contents")
    lines.append("")
    lines.append("This comprehensive proposal includes the following documents:")
    lines.append("")
    
    lines.append("### 1. Executive Summary")
    lines.append(f"📄 `{Path(artifacts.get('executive_summary', '')).name}`")
    lines.append("")
    lines.append("High-level overview of the proposed solution, including architecture highlights, "
                 "compliance posture, investment summary, and strategic advantages.")
    lines.append("")
    
    lines.append("### 2. Technical Proposal")
    lines.append(f"📄 `{Path(artifacts.get('technical_proposal', '')).name}`")
    lines.append("")
    lines.append("Detailed technical architecture, service mappings, implementation approach, "
                 "and support plans.")
    lines.append("")
    
    lines.append("### 3. Pricing Proposal")
    lines.append(f"📄 `{Path(artifacts.get('pricing_proposal', '')).name}`")
    lines.append("")
    lines.append("Comprehensive cost breakdown with low/expected/high estimates, assumptions, "
                 "and optimization opportunities.")
    lines.append("")
    
    lines.append("### 4. Risks and Assumptions Register")
    lines.append(f"📄 `{Path(artifacts.get('risks_register', '')).name}`")
    lines.append("")
    lines.append("Complete listing of identified risks with mitigation strategies and "
                 "key project assumptions.")
    lines.append("")
    
    lines.append("## Quick Summary")
    lines.append("")
    
    req_count = len(stage1.get("requirements", []))
    mandatory_count = sum(1 for r in stage1.get("requirements", []) if r.get("type") == "Mandatory")
    
    lines.append(f"- **Requirements Addressed:** {req_count} ({mandatory_count} mandatory)")
    lines.append(f"- **Cloud Services Proposed:** {len(arch_mappings)}")
    lines.append(f"- **Expected Monthly Investment:** ${costs.get('summary', {}).get('expected', 0):,.2f}")
    lines.append(f"- **Identified Risks:** {len(stage1.get('risks', []))}")
    lines.append("")
    
    lines.append("## Supporting Artifacts")
    lines.append("")
    lines.append("The following technical artifacts are also included:")
    lines.append("")
    lines.append("- `output/compliance_matrix.csv` - Detailed requirements compliance tracking")
    lines.append("- `stage2_architecture/architecture_mappings.csv` - Service-to-requirement mappings")
    lines.append("- `stage3_diagrams/azure_architecture.drawio.xml` - Solution architecture diagram")
    lines.append("- `stage4_costing/cost_breakdown.csv` - Detailed cost analysis")
    lines.append("- `output/stage1_full_report.json` - Complete analysis data (JSON)")
    lines.append("")
    
    lines.append("---")
    lines.append("")
    lines.append("*This proposal was generated using an AI-powered RFP automation platform, "
                 "ensuring comprehensive coverage, consistency, and compliance with all requirements.*")
    
    return '\n'.join(lines)
