# 🤖 Agentic AI Pre-Sales Infrastructure - Complete Prompts Documentation

## 📋 Overview

This document provides a comprehensive reference for all AI prompts used in the Agentic Pre-Sales POC system. The system uses **4 AI-powered agents** with carefully crafted prompts to transform RFP documents into complete solution proposals.

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    AI INTEGRATION FLOW                          │
└─────────────────────────────────────────────────────────────────┘

     📄 PDF/TXT Input
          │
          ▼
   [RFP Analysis Agent]  ────► AI Prompt #1: Extract Requirements
          │
          ▼
   [Architecture Agent]  ────► AI Prompt #2: Design Architecture
          │
          ▼
   [Proposal Agent]      ────► AI Prompt #3: Generate Proposal
          │
          ▼
   [AI Diagram Agent]    ────► AI Prompt #4: Generate Python Code
          │
          ▼
   📊 Complete Solution Package
```

---

## 🔧 Configuration & Setup

### Environment Variables (.env file)

```bash
# AI Provider Selection
AI_PROVIDER=openai              # Options: openai, azure, github
ENABLE_AI=true                  # Enable/disable AI features

# OpenAI Configuration
OPENAI_API_KEY=sk-proj-...     # Your OpenAI API key
OPENAI_MODEL=gpt-4o-mini       # Model: gpt-4o, gpt-4o-mini, gpt-4-turbo
OPENAI_TEMPERATURE=0.7         # Default temperature (0.0-2.0)
MAX_TOKENS=4000                # Maximum response tokens

# Azure OpenAI Configuration (if using Azure)
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your-azure-key
AZURE_OPENAI_DEPLOYMENT=gpt-4o
AZURE_OPENAI_API_VERSION=2024-02-15-preview

# GitHub Models Configuration (if using GitHub)
GITHUB_TOKEN=ghp_...
GITHUB_MODEL=gpt-4o

# SSL Configuration (for corporate environments)
DISABLE_SSL_VERIFY=false       # Set to true only if needed
```

### Python Configuration (config/ai_config.py)

```python
class AIConfig:
    """
    Centralized AI configuration manager
    - Loads .env file
    - Validates API keys
    - Provides configuration properties
    - Supports multiple providers (OpenAI, Azure, GitHub)
    """
    
    @property
    def ai_enabled(self) -> bool:
        return os.getenv('ENABLE_AI', 'true').lower() == 'true'
    
    @property
    def provider(self) -> str:
        return os.getenv('AI_PROVIDER', 'openai')
```

---

## 📝 AI PROMPT #1: RFP Analysis Agent

### **Purpose**: Extract structured requirements from raw RFP text

### **File**: `agents/rfp_analysis_agent.py`

### **System Prompt**:
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

### **Temperature**: `0.3` (Deterministic for consistency)

### **Input**: Raw RFP text (from PDF or TXT file)

### **Output**: Structured JSON with:
- Business goals
- Functional requirements
- Non-functional requirements (performance, security, availability, compliance)
- Constraints
- Assumptions
- Risks

### **Error Handling**: Falls back to static template if AI fails

### **Example Usage**:
```python
rfp_agent = RFPAnalysisAgent()
rfp_analysis = rfp_agent.run(rfp_text)
# Returns: {"business_goals": [...], "functional_requirements": [...], ...}
```

---

## 🏛️ AI PROMPT #2: Architecture Design Agent

### **Purpose**: Design cloud-agnostic logical architecture

### **File**: `agents/architecture_agent.py`

### **System Prompt**:
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

### **Temperature**: `0.4` (Balanced creativity and consistency)

### **Input**: RFP analysis JSON (from Agent #1)

### **User Prompt Context**:
```
RFP Analysis:
{rfp_analysis_json}

Design the architecture based on these requirements.
```

### **Output**: Architecture specification with:
- Layered architecture (Presentation, Application, Data, etc.)
- Components per layer
- Data flow definitions
- Security controls
- Scalability approach
- Disaster recovery strategy (RPO, RTO)

### **Example Usage**:
```python
arch_agent = ArchitectureAgent()
architecture = arch_agent.run(rfp_analysis)
# Returns: {"layers": [...], "data_flow": [...], "security_controls": [...], ...}
```

---

## 📄 AI PROMPT #3: Proposal Generation Agent

### **Purpose**: Generate executive-level proposal document

### **File**: `agents/proposal_agent.py`

### **System Prompt**:
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

### **Temperature**: `0.5` (Moderate creativity for professional writing)

### **Input**: Combined context from:
- RFP analysis
- Architecture design
- Cost estimate

### **User Prompt Context**:
```
RFP Analysis:
{rfp_analysis_json}

Architecture:
{architecture_json}

Cost Estimate:
{cost_json}

Generate a compelling proposal based on this information.
```

### **Output**: Complete Markdown document with:
- Executive Summary
- Business objectives alignment
- Architectural overview
- Component details
- Security and compliance
- Cost breakdown tables
- Risk mitigation strategies
- Implementation timeline
- Professional formatting

### **Example Output Structure**:
```markdown
# Cloud Solution Proposal

## Executive Summary
[AI-generated executive summary]

## Business Objectives
[Alignment with RFP goals]

## Proposed Architecture
[Technical overview]

## Cost Breakdown
| Service | Monthly Cost | Annual Cost |
|---------|-------------|-------------|
| ...     | ...         | ...         |

## Next Steps
[Action items and timeline]
```

---

## 🎨 AI PROMPT #4: Python Diagrams Code Generator

### **Purpose**: Generate executable Python code for architecture diagrams

### **File**: `agents/ai_diagram_agent.py`

### **System Prompt**:
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

### **Temperature**: `0.3` (Precise code generation)

### **Input**: 
- Architecture specification
- Cloud mapping (AWS/Azure/GCP)

### **User Prompt Context**:
```
Architecture:
{architecture_json}

Cloud Mapping ({cloud_provider}):
{cloud_mapping_json}

Generate Python diagrams code for this architecture using {cloud_provider} icons.
```

### **Output**: Executable Python code using the `diagrams` library

### **Example Generated Code**:
```python
from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import EC2, Lambda
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB, VPC
from diagrams.aws.storage import S3

with Diagram("AWS Cloud Architecture", show=False, filename="architecture"):
    with Cluster("VPC"):
        with Cluster("Public Subnet"):
            lb = ELB("Load Balancer")
        
        with Cluster("Private Subnet"):
            web = [EC2("Web Server 1"), EC2("Web Server 2")]
            db = RDS("Database")
    
    lb >> Edge(label="HTTPS") >> web
    web >> Edge(label="SQL") >> db
```

---

## 🔄 Complete Workflow Example

### Step-by-Step AI Integration:

```python
# 1. Initialize system
from agents.orchestrator import Orchestrator
from utils.pdf_reader import read_rfp

# 2. Read RFP document
rfp_text = read_rfp("sample_input/MMI Cloud Requirements.pdf")

# 3. Initialize orchestrator
orchestrator = Orchestrator(target_cloud="AWS")

# 4. Execute full workflow (calls all 4 AI agents)
orchestrator.execute(rfp_text)

# Behind the scenes:
# - Agent #1: AI extracts requirements → rfp_analysis.json
# - Agent #2: AI designs architecture → architecture.json
# - Agent #3: AI generates proposal → proposal.md
# - Agent #4: AI generates diagram code → generate_python_diagram.py
```

### Output Files:
```
output/
├── rfp_analysis.json              # AI-extracted requirements
├── architecture.json              # AI-designed architecture
├── cost.json                      # Cost calculations
├── proposal.md                    # AI-generated proposal
├── generate_python_diagram.py     # AI-generated diagram code
├── architecture.drawio            # Draw.io diagram
└── architecture.png               # Generated architecture image
```

---

## 🎯 AI Client Implementation

### **File**: `utils/ai_client.py`

### **Core Methods**:

```python
class AIClient:
    def chat_completion(self, messages: list, temperature: float = None, max_tokens: int = None) -> str:
        """
        Low-level API call to AI provider
        
        Args:
            messages: [{"role": "system", "content": "..."}, {"role": "user", "content": "..."}]
            temperature: 0.0-2.0 (lower = more deterministic)
            max_tokens: Maximum response length
        
        Returns:
            Generated text response
        """
        
    def analyze_with_prompt(self, system_prompt: str, user_content: str, temperature: float = None) -> str:
        """
        High-level analysis method
        
        Args:
            system_prompt: Instructions for the AI (role, format, requirements)
            user_content: Content to analyze (RFP text, architecture JSON, etc.)
            temperature: Optional temperature override
        
        Returns:
            Analysis result (JSON or Markdown)
        """
```

### **Provider Support**:
- ✅ OpenAI (GPT-4o, GPT-4o-mini, GPT-4-turbo)
- ✅ Azure OpenAI
- ✅ GitHub Models

### **Error Handling**:
```python
try:
    response = ai_client.analyze_with_prompt(system_prompt, user_content)
except Exception as e:
    print(f"⚠️ AI failed: {e}")
    # Fall back to static template
    return static_fallback()
```

---

## 📊 Temperature Settings Guide

| Agent | Temperature | Reasoning |
|-------|-------------|-----------|
| RFP Analysis | 0.3 | Deterministic extraction, consistency required |
| Architecture Design | 0.4 | Balanced - structured yet creative |
| Proposal Generation | 0.5 | More creative for professional writing |
| Diagram Code | 0.3 | Precise code generation required |

### Temperature Scale:
- **0.0-0.3**: Deterministic, factual, consistent
- **0.4-0.7**: Balanced creativity and consistency
- **0.8-1.0**: Creative, varied outputs
- **1.0+**: Highly creative (rarely used)

---

## 🛠️ Running the System

### Prerequisites:
```bash
# Install dependencies
pip install -r requirements.txt

# Required packages:
# - openai (AI provider)
# - pydantic (data validation)
# - pyyaml (config files)
# - pypdf (PDF reading)
# - diagrams (architecture diagrams)
# - python-docx (Word document generation)
```

### Execution:
```bash
# Run the complete workflow
python run.py

# The system will:
# 1. Read RFP from sample_input/
# 2. Call 4 AI agents sequentially
# 3. Generate all outputs in output/ folder
# 4. Create diagrams and proposal documents
```

### Sample Output:
```
🚀 Initializing Agentic Pre-Sales POC for AWS

============================================================
AGENTIC PRE-SALES POC - EXECUTION STARTED
============================================================

📋 Step 1/7: Analyzing RFP...
🤖 Using AI to analyze RFP...
✓ AI analysis complete
✓ RFP Analysis Complete

🏗️  Step 2/7: Designing Architecture...
🤖 Using AI to design architecture...
✓ AI architecture design complete
✓ Architecture Design Complete

📄 Step 6/7: Generating Proposal Document...
🤖 Using AI to generate proposal...
✓ AI proposal generation complete
✓ Proposal Document Complete

🐍 Generating Python diagrams code...
🤖 Using AI to generate diagrams code...
✓ AI diagram code generation complete
✓ Python diagrams code generated successfully
```

---

## 🔒 Security Best Practices

### API Key Management:
```bash
# NEVER commit .env to git
echo ".env" >> .gitignore

# Store API keys securely
OPENAI_API_KEY=sk-proj-...  # Keep this secret!

# For production, use environment variables or secret managers
export OPENAI_API_KEY=$(aws secretsmanager get-secret-value --secret-id openai-key)
```

### Corporate Environment (SSL Issues):
```bash
# Only if absolutely necessary
DISABLE_SSL_VERIFY=true

# Better approach: Configure SSL certificates
SSL_CERT_FILE=/path/to/cert.pem
```

---

## 🎓 Customization Guide

### Adding a New AI Agent:

```python
# 1. Create new agent file: agents/my_agent.py
from config.ai_config import config
from utils.ai_client import ai_client

class MyAgent:
    def __init__(self):
        self.use_ai = config.ai_enabled
    
    def run(self, input_data: dict) -> dict:
        if self.use_ai:
            return self._process_with_ai(input_data)
        else:
            return self._process_static(input_data)
    
    def _process_with_ai(self, input_data: dict) -> dict:
        system_prompt = """Your custom prompt here"""
        
        user_content = f"Process this: {input_data}"
        
        response = ai_client.analyze_with_prompt(
            system_prompt, 
            user_content, 
            temperature=0.5
        )
        
        return json.loads(response)
```

### Modifying Prompts:

```python
# Best practices for prompt engineering:

# 1. Be specific about output format
"Return ONLY a valid JSON object with this exact structure..."

# 2. Define the role clearly
"You are an expert cloud solutions architect..."

# 3. Provide examples when needed
"Example: {'key': 'value', ...}"

# 4. Set expectations
"Be comprehensive, professional, and technically sound."

# 5. Specify constraints
"No markdown code blocks, no explanations, just JSON."
```

---

## 📈 Performance Optimization

### Token Usage Optimization:
```python
# Use appropriate max_tokens
max_tokens=4000  # For large responses (proposals)
max_tokens=2000  # For structured data (JSON)

# Summarize large inputs if needed
summary = summarize_rfp(rfp_text)  # Custom summarization
response = ai_client.analyze_with_prompt(prompt, summary)
```

### Caching Strategy:
```python
# Cache AI responses to avoid redundant calls
import json
from pathlib import Path

def get_or_generate(cache_file: str, generator_func, *args):
    if Path(cache_file).exists():
        return json.loads(Path(cache_file).read_text())
    
    result = generator_func(*args)
    Path(cache_file).write_text(json.dumps(result, indent=2))
    return result

# Usage
rfp_analysis = get_or_generate(
    "output/rfp_analysis.json",
    rfp_agent.run,
    rfp_text
)
```

---

## 🐛 Troubleshooting

### Common Issues:

1. **API Key Not Working**:
   ```bash
   # Check .env file exists
   ls -la .env
   
   # Verify key is loaded
   python -c "from config.ai_config import config; print(config.openai_api_key[:10])"
   ```

2. **SSL Certificate Errors**:
   ```bash
   # Corporate environments often have this issue
   DISABLE_SSL_VERIFY=true  # Temporary fix
   ```

3. **JSON Parsing Errors**:
   ```python
   # AI sometimes returns markdown-wrapped JSON
   # The system automatically cleans this:
   response = response.strip()
   if response.startswith("```json"):
       response = response[7:]
   if response.endswith("```"):
       response = response[:-3]
   ```

4. **Rate Limiting**:
   ```python
   # Add retry logic
   import time
   from tenacity import retry, stop_after_attempt, wait_exponential
   
   @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=10))
   def call_ai_with_retry(prompt, content):
       return ai_client.analyze_with_prompt(prompt, content)
   ```

---

## 📚 Additional Resources

### Documentation:
- **OpenAI API**: https://platform.openai.com/docs
- **Diagrams Library**: https://diagrams.mingrammer.com/
- **Python-DOCX**: https://python-docx.readthedocs.io/

### Project Files:
- `AI_INTEGRATION_EXPLAINED.md` - Detailed AI integration guide
- `run.py` - Main entry point
- `agents/orchestrator.py` - Workflow coordinator
- `config/ai_config.py` - Configuration manager

---

## 🎯 Summary

This agentic AI system demonstrates:

✅ **4 AI-Powered Agents**: RFP Analysis, Architecture Design, Proposal Generation, Diagram Code Generation

✅ **Multiple AI Providers**: OpenAI, Azure OpenAI, GitHub Models

✅ **Robust Error Handling**: Fallback to static templates if AI fails

✅ **Professional Output**: JSON structures, Markdown proposals, executable Python code

✅ **Production-Ready**: Configurable, secure, maintainable

---

**Created**: December 2024  
**Version**: 1.0  
**System**: Agentic Pre-Sales POC  
**Author**: AI-Assisted Development

