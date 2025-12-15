"""
Proposal Agent
Generates executive summary and proposal document using AI
"""
import json
from config.ai_config import config
from utils.ai_client import ai_client


class ProposalAgent:
    def __init__(self):
        self.use_ai = config.ai_enabled
    
    def run(self, rfp_analysis: dict, architecture: dict, cost: dict) -> str:
        """
        Generates proposal document in Markdown format
        
        Args:
            rfp_analysis: RFP analysis results
            architecture: Architecture specification
            cost: Cost estimate
            
        Returns:
            Markdown-formatted proposal document
        """
        if self.use_ai:
            return self._generate_with_ai(rfp_analysis, architecture, cost)
        else:
            return self._generate_static(rfp_analysis, architecture, cost)
    
    def _generate_with_ai(self, rfp_analysis: dict, architecture: dict, cost: dict) -> str:
        """Use AI to generate proposal"""
        system_prompt = """You are a pre-sales consultant creating a professional cloud solution proposal.

Generate a comprehensive, executive-level proposal document in Markdown format.

Include these sections:
1. Executive Summary
2. Business Objectives Alignment
3. Proposed Architecture Overview
4. Architecture Layers and Components
5. Security Controls
6. Disaster Recovery
7. Cost Breakdown
8. Non-Functional Requirements
9. Risk Mitigation
10. Next Steps
11. Conclusion

Make it professional, persuasive, and technically sound. Use tables where appropriate."""

        try:
            print("🤖 Using AI to generate proposal...")
            
            context = f"""RFP Analysis:
{json.dumps(rfp_analysis, indent=2)}

Architecture:
{json.dumps(architecture, indent=2)}

Cost Estimate:
{json.dumps(cost, indent=2)}

Generate a compelling proposal based on this information."""

            response = ai_client.analyze_with_prompt(system_prompt, context, temperature=0.5)
            print("✓ AI proposal generation complete")
            return response
            
        except Exception as e:
            print(f"⚠️ AI proposal generation failed: {e}")
            print("⚠️ Falling back to static proposal")
            return self._generate_static(rfp_analysis, architecture, cost)
    
    def _generate_static(self, rfp_analysis: dict, architecture: dict, cost: dict) -> str:
        """Static fallback proposal"""
        # Original static template
        proposal = f"""# Cloud Solution Proposal

## Executive Summary

This proposal presents a comprehensive cloud solution designed to meet your organization's requirements for modernization, scalability, and security. Our solution leverages **{cost['cloud_provider']}** cloud services to deliver a robust, scalable, and cost-effective architecture.

### Key Highlights

- **Estimated Monthly Cost:** ${cost['summary']['total_monthly']:,.2f} USD
- **Estimated Annual Cost:** ${cost['summary']['total_annual']:,.2f} USD
- **Target Availability:** {rfp_analysis['non_functional_requirements']['availability']}
- **Compliance:** {', '.join(rfp_analysis['non_functional_requirements']['compliance'])}

---

## Business Objectives

Our solution addresses the following business goals:

"""
        for goal in rfp_analysis['business_goals']:
            proposal += f"- {goal}\n"
        
        proposal += f"""
---

## Proposed Architecture

### Architecture Overview

The proposed solution follows a **{len(architecture['layers'])}-tier layered architecture** designed for:

- Scalability
- Security
- High Availability
- Operational Excellence

### Architecture Layers

"""
        for layer in architecture['layers']:
            proposal += f"#### {layer['name']}\n\n"
            proposal += "**Components:**\n"
            for component in layer['components']:
                proposal += f"- {component}\n"
            proposal += "\n**Responsibilities:**\n"
            for responsibility in layer['responsibilities']:
                proposal += f"- {responsibility}\n"
            proposal += "\n"
        
        proposal += f"""
### Security Controls

"""
        for control in architecture.get('security_controls', []):
            proposal += f"- {control}\n"
        
        proposal += f"""

### Disaster Recovery

- **Recovery Point Objective (RPO):** {architecture['disaster_recovery']['rpo']}
- **Recovery Time Objective (RTO):** {architecture['disaster_recovery']['rto']}
- **Strategy:** {architecture['disaster_recovery']['strategy']}

---

## Cost Breakdown

### Monthly Cost Summary

| Service | Type | Monthly Cost | Annual Cost |
|---------|------|--------------|-------------|
"""
        for component in cost['components']:
            proposal += f"| {component['service_name']} | {component['service_type']} | ${component['monthly_cost']:,.2f} | ${component['annual_cost']:,.2f} |\n"
        
        proposal += f"""
**Total Monthly:** ${cost['summary']['total_monthly']:,.2f} USD  
**Total Annual:** ${cost['summary']['total_annual']:,.2f} USD

### Cost Assumptions

"""
        for assumption in cost['assumptions']:
            proposal += f"- {assumption}\n"
        
        proposal += f"""

---

## Non-Functional Requirements

- **Performance:** {rfp_analysis['non_functional_requirements']['performance']}
- **Security:** {rfp_analysis['non_functional_requirements']['security']}
- **Availability:** {rfp_analysis['non_functional_requirements']['availability']}
- **Compliance Standards:** {', '.join(rfp_analysis['non_functional_requirements']['compliance'])}

---

## Risk Mitigation

We have identified the following risks and mitigation strategies:

"""
        for risk in rfp_analysis.get('risks', []):
            proposal += f"- **Risk:** {risk}\n"
            proposal += f"  - **Mitigation:** To be defined in detailed planning phase\n"
        
        proposal += f"""

---

## Next Steps

1. Solution review and feedback
2. Detailed technical design
3. Proof of Concept (POC) development
4. Implementation planning
5. Production deployment

---

## Conclusion

This proposal presents a comprehensive, scalable, and secure cloud solution that aligns with your business objectives. We are committed to delivering excellence and look forward to partnering with you on this transformative journey.

For questions or clarifications, please contact our pre-sales team.

---

*Generated by Agentic Pre-Sales POC*
"""
        
        return proposal
