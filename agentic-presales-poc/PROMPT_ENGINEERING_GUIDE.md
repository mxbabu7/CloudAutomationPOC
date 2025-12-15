# 🛠️ Prompt Engineering Guide - Customization & Best Practices

## 📚 Table of Contents
1. [Understanding the Prompt Structure](#understanding-the-prompt-structure)
2. [Modifying Existing Prompts](#modifying-existing-prompts)
3. [Adding New AI Agents](#adding-new-ai-agents)
4. [Prompt Engineering Best Practices](#prompt-engineering-best-practices)
5. [Common Customization Scenarios](#common-customization-scenarios)
6. [Testing & Validation](#testing--validation)

---

## Understanding the Prompt Structure

### Anatomy of an AI Prompt in This System

Every AI agent follows this structure:

```python
# 1. System Prompt - Defines the role and output format
system_prompt = """
You are a [ROLE].

[TASK DESCRIPTION]

Return [OUTPUT FORMAT]

[SPECIFIC REQUIREMENTS]
"""

# 2. User Content - Provides the data to process
user_content = f"""
[CONTEXT]
{input_data}

[INSTRUCTION]
"""

# 3. AI Call - Executes the prompt
response = ai_client.analyze_with_prompt(
    system_prompt, 
    user_content, 
    temperature=0.5  # Controls randomness
)

# 4. Response Processing - Cleans and parses output
result = clean_and_parse(response)
```

---

## Modifying Existing Prompts

### Example 1: Customize RFP Analysis to Include Budget

**Current**: `agents/rfp_analysis_agent.py`

**Before**:
```python
system_prompt = """You are an expert RFP analyst. Analyze the provided RFP document and extract structured information.

Return ONLY a valid JSON object with this exact structure:
{
  "business_goals": ["goal1", "goal2", ...],
  "functional_requirements": ["req1", "req2", ...],
  ...
}
```

**After** (add budget field):
```python
system_prompt = """You are an expert RFP analyst. Analyze the provided RFP document and extract structured information.

Return ONLY a valid JSON object with this exact structure:
{
  "business_goals": ["goal1", "goal2", ...],
  "functional_requirements": ["req1", "req2", ...],
  "budget_information": {
    "total_budget": "amount if specified",
    "budget_constraints": "description",
    "payment_terms": "description"
  },
  ...
}
```

### Example 2: Make Architecture More Detailed

**File**: `agents/architecture_agent.py`

**Enhancement**: Add component-level specifications

```python
system_prompt = """You are a cloud solutions architect. Design a cloud-agnostic logical architecture.

Return ONLY a valid JSON object with this exact structure:
{
  "layers": [
    {
      "name": "Layer Name",
      "components": [
        {
          "name": "Component Name",
          "type": "Web Server|Database|Cache|etc.",
          "specifications": {
            "cpu": "2 vCPUs",
            "memory": "4GB",
            "storage": "100GB"
          },
          "replicas": 2,
          "responsibilities": ["Responsibility1", "Responsibility2"]
        }
      ]
    }
  ],
  ...
}
```

### Example 3: Customize Proposal Tone

**File**: `agents/proposal_agent.py`

**Variations**:

**Formal/Enterprise**:
```python
system_prompt = """You are a senior pre-sales consultant at a Fortune 500 enterprise software company.

Generate a formal, board-level proposal document in Markdown format.

Tone: Professional, authoritative, data-driven
Style: Executive-level, strategic focus
Language: Formal business English

Include extensive ROI calculations, risk analysis, and executive summaries.
```

**Startup/Agile**:
```python
system_prompt = """You are a solutions architect at a modern cloud-native startup.

Generate a concise, developer-friendly proposal document in Markdown format.

Tone: Conversational, modern, technical
Style: Developer-focused, hands-on details
Language: Clear, direct, no jargon

Focus on technical implementation, scalability, and modern best practices.
```

---

## Adding New AI Agents

### Step 1: Create New Agent File

**File**: `agents/security_assessment_agent.py`

```python
"""
Security Assessment Agent
Analyzes architecture and generates security recommendations using AI
"""
import json
from config.ai_config import config
from utils.ai_client import ai_client


class SecurityAssessmentAgent:
    def __init__(self):
        self.use_ai = config.ai_enabled
    
    def run(self, architecture: dict, rfp_analysis: dict) -> dict:
        """
        Generates comprehensive security assessment
        
        Args:
            architecture: Architecture specification
            rfp_analysis: RFP analysis with compliance requirements
            
        Returns:
            Security assessment report
        """
        if self.use_ai:
            return self._assess_with_ai(architecture, rfp_analysis)
        else:
            return self._assess_static(architecture, rfp_analysis)
    
    def _assess_with_ai(self, architecture: dict, rfp_analysis: dict) -> dict:
        """Use AI to perform security assessment"""
        
        # Define the system prompt
        system_prompt = """You are a cybersecurity expert specializing in cloud infrastructure security.

Analyze the provided architecture and RFP requirements to generate a comprehensive security assessment.

Return ONLY a valid JSON object with this exact structure:
{
  "security_posture": {
    "overall_score": "1-10",
    "summary": "Brief assessment"
  },
  "threats_identified": [
    {
      "threat": "Threat description",
      "severity": "Critical|High|Medium|Low",
      "likelihood": "High|Medium|Low",
      "impact": "Description of potential impact"
    }
  ],
  "vulnerabilities": [
    {
      "component": "Component name",
      "vulnerability": "Description",
      "cvss_score": "0.0-10.0",
      "remediation": "How to fix"
    }
  ],
  "compliance_gaps": [
    {
      "standard": "ISO 27001|SOC 2|GDPR|etc.",
      "requirement": "Specific requirement",
      "gap": "What's missing",
      "priority": "High|Medium|Low"
    }
  ],
  "recommendations": [
    {
      "category": "Network|Identity|Data|Application|etc.",
      "recommendation": "Specific action",
      "rationale": "Why this is important",
      "effort": "Low|Medium|High",
      "impact": "Low|Medium|High"
    }
  ],
  "security_controls": {
    "preventive": ["Control1", "Control2"],
    "detective": ["Control1", "Control2"],
    "corrective": ["Control1", "Control2"]
  },
  "estimated_remediation_cost": {
    "low": "Minimum cost",
    "high": "Maximum cost"
  }
}

Be thorough, specific, and actionable in your recommendations."""

        try:
            print("🤖 Using AI to perform security assessment...")
            
            # Prepare context
            context = f"""Architecture:
{json.dumps(architecture, indent=2)}

RFP Compliance Requirements:
{json.dumps(rfp_analysis.get('non_functional_requirements', {}).get('compliance', []), indent=2)}

Security Requirements:
{rfp_analysis.get('non_functional_requirements', {}).get('security', 'Not specified')}

Analyze this architecture for security vulnerabilities and compliance gaps."""

            # Call AI
            response = ai_client.analyze_with_prompt(
                system_prompt, 
                context, 
                temperature=0.3  # Deterministic for security analysis
            )
            
            # Clean response
            response = response.strip()
            if response.startswith("```json"):
                response = response[7:]
            if response.startswith("```"):
                response = response[3:]
            if response.endswith("```"):
                response = response[:-3]
            response = response.strip()
            
            result = json.loads(response)
            print("✓ AI security assessment complete")
            return result
            
        except Exception as e:
            print(f"⚠️ AI security assessment failed: {e}")
            print("⚠️ Falling back to static assessment")
            return self._assess_static(architecture, rfp_analysis)
    
    def _assess_static(self, architecture: dict, rfp_analysis: dict) -> dict:
        """Static fallback assessment"""
        return {
            "security_posture": {
                "overall_score": "7",
                "summary": "Good baseline security with room for improvement"
            },
            "threats_identified": [
                {
                    "threat": "DDoS attacks on public endpoints",
                    "severity": "High",
                    "likelihood": "Medium",
                    "impact": "Service disruption and availability loss"
                }
            ],
            "recommendations": [
                {
                    "category": "Network",
                    "recommendation": "Implement Web Application Firewall (WAF)",
                    "rationale": "Protect against common web exploits",
                    "effort": "Low",
                    "impact": "High"
                }
            ]
        }
```

### Step 2: Integrate into Orchestrator

**File**: `agents/orchestrator.py`

```python
from agents.security_assessment_agent import SecurityAssessmentAgent

class Orchestrator:
    def execute(self, rfp_text: str):
        # ... existing code ...
        
        # Add new step
        print("\n🔒 Step 8/8: Performing Security Assessment...")
        security = SecurityAssessmentAgent().run(arch, rfp)
        print("✓ Security Assessment Complete")
        
        # Save output
        self._save("security_assessment.json", security)
```

---

## Prompt Engineering Best Practices

### 1. **Be Specific About Output Format**

❌ **Bad**:
```python
"Analyze this architecture and provide recommendations."
```

✅ **Good**:
```python
"""Analyze this architecture and provide recommendations.

Return ONLY a valid JSON object with this exact structure (no markdown, no code blocks):
{
  "recommendations": [
    {
      "category": "string",
      "recommendation": "string",
      "priority": "High|Medium|Low"
    }
  ]
}"""
```

### 2. **Define the Role Clearly**

❌ **Bad**:
```python
"Analyze this document."
```

✅ **Good**:
```python
"""You are an expert cloud solutions architect with 15 years of experience in 
enterprise infrastructure design. You specialize in AWS, Azure, and GCP 
architectures and have deep knowledge of security, compliance, and cost optimization."""
```

### 3. **Provide Examples (Few-Shot Learning)**

✅ **Good**:
```python
"""Extract requirements from the RFP.

Example input:
"We need a highly available web application supporting 10,000 concurrent users."

Example output:
{
  "functional_requirements": ["Web application hosting", "Session management"],
  "non_functional_requirements": {
    "performance": "Support 10,000 concurrent users",
    "availability": "Highly available (implied 99.9%+)"
  }
}

Now extract from the following RFP:
{rfp_text}"""
```

### 4. **Set Clear Constraints**

✅ **Good**:
```python
"""Generate a proposal document.

Constraints:
- Maximum 3000 words
- Executive-level language (no deep technical jargon)
- Include exactly 3 cost scenarios: Basic, Standard, Premium
- Must include ROI calculation
- Focus on business value, not just technical features"""
```

### 5. **Handle Edge Cases**

✅ **Good**:
```python
"""Extract budget information from the RFP.

If budget is not explicitly mentioned:
- Return "budget": "Not specified"
- Suggest typical budget ranges based on requirements

If only a budget range is given:
- Return both min and max values

If budget is mentioned as "cost-effective" or "budget-conscious":
- Return this as a constraint, not a number"""
```

### 6. **Use Temperature Appropriately**

```python
# Deterministic tasks (extraction, parsing)
temperature=0.0-0.3  # Examples: RFP analysis, code generation

# Balanced tasks (architecture design)
temperature=0.4-0.6  # Examples: Solution design, technical decisions

# Creative tasks (writing, brainstorming)
temperature=0.7-1.0  # Examples: Proposal writing, marketing content
```

---

## Common Customization Scenarios

### Scenario 1: Add Multi-Language Support

**Goal**: Generate proposals in different languages

```python
class ProposalAgent:
    def run(self, rfp_analysis: dict, architecture: dict, cost: dict, language: str = "English") -> str:
        """Generate proposal in specified language"""
        
        system_prompt = f"""You are a pre-sales consultant creating a professional cloud solution proposal.

IMPORTANT: Generate the entire proposal in {language}.

Generate a comprehensive, executive-level proposal document in Markdown format.
[... rest of prompt ...]

All section headings, content, tables, and conclusions must be in {language}."""

        # ... rest of implementation
```

### Scenario 2: Industry-Specific Customization

**Goal**: Tailor architecture for specific industries

```python
class ArchitectureAgent:
    def __init__(self, industry: str = "general"):
        self.industry = industry
        self.use_ai = config.ai_enabled
    
    def _get_industry_specific_prompt(self) -> str:
        """Get industry-specific requirements"""
        
        industry_requirements = {
            "healthcare": """
Additional requirements for healthcare:
- HIPAA compliance mandatory
- PHI data encryption at rest and in transit
- Audit logging for all data access
- BAA (Business Associate Agreement) considerations
""",
            "finance": """
Additional requirements for financial services:
- PCI DSS compliance if handling payments
- SOX compliance for financial data
- Strong authentication (MFA required)
- Real-time fraud detection capabilities
""",
            "government": """
Additional requirements for government:
- FedRAMP compliance
- Data residency requirements (must stay in specified regions)
- Enhanced security controls (FIPS 140-2)
- No data transfer to non-approved countries
"""
        }
        
        return industry_requirements.get(self.industry, "")
    
    def _design_with_ai(self, rfp_analysis: dict) -> dict:
        base_prompt = """You are a cloud solutions architect..."""
        
        industry_prompt = self._get_industry_specific_prompt()
        
        system_prompt = base_prompt + "\n\n" + industry_prompt
        
        # ... rest of implementation
```

### Scenario 3: Cost Optimization Focus

**Goal**: Generate cost-optimized architectures

```python
class ArchitectureAgent:
    def run(self, rfp_analysis: dict, cost_focus: bool = False) -> dict:
        """Design architecture with optional cost optimization focus"""
        
        if cost_focus:
            cost_guidance = """
COST OPTIMIZATION PRIORITY:
- Prefer serverless over always-on infrastructure
- Use spot instances where possible
- Implement auto-scaling aggressively
- Recommend reserved instances for stable workloads
- Suggest storage lifecycle policies
- Consider multi-tenant architectures
- Evaluate open-source alternatives to expensive managed services

Balance cost with the non-functional requirements, but prioritize cost savings when multiple options exist.
"""
            system_prompt = base_system_prompt + "\n\n" + cost_guidance
        
        # ... rest of implementation
```

### Scenario 4: Add Detailed Logging

**Goal**: Track AI usage and responses for analysis

```python
import logging
from datetime import datetime
from pathlib import Path

class AuditedAIClient:
    """AI Client wrapper with detailed logging"""
    
    def __init__(self):
        self.ai_client = ai_client
        self.setup_logging()
    
    def setup_logging(self):
        """Setup audit logging"""
        Path("logs").mkdir(exist_ok=True)
        logging.basicConfig(
            filename=f'logs/ai_calls_{datetime.now().strftime("%Y%m%d")}.log',
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def analyze_with_prompt(self, system_prompt: str, user_content: str, temperature: float = None) -> str:
        """Audited AI call"""
        
        # Log the request
        self.logger.info(f"""
AI Call Started
Temperature: {temperature}
System Prompt Length: {len(system_prompt)}
User Content Length: {len(user_content)}
System Prompt: {system_prompt[:200]}...
""")
        
        try:
            # Make the AI call
            start_time = datetime.now()
            response = self.ai_client.analyze_with_prompt(system_prompt, user_content, temperature)
            duration = (datetime.now() - start_time).total_seconds()
            
            # Log the response
            self.logger.info(f"""
AI Call Completed
Duration: {duration}s
Response Length: {len(response)}
Response Preview: {response[:200]}...
""")
            
            return response
            
        except Exception as e:
            self.logger.error(f"AI Call Failed: {str(e)}")
            raise
```

---

## Testing & Validation

### Test Your Prompts

**File**: `tests/test_prompts.py`

```python
import unittest
import json
from agents.rfp_analysis_agent import RFPAnalysisAgent

class TestPrompts(unittest.TestCase):
    
    def test_rfp_analysis_output_format(self):
        """Test that RFP analysis returns valid JSON"""
        
        sample_rfp = """
        Our organization needs a cloud infrastructure to support 
        a web application with 10,000 users. We require 99.9% uptime,
        ISO 27001 compliance, and low latency (<100ms).
        """
        
        agent = RFPAnalysisAgent()
        result = agent.run(sample_rfp)
        
        # Validate structure
        self.assertIn('business_goals', result)
        self.assertIn('functional_requirements', result)
        self.assertIn('non_functional_requirements', result)
        
        # Validate types
        self.assertIsInstance(result['business_goals'], list)
        self.assertIsInstance(result['functional_requirements'], list)
        
        # Validate content extraction
        nfr = result['non_functional_requirements']
        self.assertIn('99.9%', str(nfr.get('availability', '')))
        self.assertIn('ISO 27001', str(nfr.get('compliance', [])))
    
    def test_prompt_consistency(self):
        """Test that same input produces similar outputs"""
        
        sample_rfp = "We need a scalable web application."
        
        agent = RFPAnalysisAgent()
        
        # Run multiple times (with low temperature for consistency)
        results = [agent.run(sample_rfp) for _ in range(3)]
        
        # Check that key fields are consistent
        for result in results:
            self.assertIn('scalability', ' '.join(result['business_goals']).lower())

if __name__ == '__main__':
    unittest.main()
```

### Validate JSON Output

```python
def validate_json_response(response: str, expected_keys: list) -> dict:
    """Validate and clean JSON response from AI"""
    
    # Clean markdown code blocks
    response = response.strip()
    if response.startswith("```json"):
        response = response[7:]
    elif response.startswith("```"):
        response = response[3:]
    if response.endswith("```"):
        response = response[:-3]
    response = response.strip()
    
    # Parse JSON
    try:
        data = json.loads(response)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON response: {e}\nResponse: {response[:200]}")
    
    # Validate required keys
    missing_keys = [key for key in expected_keys if key not in data]
    if missing_keys:
        raise ValueError(f"Missing required keys: {missing_keys}")
    
    return data
```

---

## 🎓 Advanced Techniques

### Chain-of-Thought Prompting

For complex reasoning tasks:

```python
system_prompt = """You are a cloud cost optimization expert.

Use this step-by-step reasoning process:

1. ANALYZE: Review the architecture components
2. IDENTIFY: Find cost-intensive components
3. EVALUATE: Consider alternatives for each component
4. CALCULATE: Estimate savings for each alternative
5. RECOMMEND: Prioritize recommendations by ROI

For each step, show your reasoning before the final recommendation.

Output format:
{
  "analysis": "Your analysis here",
  "cost_hotspots": [...],
  "alternatives_evaluated": [...],
  "recommendations": [...]
}"""
```

### Retrieval-Augmented Generation (RAG)

Enhance prompts with external knowledge:

```python
def get_cloud_best_practices() -> str:
    """Load cloud best practices from knowledge base"""
    # In production, this would query a vector database
    return """
AWS Well-Architected Framework principles:
1. Operational Excellence
2. Security
3. Reliability
4. Performance Efficiency
5. Cost Optimization
6. Sustainability
"""

system_prompt = f"""You are a cloud solutions architect.

Use these best practices as guidance:
{get_cloud_best_practices()}

Now design an architecture for the following requirements:
[...]
"""
```

---

## 📊 Monitoring & Analytics

### Track Prompt Performance

```python
class PromptMetrics:
    """Track prompt effectiveness"""
    
    def __init__(self):
        self.metrics = []
    
    def log_prompt_call(self, agent_name: str, duration: float, tokens_used: int, success: bool):
        """Log metrics for each prompt call"""
        self.metrics.append({
            "timestamp": datetime.now().isoformat(),
            "agent": agent_name,
            "duration_seconds": duration,
            "tokens_used": tokens_used,
            "success": success
        })
    
    def get_summary(self) -> dict:
        """Get summary statistics"""
        successful = [m for m in self.metrics if m['success']]
        
        return {
            "total_calls": len(self.metrics),
            "successful_calls": len(successful),
            "success_rate": len(successful) / len(self.metrics) if self.metrics else 0,
            "avg_duration": sum(m['duration_seconds'] for m in successful) / len(successful) if successful else 0,
            "total_tokens": sum(m['tokens_used'] for m in successful)
        }
```

---

## 🔗 Resources

- **OpenAI Prompt Engineering Guide**: https://platform.openai.com/docs/guides/prompt-engineering
- **Azure OpenAI Best Practices**: https://learn.microsoft.com/azure/ai-services/openai/
- **Prompt Engineering Tips**: https://www.promptingguide.ai/

---

**Guide Version**: 1.0  
**Last Updated**: December 2024  
**System**: Agentic Pre-Sales POC
