# AI Integration Architecture - Agentic Pre-Sales POC

## 🤖 Overview

The Agentic Pre-Sales POC uses **AI at 4 critical points** in the workflow to transform raw PDF requirements into professional solution documents. This document explains how AI is integrated and where it's used.

---

## 📊 AI Integration Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         AI INTEGRATION LAYERS                        │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│ CONFIGURATION LAYER (.env file)                                     │
│                                                                      │
│ OPENAI_API_KEY=sk-proj-...                                          │
│ OPENAI_MODEL=gpt-4o-mini                                            │
│ AI_PROVIDER=openai  (or azure, github)                              │
│ OPENAI_TEMPERATURE=0.7                                              │
│ ENABLE_AI=true                                                       │
└──────────────────────────┬──────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────────┐
│ AI CONFIG MANAGER (config/ai_config.py)                             │
│                                                                      │
│ - Loads .env file                                                    │
│ - Validates API keys                                                 │
│ - Configures AI provider (OpenAI/Azure/GitHub)                      │
│ - Sets model parameters (temperature, max_tokens)                   │
└──────────────────────────┬──────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────────┐
│ AI CLIENT (utils/ai_client.py)                                      │
│                                                                      │
│ Unified interface for:                                               │
│ ✅ OpenAI (GPT-4o, GPT-4o-mini)                                      │
│ ✅ Azure OpenAI                                                      │
│ ✅ GitHub Models                                                     │
│                                                                      │
│ Methods:                                                             │
│ - chat_completion(messages, temperature, max_tokens)                │
│ - analyze_with_prompt(system_prompt, user_content)                  │
└──────────────────────────┬──────────────────────────────────────────┘
                           │
                           │ Imported by 4 AI-powered agents
                           │
        ┌──────────────────┼──────────────────┬──────────────────┐
        │                  │                  │                  │
        ▼                  ▼                  ▼                  ▼
┌──────────────┐  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐
│ RFP Analysis │  │Architecture │  │  Proposal    │  │  AI Diagram  │
│    Agent     │  │    Agent    │  │    Agent     │  │    Agent     │
│              │  │             │  │              │  │              │
│ AI Call #1   │  │ AI Call #2  │  │ AI Call #3   │  │ AI Call #4   │
└──────────────┘  └─────────────┘  └──────────────┘  └──────────────┘
```

---

## 🔄 AI-Powered Workflow

### **Step-by-Step AI Integration:**

```
1. PDF Input → 2. AI Analysis → 3. AI Design → 4. Logic Processing → 
5. AI Proposal → 6. AI Diagram Code → 7. Output Documents
```

### **Detailed Flow:**

```
┌─────────────────────────────────────────────────────────────────────┐
│ INPUT: MMI Cloud Requirements.pdf (5840 characters)                 │
└────────────────────────┬────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────────┐
│ AI CALL #1: RFP Analysis (rfp_analysis_agent.py)                    │
│                                                                      │
│ Model: GPT-4o-mini                                                   │
│ Temperature: 0.3 (deterministic)                                     │
│                                                                      │
│ System Prompt:                                                       │
│ "You are an expert RFP analyst. Extract structured requirements..."  │
│                                                                      │
│ Input: Full PDF text (5840 chars)                                   │
│                                                                      │
│ AI Processing:                                                       │
│ ├─ Identifies business goals                                        │
│ ├─ Extracts functional requirements                                 │
│ ├─ Analyzes non-functional requirements                             │
│ ├─ Detects constraints and assumptions                              │
│ └─ Identifies risks                                                 │
│                                                                      │
│ Output: rfp_analysis.json                                            │
│ {                                                                    │
│   "business_goals": [                                                │
│     "Modernize the MDP application by migrating it to AWS Cloud",   │
│     "Streamline claims processing and reduce duplicates",            │
│     ...                                                              │
│   ],                                                                 │
│   "functional_requirements": [                                       │
│     "Migrate ETL code from DataStage/Unix to Databricks",           │
│     "Migrate DB2 database objects and data",                        │
│     ...                                                              │
│   ]                                                                  │
│ }                                                                    │
│                                                                      │
│ Tokens Used: ~6,000 tokens                                           │
│ Cost: ~$0.003 (GPT-4o-mini pricing)                                 │
└────────────────────────┬────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────────┐
│ AI CALL #2: Architecture Design (architecture_agent.py)             │
│                                                                      │
│ Model: GPT-4o-mini                                                   │
│ Temperature: 0.5 (balanced creativity)                               │
│                                                                      │
│ System Prompt:                                                       │
│ "You are a cloud solution architect. Design a comprehensive          │
│  architecture with layers, components, data flows..."                │
│                                                                      │
│ Input: rfp_analysis.json (structured requirements)                  │
│                                                                      │
│ AI Processing:                                                       │
│ ├─ Designs architecture layers (Presentation, App, Data, etc.)      │
│ ├─ Selects appropriate components for each layer                    │
│ ├─ Defines data flow between components                             │
│ ├─ Adds security controls                                           │
│ ├─ Plans scalability approach                                       │
│ └─ Designs disaster recovery strategy                               │
│                                                                      │
│ Output: architecture.json                                            │
│ {                                                                    │
│   "layers": [                                                        │
│     {                                                                │
│       "name": "Presentation Layer",                                  │
│       "components": ["Web UI", "Mobile App"],                        │
│       "responsibilities": [...]                                      │
│     },                                                               │
│     {                                                                │
│       "name": "Data Layer",                                          │
│       "components": ["Databricks", "DB2 Migration Tool", ...],       │
│       "responsibilities": ["ETL processing", "Data migration"]       │
│     }                                                                │
│   ],                                                                 │
│   "data_flow": [...],                                                │
│   "security_controls": [...]                                         │
│ }                                                                    │
│                                                                      │
│ Tokens Used: ~4,000 tokens                                           │
│ Cost: ~$0.002                                                        │
└────────────────────────┬────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────────┐
│ NON-AI PROCESSING (Logic-based agents)                              │
│                                                                      │
│ diagram_agent.py:        Converts architecture to diagram spec      │
│ cloud_mapping_agent.py:  Maps to AWS/Azure/GCP services            │
│ cost_agent.py:           Calculates costs from service mappings     │
│ roadmap_agent.py:        Generates static roadmap template          │
│                                                                      │
│ Why no AI here? Deterministic logic is faster and more reliable     │
└────────────────────────┬────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────────┐
│ AI CALL #3: Proposal Generation (proposal_agent.py)                 │
│                                                                      │
│ Model: GPT-4o-mini                                                   │
│ Temperature: 0.7 (creative writing)                                  │
│                                                                      │
│ System Prompt:                                                       │
│ "You are a technical proposal writer. Create a professional          │
│  proposal document in Markdown format..."                            │
│                                                                      │
│ Input: rfp_analysis.json + architecture.json + cost.json            │
│                                                                      │
│ AI Processing:                                                       │
│ ├─ Writes executive summary                                         │
│ ├─ Explains proposed solution                                       │
│ ├─ Details technical approach                                       │
│ ├─ Presents cost breakdown                                          │
│ └─ Adds benefits and value proposition                              │
│                                                                      │
│ Output: proposal.md (Markdown document)                              │
│                                                                      │
│ Tokens Used: ~5,000 tokens                                           │
│ Cost: ~$0.003                                                        │
└────────────────────────┬────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────────┐
│ AI CALL #4: Python Diagram Code (ai_diagram_agent.py)               │
│                                                                      │
│ Model: GPT-4o-mini                                                   │
│ Temperature: 0.3 (code generation needs precision)                   │
│                                                                      │
│ System Prompt:                                                       │
│ "You are an expert at generating Python code using the 'diagrams'    │
│  library. Generate complete, executable code..."                     │
│                                                                      │
│ Input: architecture.json + cloud_mapping (AWS services)             │
│                                                                      │
│ AI Processing:                                                       │
│ ├─ Generates Python imports for AWS icons                           │
│ ├─ Creates Diagram structure with Clusters                          │
│ ├─ Defines components as diagram nodes                              │
│ ├─ Connects components with Edge connections                        │
│ └─ Adds labels, colors, and styling                                 │
│                                                                      │
│ Output: generate_python_diagram.py (Executable Python code)         │
│                                                                      │
│ Tokens Used: ~4,000 tokens                                           │
│ Cost: ~$0.002                                                        │
└────────────────────────┬────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────────┐
│ FINAL OUTPUTS (9 files)                                             │
│                                                                      │
│ ✅ rfp_analysis.json (AI-generated)                                  │
│ ✅ architecture.json (AI-generated)                                  │
│ ✅ diagram.json (Logic-based from architecture)                      │
│ ✅ cost.json (Logic-based calculation)                               │
│ ✅ proposal.md (AI-generated)                                        │
│ ✅ roadmap.json (Static template)                                    │
│ ✅ architecture.drawio (Generated from diagram.json)                 │
│ ✅ generate_python_diagram.py (AI-generated code)                    │
│ ✅ Infrastructure_Solution_Architecture.docx (Word doc)              │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🔧 AI Configuration Details

### **Configuration File (.env):**

```ini
# AI Provider Selection
AI_PROVIDER=openai          # Options: openai, azure, github
ENABLE_AI=true               # Master switch for AI features

# OpenAI Configuration
OPENAI_API_KEY=sk-proj-...  # Your OpenAI API key
OPENAI_MODEL=gpt-4o-mini    # Model selection
OPENAI_TEMPERATURE=0.7      # Creativity level (0.0-2.0)
OPENAI_MAX_TOKENS=4000      # Maximum response length

# Azure OpenAI (Alternative)
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=...
AZURE_OPENAI_DEPLOYMENT=gpt-4
AZURE_OPENAI_API_VERSION=2024-02-15-preview

# GitHub Models (Alternative)
GITHUB_TOKEN=ghp_...
GITHUB_MODEL=gpt-4o
```

### **AI Provider Support:**

| Provider | Endpoint | Models | Status |
|----------|----------|--------|--------|
| **OpenAI** | api.openai.com | GPT-4o, GPT-4o-mini, GPT-4 | ✅ Active |
| **Azure OpenAI** | *.openai.azure.com | GPT-4, GPT-3.5-turbo | ✅ Supported |
| **GitHub Models** | models.inference.ai.azure.com | GPT-4o, Phi-3 | ✅ Supported |

---

## 💡 How AI Enhances Each Step

### **1. RFP Analysis Agent (AI-Powered)**

**What AI Does:**
- Reads unstructured PDF text
- Identifies business goals buried in paragraphs
- Extracts specific requirements (e.g., "1 billion MMI IDs")
- Detects non-functional requirements (performance, security)
- Recognizes constraints and timelines

**Why AI is Needed:**
- PDF text is unstructured (paragraphs, sentences)
- Requires natural language understanding
- Context-aware extraction (understands "Databricks migration" as a requirement)

**Alternative Without AI:**
- Static keyword matching (would miss context)
- Manual extraction (time-consuming)
- Rigid templates (wouldn't adapt to different RFPs)

---

### **2. Architecture Agent (AI-Powered)**

**What AI Does:**
- Designs architecture based on requirements
- Selects appropriate layers (Presentation, Data, Security)
- Chooses components for each layer
- Defines data flows between components
- Adds security controls and scalability strategies

**Why AI is Needed:**
- Creative design requires understanding best practices
- Context-aware decisions (e.g., "1 billion records" → DynamoDB)
- Trade-off analysis (cost vs. performance)

**Alternative Without AI:**
- Static templates (same architecture for every RFP)
- Manual architecture design (requires senior architect)
- Rule-based systems (too rigid, can't adapt)

---

### **3. Proposal Agent (AI-Powered)**

**What AI Does:**
- Writes professional proposal in natural language
- Explains technical concepts in business terms
- Creates executive summary for decision-makers
- Connects requirements to proposed solution
- Adds value propositions and benefits

**Why AI is Needed:**
- Natural language generation (fluent, professional writing)
- Context synthesis (combines RFP + architecture + costs)
- Audience adaptation (technical + executive content)

**Alternative Without AI:**
- Template-based proposals (generic, not tailored)
- Manual writing (time-consuming, 2-3 hours per proposal)
- Markdown templates (lacks customization)

---

### **4. AI Diagram Agent (AI-Powered)**

**What AI Does:**
- Generates executable Python code (diagrams library)
- Selects appropriate AWS icons for each component
- Creates logical groupings (Clusters)
- Defines connections with proper labels
- Applies best practices for diagram layout

**Why AI is Needed:**
- Code generation requires understanding of:
  - Python syntax
  - Diagrams library API
  - AWS service mappings
  - Visual layout best practices

**Alternative Without AI:**
- Static code templates (basic diagrams only)
- Manual coding (requires Python + diagrams expertise)
- Hardcoded diagrams (not adaptable to different architectures)

---

## 📊 AI Usage Statistics

### **Per Execution:**

| Metric | Value |
|--------|-------|
| Total AI Calls | 4 |
| Total Tokens | ~19,000 tokens |
| Total Cost | ~$0.01 (GPT-4o-mini) |
| Total Time | ~15-30 seconds |
| AI Processing | ~10 seconds |
| Network I/O | ~5-20 seconds |

### **Cost Breakdown:**

| AI Call | Tokens | Cost (GPT-4o-mini) |
|---------|--------|-------------------|
| RFP Analysis | ~6,000 | $0.003 |
| Architecture Design | ~4,000 | $0.002 |
| Proposal Generation | ~5,000 | $0.003 |
| Diagram Code | ~4,000 | $0.002 |
| **Total** | **~19,000** | **~$0.01** |

**Annual Cost (100 RFPs):** ~$1.00 💰

---

## 🔒 Graceful Fallback System

### **What Happens if AI Fails?**

Each AI-powered agent has a **static fallback**:

```python
def run(self, input_data):
    if self.use_ai:
        try:
            return self._generate_with_ai(input_data)
        except Exception as e:
            print(f"⚠️ AI failed: {e}")
            print("⚠️ Falling back to static template")
            return self._generate_static(input_data)
    else:
        return self._generate_static(input_data)
```

### **Fallback Behavior:**

| Agent | AI Fails | Fallback Action |
|-------|----------|-----------------|
| RFP Analysis | Returns generic requirements template | Basic goals + requirements |
| Architecture | Returns standard 3-tier architecture | Generic layers, no customization |
| Proposal | Returns template proposal | Standard sections, placeholder text |
| Diagram Code | Returns basic diagram code | Simple 6-component diagram |

**Result:** System **never crashes**, always produces output (even if basic)

---

## 🎯 AI Integration Benefits

### **1. Speed**
- AI generates in **10 seconds** what takes humans **2-3 hours**
- Instant analysis of 5,000+ character PDFs
- Automatic architecture design

### **2. Quality**
- Consistent, professional output
- No human errors or omissions
- Best practices built-in

### **3. Customization**
- Tailored to each specific RFP
- Adapts to different requirements
- Context-aware decisions

### **4. Scalability**
- Process 100s of RFPs without fatigue
- Parallel processing possible
- No quality degradation at scale

### **5. Cost-Effectiveness**
- $0.01 per RFP vs. $200-500 human cost
- 99.5% cost reduction
- ROI positive after 1st use

---

## 🔄 Orchestrator's Role

The **orchestrator** doesn't call AI directly—it:

1. **Coordinates** the 7 specialized agents
2. **Passes data** between agents sequentially
3. **Manages** error handling and fallbacks
4. **Generates** final output files

**Why this architecture?**
- **Separation of concerns** - Each agent has one job
- **Testability** - Each agent can be tested independently
- **Maintainability** - Easy to update/replace individual agents
- **Reusability** - Agents can be used in different workflows

---

## 🚀 Advanced AI Features

### **Temperature Control:**

```python
# RFP Analysis: Low temperature (0.3) - Deterministic
ai_client.analyze_with_prompt(system_prompt, rfp_text, temperature=0.3)

# Architecture: Medium (0.5) - Balanced
ai_client.analyze_with_prompt(system_prompt, context, temperature=0.5)

# Proposal: High (0.7) - Creative writing
ai_client.analyze_with_prompt(system_prompt, context, temperature=0.7)
```

**Why different temperatures?**
- **Low (0.3):** Factual extraction (RFP analysis)
- **Medium (0.5):** Balanced creativity (architecture design)
- **High (0.7):** Natural language writing (proposals)

### **JSON Response Cleaning:**

AI sometimes returns:
```
```json
{
  "data": "value"
}
```
```

Code automatically cleans:
```python
if response.startswith("```json"):
    response = response[7:]
if response.endswith("```"):
    response = response[:-3]
```

---

## 📚 Summary

### **AI Integration Points:**

1. ✅ **Configuration** - `.env` → `ai_config.py`
2. ✅ **Client** - `ai_client.py` (unified interface)
3. ✅ **Agents** - 4 AI-powered agents
4. ✅ **Fallbacks** - Graceful degradation to static templates

### **Key Benefits:**

- 🚀 **Speed:** 10 seconds vs. 2-3 hours
- 💰 **Cost:** $0.01 vs. $200-500 per RFP
- 📊 **Quality:** Consistent, professional outputs
- 🔄 **Scalability:** 100s of RFPs without degradation

### **Architecture Principles:**

- **Modular** - Each agent is independent
- **Flexible** - Supports multiple AI providers
- **Resilient** - Graceful fallbacks if AI fails
- **Configurable** - Easy to adjust via .env file

**The AI integration is the core intelligence of the system, transforming raw PDFs into professional solution documents automatically.**
