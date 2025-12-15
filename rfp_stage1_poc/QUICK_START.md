# Quick Start Guide - RFP Stage 1 POC

## ⚡ 5-Minute Quick Start

### Step 1: Navigate to Project
```bash
cd c:\Users\258211\GitLocalWS\rfp_stage1_poc
```

### Step 2: Run the POC
```bash
c:\Users\258211\GitLocalWS\agentic-presales-poc\testenv\Scripts\python.exe main.py
```

### Step 3: Check Outputs
```bash
dir output\
# View:
# - compliance_matrix.csv
# - strategy_brief.md
# - stage1_full_report.json
```

---

## 📂 File Structure

```
rfp_stage1_poc/
├── main.py                      ⭐ START HERE
├── orchestrator.py              # Coordinates all agents
├── requirements.txt             # Dependencies
├── sample_rfp.txt              # Test RFP document
├── README.md                    # Full documentation
├── EXECUTION_SUMMARY.md         # Detailed results
├── .env.example                 # LLM configuration template
│
├── ingest/
│   ├── __init__.py
│   └── document_loader.py       # Load TXT/PDF/DOCX
│
├── agents/
│   ├── __init__.py
│   ├── requirements_agent.py    # Extract requirements
│   ├── evaluation_agent.py      # Extract criteria
│   ├── risk_agent.py           # Identify risks
│   └── strategy_agent.py       # Generate strategy
│
└── output/
    ├── compliance_matrix.csv    # ✅ Generated
    ├── strategy_brief.md        # ✅ Generated
    └── stage1_full_report.json  # ✅ Generated
```

---

## 🎯 What Gets Generated

### 1. Compliance Matrix (CSV)
- All requirements with unique IDs
- Section traceability
- Type (Mandatory/Optional)
- Ready for Excel import

### 2. Strategy Brief (Markdown)
- Executive summary
- Key themes
- Risk mitigation
- Timeline recommendations

### 3. Full Report (JSON)
- Complete structured data
- Machine-readable format
- Ready for integration

---

## 🔧 Common Commands

### Run with Sample RFP
```bash
python main.py
```

### Run with Your RFP
```bash
python main.py path/to/your/rfp.txt
```

### Install Dependencies (if needed)
```bash
pip install -r requirements.txt
```

---

## 💡 Key Features

✅ **Works Immediately** - No API keys required  
✅ **LLM-Ready** - Upgrade to OpenAI/Azure anytime  
✅ **Multi-Format** - Supports TXT, PDF, DOCX  
✅ **Professional Output** - CSV + Markdown + JSON  
✅ **Production-Ready** - Clean, documented code  

---

## 🚀 Upgrade to LLM

### For Better Extraction Quality:

**OpenAI:**
```bash
export OPENAI_API_KEY='sk-...'
python main.py
```

**Azure OpenAI:**
```bash
export AZURE_OPENAI_KEY='your-key'
export AZURE_OPENAI_ENDPOINT='https://your-resource.openai.azure.com'
python main.py
```

---

## 📊 Example Output

```
============================================================
RFP STAGE 1 SUMMARY
============================================================

Requirements:
  - Total: 29
  - Mandatory: 23
  - Optional: 6

Evaluation Criteria: 4
  - Technical Solution: 40%
  - Financial Proposal: 30%
  - Experience & Qualifications: 20%

Risks: 4
  - High: 3
  - Medium: 1

✅ Stage 1 processing completed successfully!
```

---

## 🎓 Agent Flow

```
RFP Document
    ↓
Document Loader (ingest/)
    ↓
Orchestrator
    ↓
┌───────────────────────────────────┐
│  Requirements Agent → 29 items    │
│  Evaluation Agent → 4 criteria    │
│  Risk Agent → 4 risks             │
│  Strategy Agent → Brief           │
└───────────────────────────────────┘
    ↓
Output Files (CSV + MD + JSON)
```

---

## ✅ Production-Ready Checklist

- [x] Deterministic outputs
- [x] Section traceability
- [x] Modular architecture
- [x] Error handling
- [x] LLM-agnostic design
- [x] Professional documentation
- [x] Sample RFP included
- [x] Multiple output formats

---

## 📞 Need Help?

1. **Full Documentation:** See `README.md`
2. **Detailed Results:** See `EXECUTION_SUMMARY.md`
3. **Code Examples:** Check `agents/*.py`
4. **Sample Outputs:** Browse `output/` directory

---

**Ready to Process RFPs!** 🚀
