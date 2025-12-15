# RFP Agentic Platform - Stages 1-5

## End-to-End RFP Automation: From Compliance to Proposal

**Complete presales automation platform** that transforms RFP documents into bid-ready artifacts using AI agents.

---

## 🎯 What This Platform Does

Automates the entire RFP response process through 5 intelligent stages:

```
RFP Document → [5 AI Stages] → Complete Proposal Package
```

### Stage Breakdown

| Stage | Name | Output |
|-------|------|--------|
| **1** | Compliance & Requirements | Requirements matrix, risks, strategy |
| **2** | Architecture Mapping | Cloud services, patterns, compliance |
| **3** | Diagram Generation | draw.io architecture diagrams |
| **4** | Cost Estimation | Budget breakdown with ranges |
| **5** | Proposal Generation | Executive-ready documents |

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Your Environment

**Option A: Use OpenAI (Recommended for Getting Started)**
```bash
# Set your OpenAI API key
export OPENAI_API_KEY="your-key-here"
```

**Option B: Use Azure OpenAI**
```bash
export AZURE_OPENAI_KEY="your-key"
export AZURE_OPENAI_ENDPOINT="https://your-endpoint.openai.azure.com/"
export AZURE_OPENAI_DEPLOYMENT="gpt-4o-mini"
```

### 3. Configure Cloud Provider

Edit `config.yaml`:
```yaml
cloud:
  provider: "azure"  # Options: azure, aws, gcp
  region: "eastus"

scale: "medium"  # Options: small, medium, large, enterprise
```

### 4. Run the Complete Pipeline

```bash
python main.py "path/to/your/rfp.pdf"
```

---

## 📦 Generated Artifacts

### Stage 1: Compliance & Requirements
- `output/compliance_matrix.csv` - Detailed requirements tracking
- `output/strategy_brief.md` - Response strategy
- `output/stage1_full_report.json` - Complete analysis data

### Stage 2: Architecture Mapping
- `stage2_architecture/architecture_mappings.json` - Service mappings
- `stage2_architecture/architecture_mappings.csv` - CSV format

### Stage 3: Diagrams
- `stage3_diagrams/azure_architecture.drawio.xml` - **Import to diagrams.net**
- `stage3_diagrams/architecture_summary.md` - Diagram documentation

### Stage 4: Cost Estimation
- `stage4_costing/cost_estimate.json` - Detailed cost data
- `stage4_costing/cost_breakdown.csv` - Service costs
- `stage4_costing/cost_summary.md` - Executive summary

### Stage 5: Proposal Pack (Bid-Ready)
- `stage5_proposal/MASTER_PROPOSAL.md` - **Start here!**
- `stage5_proposal/executive_summary.md` - 2-3 page executive brief
- `stage5_proposal/technical_proposal.md` - Technical details
- `stage5_proposal/pricing_proposal.md` - Cost breakdown
- `stage5_proposal/risks_and_assumptions.md` - Risk register

---

## 🏗️ Architecture

### Agent-Based Design

```
┌─────────────────────────────────────────────────────────┐
│                   RFPOrchestrator                       │
│                  (Coordinates Pipeline)                 │
└─────────────────────────────────────────────────────────┘
              ↓              ↓              ↓
    ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
    │  Stage 1-2   │  │  Stage 3-4   │  │   Stage 5    │
    │   Agents     │  │   Agents     │  │    Agent     │
    └──────────────┘  └──────────────┘  └──────────────┘
         ↓                  ↓                  ↓
    Requirements      Diagrams &         Proposal
    & Architecture      Costs              Pack
```

### Agents Included

1. **Requirements Agent** - Extracts structured requirements
2. **Evaluation Agent** - Identifies scoring criteria
3. **Risk Agent** - Assesses risks and mitigation
4. **Strategy Agent** - Generates win themes
5. **Architecture Mapping Agent** - Maps to cloud services
6. **Diagram Agent** - Generates architecture diagrams
7. **Costing Agent** - Estimates cloud costs
8. **Proposal Pack Agent** - Creates executive documents

---

## ⚙️ Configuration Guide

### config.yaml Structure

```yaml
# Cloud Provider
cloud:
  provider: "azure"  # azure, aws, or gcp
  region: "eastus"

# Deployment Scale
scale: "medium"  # small, medium, large, enterprise

# Enable/Disable Stages
stages:
  stage1:
    enabled: true
  stage2:
    enabled: true
  stage3:
    enabled: true
  stage4:
    enabled: true
  stage5:
    enabled: true

# LLM Configuration
llm:
  enabled: true
  model: "gpt-4o-mini"
  temperature: 0.1
```

### Switching Cloud Providers

**For AWS:**
```yaml
cloud:
  provider: "aws"
  region: "us-east-1"
```

**For GCP:**
```yaml
cloud:
  provider: "gcp"
  region: "us-central1"
```

The system automatically maps to appropriate services for each provider.

---

## 🎓 Usage Examples

### Run Complete Pipeline (All Stages)

```bash
python main.py my_rfp.pdf
```

### Run Specific Stages Only

Edit `config.yaml` to disable stages:
```yaml
stages:
  stage1:
    enabled: true
  stage2:
    enabled: true
  stage3:
    enabled: false  # Skip diagrams
  stage4:
    enabled: false  # Skip costing
  stage5:
    enabled: false  # Skip proposal
```

### Use Different Scale

```yaml
scale: "enterprise"  # Higher costs, more services
```

---

## 🔧 Advanced Features

### LLM-Enhanced vs Rule-Based

- **With LLM** (API key configured): Intelligent, context-aware analysis
- **Without LLM** (no API key): Fast, deterministic rule-based extraction

The platform automatically falls back to rules if LLM is unavailable.

### Multi-Cloud Support

Supports **Azure**, **AWS**, and **GCP** with automatic service mapping:

| Requirement | Azure | AWS | GCP |
|-------------|-------|-----|-----|
| HA | Azure Front Door | CloudFront | Cloud CDN |
| Compute | Virtual Machines | EC2 | Compute Engine |
| Database | Azure SQL | RDS | Cloud SQL |

---

## 📊 Cost Estimation

### Cost Ranges

Each estimate provides three values:

- **Low**: Conservative estimate (~70% of expected)
- **Expected**: Most likely cost
- **High**: Maximum estimate (~150% of expected)

### Scale Impact

| Scale | Multiplier | Example Monthly Cost |
|-------|-----------|---------------------|
| Small | 0.5x | $600 - $1,500 |
| Medium | 1.0x | $1,200 - $3,000 |
| Large | 2.5x | $3,000 - $7,500 |
| Enterprise | 5.0x | $6,000 - $15,000 |

### Cost Optimization

The platform automatically identifies:
- Reserved instance opportunities (30-50% savings)
- Right-sizing recommendations
- Auto-scaling opportunities
- Storage lifecycle policies

---

## 📐 Diagram Generation

### Using Generated Diagrams

1. Open `stage3_diagrams/azure_architecture.drawio.xml`
2. Go to [diagrams.net](https://app.diagrams.net)
3. Click **File → Open From → Device**
4. Select the `.drawio.xml` file
5. Edit, customize, and export

### Diagram Features

- Services organized by category
- Color-coded compliance levels
- Architecture patterns labeled
- Cloud provider icons (when available)

---

## 🎯 Why This Is Enterprise-Ready

✅ **Agent Isolation** - Each stage is independently testable  
✅ **Cloud-Agnostic** - Switch providers with one config change  
✅ **Deterministic** - JSON → CSV → Documents (auditable)  
✅ **Presales-Friendly** - Executive-ready outputs  
✅ **Demo-Ready** - Works with or without LLM  
✅ **Extensible** - Add new agents or stages easily  

---

## 🛠️ Troubleshooting

### "No LLM configured" Warning

**Solution**: Set one of these environment variables:
```bash
export OPENAI_API_KEY="your-key"
# OR
export AZURE_OPENAI_KEY="your-key"
export AZURE_OPENAI_ENDPOINT="https://your-endpoint.openai.azure.com/"
```

### Import Error: "No module named 'yaml'"

**Solution**:
```bash
pip install pyyaml
```

### Diagram Not Opening

**Solution**: Ensure file extension is `.drawio.xml` and use diagrams.net (not draw.io desktop app).

---

## 📝 Project Structure

```
rfp_stage1_poc/
├── main.py                    # Entry point
├── orchestrator.py            # Pipeline coordinator
├── config.yaml                # Configuration
├── requirements.txt           # Dependencies
│
├── agents/                    # All AI agents
│   ├── requirements_agent.py
│   ├── evaluation_agent.py
│   ├── risk_agent.py
│   ├── strategy_agent.py
│   ├── architecture_mapping_agent.py
│   ├── diagram_agent.py
│   ├── costing_agent.py
│   └── proposal_pack_agent.py
│
├── ingest/                    # Document loading
│   └── document_loader.py
│
├── output/                    # Stage 1 outputs
├── stage2_architecture/       # Stage 2 outputs
├── stage3_diagrams/          # Stage 3 outputs
├── stage4_costing/           # Stage 4 outputs
└── stage5_proposal/          # Stage 5 outputs
```

---

## 🎓 Next Steps

1. **Review Generated Proposal**
   - Start with `stage5_proposal/MASTER_PROPOSAL.md`
   - Review executive summary
   - Validate technical details

2. **Customize Diagrams**
   - Open `.drawio.xml` in diagrams.net
   - Add connections between services
   - Export as PNG/PDF for presentations

3. **Refine Costs**
   - Review `stage4_costing/cost_summary.md`
   - Apply optimization recommendations
   - Add reserved instance pricing

4. **Deliver to Customer**
   - Package all artifacts
   - Include architecture diagram
   - Present executive summary

---

## 📄 License

This is a proof-of-concept for demonstration purposes.

---

## 🤝 Contributing

This platform is designed to be extended. To add a new stage:

1. Create agent in `agents/new_agent.py`
2. Add stage method to `orchestrator.py`
3. Update `config.yaml` with stage settings
4. Update `main.py` to display outputs

---

## 💡 Tips for Best Results

1. **Use LLM for Complex RFPs** - More accurate requirement extraction
2. **Configure Cloud Provider** - Match customer's preferred platform
3. **Set Appropriate Scale** - Impacts architecture and costs
4. **Review Assumptions** - In risks_and_assumptions.md
5. **Validate Compliance** - Check compliance_matrix.csv

---

**Built with ❤️ for presales teams everywhere**

Transform hours of manual work into minutes of automated intelligence.
