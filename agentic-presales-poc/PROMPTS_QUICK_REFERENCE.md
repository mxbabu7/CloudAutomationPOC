# 🚀 Quick Reference: AI Prompts for Agentic Pre-Sales

## 📌 Quick Navigation
- [Prompt #1: RFP Analysis](#prompt-1-rfp-analysis) - Extract requirements
- [Prompt #2: Architecture Design](#prompt-2-architecture-design) - Design solution
- [Prompt #3: Proposal Generation](#prompt-3-proposal-generation) - Create document
- [Prompt #4: Diagram Code](#prompt-4-diagram-code) - Generate diagrams

---

## Prompt #1: RFP Analysis

**Agent**: `agents/rfp_analysis_agent.py`  
**Temperature**: 0.3 (deterministic)  
**Purpose**: Extract structured requirements from RFP

### System Prompt:
```
You are an expert RFP analyst. Analyze the provided RFP document and extract structured information.

Return ONLY a valid JSON object with this exact structure (no markdown, no code blocks, just raw JSON):
{
  "business_goals": ["goal1", "goal2", ...],
  "functional_requirements": ["req1", "req2", ...],
  "non_functional_requirements": {
    "performance": "description",
    "security": "description",
    "availability": "description",
    "compliance": ["standard1", "standard2", ...]
  },
  "constraints": ["constraint1", "constraint2", ...],
  "assumptions": ["assumption1", "assumption2", ...],
  "risks": ["risk1", "risk2", ...]
}

Extract as much detail as possible from the RFP. Be specific and comprehensive.
```

### Usage Example:
```python
from agents.rfp_analysis_agent import RFPAnalysisAgent

agent = RFPAnalysisAgent()
result = agent.run(rfp_text)
```

---

## Prompt #2: Architecture Design

**Agent**: `agents/architecture_agent.py`  
**Temperature**: 0.4 (balanced)  
**Purpose**: Design cloud-agnostic architecture

### System Prompt:
```
You are a cloud solutions architect. Design a cloud-agnostic logical architecture based on the RFP analysis provided.

Return ONLY a valid JSON object with this exact structure (no markdown, no code blocks):
{
  "layers": [
    {
      "name": "Layer Name",
      "components": ["Component1", "Component2"],
      "responsibilities": ["Responsibility1", "Responsibility2"]
    }
  ],
  "data_flow": [
    {
      "from": "Component A",
      "to": "Component B",
      "protocol": "HTTPS"
    }
  ],
  "security_controls": ["Control1", "Control2"],
  "scalability_approach": "Description of scaling strategy",
  "disaster_recovery": {
    "rpo": "Time value",
    "rto": "Time value",
    "strategy": "DR strategy description"
  }
}

Design a comprehensive, production-ready architecture.
```

### User Context:
```
RFP Analysis:
{rfp_analysis_json}

Design the architecture based on these requirements.
```

### Usage Example:
```python
from agents.architecture_agent import ArchitectureAgent

agent = ArchitectureAgent()
architecture = agent.run(rfp_analysis)
```

---

## Prompt #3: Proposal Generation

**Agent**: `agents/proposal_agent.py`  
**Temperature**: 0.5 (creative)  
**Purpose**: Generate professional proposal document

### System Prompt:
```
You are a pre-sales consultant creating a professional cloud solution proposal.

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

Make it professional, persuasive, and technically sound. Use tables where appropriate.
```

### User Context:
```
RFP Analysis:
{rfp_analysis_json}

Architecture:
{architecture_json}

Cost Estimate:
{cost_json}

Generate a compelling proposal based on this information.
```

### Usage Example:
```python
from agents.proposal_agent import ProposalAgent

agent = ProposalAgent()
proposal_md = agent.run(rfp_analysis, architecture, cost)
```

---

## Prompt #4: Diagram Code

**Agent**: `agents/ai_diagram_agent.py`  
**Temperature**: 0.3 (precise)  
**Purpose**: Generate executable Python diagram code

### System Prompt:
```
You are an expert at generating Python code using the 'diagrams' library for AWS/Azure/GCP architecture diagrams.

Generate complete, executable Python code that:
1. Imports necessary components from the diagrams library
2. Creates a professional architecture diagram
3. Uses appropriate cloud provider icons (aws/azure/gcp)
4. Includes clusters for logical grouping
5. Shows data flows with Edge connections
6. Uses proper colors and labels

Return ONLY valid Python code that can be executed directly. No markdown, no explanations, just code.

Use this structure:
```python
from diagrams import Diagram, Cluster, Edge
from diagrams.{provider}.compute import EC2, Lambda
# ... other imports

with Diagram("Architecture Name", show=False, filename="output_architecture"):
    # Create components and clusters
    # Connect with edges
```

Make it production-ready and visually clear.
```

### User Context:
```
Architecture:
{architecture_json}

Cloud Mapping ({cloud_provider}):
{cloud_mapping_json}

Generate Python diagrams code for this architecture using {cloud_provider} icons.
```

### Usage Example:
```python
from agents.ai_diagram_agent import AIDiagramAgent

agent = AIDiagramAgent()
python_code = agent.run(architecture, cloud_mapping)
```

---

## 🎛️ Temperature Guide

| Agent | Temp | Why |
|-------|------|-----|
| RFP Analysis | 0.3 | Consistent extraction |
| Architecture | 0.4 | Balanced design |
| Proposal | 0.5 | Creative writing |
| Diagram Code | 0.3 | Precise code |

---

## 🔧 Configuration (.env)

```bash
# AI Provider
AI_PROVIDER=openai
ENABLE_AI=true

# OpenAI
OPENAI_API_KEY=sk-proj-...
OPENAI_MODEL=gpt-4o-mini
OPENAI_TEMPERATURE=0.7
MAX_TOKENS=4000

# Azure (alternative)
AZURE_OPENAI_ENDPOINT=https://...
AZURE_OPENAI_API_KEY=...
AZURE_OPENAI_DEPLOYMENT=gpt-4o

# GitHub Models (alternative)
GITHUB_TOKEN=ghp_...
GITHUB_MODEL=gpt-4o
```

---

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure .env file
cp .env.example .env
# Edit .env with your API key

# 3. Run the system
python run.py
```

---

## 📊 Output Files

```
output/
├── rfp_analysis.json              # Prompt #1 output
├── architecture.json              # Prompt #2 output
├── proposal.md                    # Prompt #3 output
├── generate_python_diagram.py     # Prompt #4 output
├── cost.json                      # Cost calculations
└── architecture.png               # Generated diagram
```

---

## 🎯 Key Features

✅ **4 Specialized AI Agents**  
✅ **Multiple AI Providers** (OpenAI, Azure, GitHub)  
✅ **Structured JSON Output**  
✅ **Professional Markdown Proposals**  
✅ **Executable Python Code**  
✅ **Fallback Templates** (if AI fails)  
✅ **Corporate SSL Support**  

---

## 📚 Full Documentation

See `AI_PROMPTS_DOCUMENTATION.md` for complete details.

---

**Quick Reference v1.0** | Agentic Pre-Sales POC
