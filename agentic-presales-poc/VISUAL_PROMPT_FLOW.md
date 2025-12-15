# 🎨 Visual Prompt Flow Architecture

```
╔══════════════════════════════════════════════════════════════════════════════════╗
║                    AGENTIC AI PRE-SALES INFRASTRUCTURE                           ║
║                         Complete Prompt Flow Diagram                             ║
╚══════════════════════════════════════════════════════════════════════════════════╝


┌──────────────────────────────────────────────────────────────────────────────────┐
│  STEP 0: CONFIGURATION & INITIALIZATION                                         │
└──────────────────────────────────────────────────────────────────────────────────┘

    📁 .env File
    ├── AI_PROVIDER=openai
    ├── OPENAI_API_KEY=sk-proj-...
    ├── OPENAI_MODEL=gpt-4o-mini
    ├── OPENAI_TEMPERATURE=0.7
    └── ENABLE_AI=true
         │
         ▼
    ⚙️  config/ai_config.py
         │
         ▼
    🔌 utils/ai_client.py
    ├── OpenAI Client
    ├── Azure OpenAI Client  
    └── GitHub Models Client


┌──────────────────────────────────────────────────────────────────────────────────┐
│  INPUT: RFP DOCUMENT                                                             │
└──────────────────────────────────────────────────────────────────────────────────┘

    📄 sample_input/MMI Cloud Requirements.pdf
         │
         │ utils/pdf_reader.py (PyPDF)
         ▼
    📝 Raw Text (5,840 characters)
    │
    │  "The organization requires a cloud-based infrastructure..."
    │
    └─────────────────────────────────────────────────────────────────────────┐
                                                                               │
                                                                               ▼


╔══════════════════════════════════════════════════════════════════════════════════╗
║  AI PROMPT #1: RFP ANALYSIS AGENT                                                ║
╠══════════════════════════════════════════════════════════════════════════════════╣
║  Agent: agents/rfp_analysis_agent.py                                             ║
║  Model: GPT-4o-mini                                                              ║
║  Temperature: 0.3 (Deterministic)                                                ║
║  Max Tokens: 4000                                                                ║
╚══════════════════════════════════════════════════════════════════════════════════╝

    🎯 SYSTEM PROMPT:
    ┌────────────────────────────────────────────────────────────────────────┐
    │ "You are an expert RFP analyst. Analyze the provided RFP document     │
    │  and extract structured information.                                   │
    │                                                                        │
    │  Return ONLY a valid JSON object with:                                │
    │  - business_goals                                                      │
    │  - functional_requirements                                             │
    │  - non_functional_requirements (performance, security, availability)   │
    │  - constraints                                                         │
    │  - assumptions                                                         │
    │  - risks                                                               │
    │                                                                        │
    │  Extract as much detail as possible. Be specific and comprehensive."   │
    └────────────────────────────────────────────────────────────────────────┘

    💬 USER PROMPT:
    ┌────────────────────────────────────────────────────────────────────────┐
    │ [Raw RFP text - 5,840 characters]                                     │
    └────────────────────────────────────────────────────────────────────────┘

    🤖 AI PROCESSING...
    
    ✅ OUTPUT: output/rfp_analysis.json
    ┌────────────────────────────────────────────────────────────────────────┐
    │ {                                                                      │
    │   "business_goals": [                                                  │
    │     "Modernize infrastructure",                                        │
    │     "Improve scalability",                                             │
    │     "Enhance security"                                                 │
    │   ],                                                                   │
    │   "functional_requirements": [...],                                    │
    │   "non_functional_requirements": {                                     │
    │     "performance": "Low latency (<100ms)",                             │
    │     "security": "IAM, encryption at rest/transit",                     │
    │     "availability": "99.9% uptime SLA",                                │
    │     "compliance": ["ISO 27001", "SOC 2", "GDPR"]                       │
    │   },                                                                   │
    │   "constraints": ["Budget-conscious", "6-month timeline"],             │
    │   "assumptions": ["Greenfield deployment"],                            │
    │   "risks": ["Vendor lock-in", "Data migration"]                        │
    │ }                                                                      │
    └────────────────────────────────────────────────────────────────────────┘
         │
         └─────────────────────────────────────────────────────────────────────┐
                                                                               │
                                                                               ▼


╔══════════════════════════════════════════════════════════════════════════════════╗
║  AI PROMPT #2: ARCHITECTURE DESIGN AGENT                                         ║
╠══════════════════════════════════════════════════════════════════════════════════╣
║  Agent: agents/architecture_agent.py                                             ║
║  Model: GPT-4o-mini                                                              ║
║  Temperature: 0.4 (Balanced)                                                     ║
║  Max Tokens: 4000                                                                ║
╚══════════════════════════════════════════════════════════════════════════════════╝

    🎯 SYSTEM PROMPT:
    ┌────────────────────────────────────────────────────────────────────────┐
    │ "You are a cloud solutions architect. Design a cloud-agnostic         │
    │  logical architecture based on the RFP analysis provided.              │
    │                                                                        │
    │  Return ONLY a valid JSON object with:                                │
    │  - layers (name, components, responsibilities)                         │
    │  - data_flow (from, to, protocol)                                      │
    │  - security_controls                                                   │
    │  - scalability_approach                                                │
    │  - disaster_recovery (rpo, rto, strategy)                              │
    │                                                                        │
    │  Design a comprehensive, production-ready architecture."               │
    └────────────────────────────────────────────────────────────────────────┘

    💬 USER PROMPT:
    ┌────────────────────────────────────────────────────────────────────────┐
    │ RFP Analysis:                                                          │
    │ {rfp_analysis.json content}                                            │
    │                                                                        │
    │ Design the architecture based on these requirements.                   │
    └────────────────────────────────────────────────────────────────────────┘

    🤖 AI PROCESSING...
    
    ✅ OUTPUT: output/architecture.json
    ┌────────────────────────────────────────────────────────────────────────┐
    │ {                                                                      │
    │   "layers": [                                                          │
    │     {                                                                  │
    │       "name": "Presentation Layer",                                    │
    │       "components": ["Web App", "Mobile App", "CDN"],                  │
    │       "responsibilities": ["UI", "Client logic", "Content delivery"]   │
    │     },                                                                 │
    │     {                                                                  │
    │       "name": "Application Layer",                                     │
    │       "components": ["API Gateway", "Business Logic", "Auth Service"], │
    │       "responsibilities": ["Request routing", "Business rules"]        │
    │     },                                                                 │
    │     {                                                                  │
    │       "name": "Data Layer",                                            │
    │       "components": ["Database", "Cache", "Object Storage"],           │
    │       "responsibilities": ["Data persistence", "State management"]     │
    │     }                                                                  │
    │   ],                                                                   │
    │   "data_flow": [                                                       │
    │     {"from": "Web App", "to": "API Gateway", "protocol": "HTTPS"},     │
    │     {"from": "API Gateway", "to": "Business Logic", "protocol": "HTTP"}│
    │   ],                                                                   │
    │   "security_controls": ["IAM", "Encryption", "WAF", "DDoS Protection"],│
    │   "scalability_approach": "Auto-scaling groups, load balancing",       │
    │   "disaster_recovery": {                                               │
    │     "rpo": "1 hour",                                                   │
    │     "rto": "4 hours",                                                  │
    │     "strategy": "Multi-region replication with automated failover"     │
    │   }                                                                    │
    │ }                                                                      │
    └────────────────────────────────────────────────────────────────────────┘
         │
         │  [Non-AI Agents Execute]
         │  ├── Cloud Mapping Agent → maps to AWS/Azure/GCP services
         │  ├── Cost Agent → calculates pricing
         │  └── Roadmap Agent → generates timeline
         │
         └─────────────────────────────────────────────────────────────────────┐
                                                                               │
                                                                               ▼


╔══════════════════════════════════════════════════════════════════════════════════╗
║  AI PROMPT #3: PROPOSAL GENERATION AGENT                                         ║
╠══════════════════════════════════════════════════════════════════════════════════╣
║  Agent: agents/proposal_agent.py                                                 ║
║  Model: GPT-4o-mini                                                              ║
║  Temperature: 0.5 (Creative)                                                     ║
║  Max Tokens: 4000                                                                ║
╚══════════════════════════════════════════════════════════════════════════════════╝

    🎯 SYSTEM PROMPT:
    ┌────────────────────────────────────────────────────────────────────────┐
    │ "You are a pre-sales consultant creating a professional cloud         │
    │  solution proposal.                                                    │
    │                                                                        │
    │  Generate a comprehensive, executive-level proposal in Markdown.       │
    │                                                                        │
    │  Include these sections:                                               │
    │  1. Executive Summary                                                  │
    │  2. Business Objectives Alignment                                      │
    │  3. Proposed Architecture Overview                                     │
    │  4. Architecture Layers and Components                                 │
    │  5. Security Controls                                                  │
    │  6. Disaster Recovery                                                  │
    │  7. Cost Breakdown                                                     │
    │  8. Non-Functional Requirements                                        │
    │  9. Risk Mitigation                                                    │
    │  10. Next Steps                                                        │
    │  11. Conclusion                                                        │
    │                                                                        │
    │  Make it professional, persuasive, and technically sound.              │
    │  Use tables where appropriate."                                        │
    └────────────────────────────────────────────────────────────────────────┘

    💬 USER PROMPT:
    ┌────────────────────────────────────────────────────────────────────────┐
    │ RFP Analysis:                                                          │
    │ {rfp_analysis.json}                                                    │
    │                                                                        │
    │ Architecture:                                                          │
    │ {architecture.json}                                                    │
    │                                                                        │
    │ Cost Estimate:                                                         │
    │ {cost.json}                                                            │
    │                                                                        │
    │ Generate a compelling proposal based on this information.              │
    └────────────────────────────────────────────────────────────────────────┘

    🤖 AI PROCESSING...
    
    ✅ OUTPUT: output/proposal.md
    ┌────────────────────────────────────────────────────────────────────────┐
    │ # Cloud Solution Proposal                                              │
    │                                                                        │
    │ ## Executive Summary                                                   │
    │                                                                        │
    │ This proposal presents a comprehensive cloud solution designed to      │
    │ meet your organization's requirements for modernization, scalability,  │
    │ and security. Our solution leverages AWS cloud services to deliver     │
    │ a robust, scalable, and cost-effective architecture.                   │
    │                                                                        │
    │ ### Key Highlights                                                     │
    │                                                                        │
    │ - **Estimated Monthly Cost:** $8,450.00 USD                            │
    │ - **Estimated Annual Cost:** $101,400.00 USD                           │
    │ - **Target Availability:** 99.9% uptime SLA                            │
    │ - **Compliance:** ISO 27001, SOC 2, GDPR                               │
    │                                                                        │
    │ ## Business Objectives                                                 │
    │                                                                        │
    │ [AI-generated alignment with RFP goals]                                │
    │                                                                        │
    │ ## Proposed Architecture                                               │
    │                                                                        │
    │ [Detailed architecture description]                                    │
    │                                                                        │
    │ ## Cost Breakdown                                                      │
    │                                                                        │
    │ | Service          | Monthly Cost | Annual Cost  |                    │
    │ |------------------|--------------|--------------|                    │
    │ | EC2 Instances    | $2,800       | $33,600      |                    │
    │ | RDS Database     | $1,500       | $18,000      |                    │
    │ | S3 Storage       | $850         | $10,200      |                    │
    │ | CloudFront CDN   | $1,200       | $14,400      |                    │
    │ | Load Balancer    | $600         | $7,200       |                    │
    │ | Other Services   | $1,500       | $18,000      |                    │
    │ | **TOTAL**        | **$8,450**   | **$101,400** |                    │
    │                                                                        │
    │ [... rest of professional proposal ...]                                │
    └────────────────────────────────────────────────────────────────────────┘
         │
         └─────────────────────────────────────────────────────────────────────┐
                                                                               │
                                                                               ▼


╔══════════════════════════════════════════════════════════════════════════════════╗
║  AI PROMPT #4: PYTHON DIAGRAM CODE GENERATOR                                     ║
╠══════════════════════════════════════════════════════════════════════════════════╣
║  Agent: agents/ai_diagram_agent.py                                               ║
║  Model: GPT-4o-mini                                                              ║
║  Temperature: 0.3 (Precise)                                                      ║
║  Max Tokens: 4000                                                                ║
╚══════════════════════════════════════════════════════════════════════════════════╝

    🎯 SYSTEM PROMPT:
    ┌────────────────────────────────────────────────────────────────────────┐
    │ "You are an expert at generating Python code using the 'diagrams'     │
    │  library for AWS/Azure/GCP architecture diagrams.                      │
    │                                                                        │
    │  Generate complete, executable Python code that:                       │
    │  1. Imports necessary components from the diagrams library             │
    │  2. Creates a professional architecture diagram                        │
    │  3. Uses appropriate cloud provider icons (aws/azure/gcp)              │
    │  4. Includes clusters for logical grouping                             │
    │  5. Shows data flows with Edge connections                             │
    │  6. Uses proper colors and labels                                      │
    │                                                                        │
    │  Return ONLY valid Python code. No markdown, no explanations.          │
    │                                                                        │
    │  Make it production-ready and visually clear."                         │
    └────────────────────────────────────────────────────────────────────────┘

    💬 USER PROMPT:
    ┌────────────────────────────────────────────────────────────────────────┐
    │ Architecture:                                                          │
    │ {architecture.json}                                                    │
    │                                                                        │
    │ Cloud Mapping (AWS):                                                   │
    │ {cloud_mapping.json}                                                   │
    │                                                                        │
    │ Generate Python diagrams code for this architecture using AWS icons.   │
    └────────────────────────────────────────────────────────────────────────┘

    🤖 AI PROCESSING...
    
    ✅ OUTPUT: output/generate_python_diagram.py
    ┌────────────────────────────────────────────────────────────────────────┐
    │ """                                                                    │
    │ Auto-generated Architecture Diagram                                    │
    │ Generated by Agentic Pre-Sales POC                                     │
    │ """                                                                    │
    │ from diagrams import Diagram, Cluster, Edge                            │
    │ from diagrams.aws.compute import EC2, Lambda, ECS                      │
    │ from diagrams.aws.database import RDS, Dynamodb                        │
    │ from diagrams.aws.network import VPC, ELB, CloudFront                  │
    │ from diagrams.aws.storage import S3                                    │
    │ from diagrams.aws.security import KMS, WAF, IAM                        │
    │                                                                        │
    │ with Diagram("AWS Cloud Architecture", show=False, filename="aws_arch"):│
    │     # Presentation Layer                                               │
    │     with Cluster("Presentation Layer"):                                │
    │         cdn = CloudFront("CDN")                                        │
    │         waf = WAF("Web Firewall")                                      │
    │         lb = ELB("Load Balancer")                                      │
    │                                                                        │
    │     # Application Layer                                                │
    │     with Cluster("Application Layer"):                                 │
    │         web_servers = [EC2("Web 1"), EC2("Web 2"), EC2("Web 3")]       │
    │         api = Lambda("API Gateway")                                    │
    │                                                                        │
    │     # Data Layer                                                       │
    │     with Cluster("Data Layer"):                                        │
    │         db = RDS("Primary DB")                                         │
    │         cache = Dynamodb("Cache")                                      │
    │         storage = S3("Object Storage")                                 │
    │                                                                        │
    │     # Security                                                         │
    │     iam = IAM("Identity & Access")                                     │
    │     kms = KMS("Encryption")                                            │
    │                                                                        │
    │     # Data Flow                                                        │
    │     cdn >> Edge(label="HTTPS") >> waf >> lb                            │
    │     lb >> Edge(label="HTTP") >> web_servers                            │
    │     web_servers >> Edge(label="API") >> api                            │
    │     api >> Edge(label="SQL") >> db                                     │
    │     api >> Edge(label="Cache") >> cache                                │
    │     web_servers >> Edge(label="Assets") >> storage                     │
    │                                                                        │
    │ print("✅ Architecture diagram generated: aws_arch.png")               │
    └────────────────────────────────────────────────────────────────────────┘
         │
         │  Execute: python output/generate_python_diagram.py
         ▼
    🖼️  OUTPUT: aws_arch.png (Visual Architecture Diagram)


┌──────────────────────────────────────────────────────────────────────────────────┐
│  FINAL DELIVERABLES                                                              │
└──────────────────────────────────────────────────────────────────────────────────┘

    📦 Complete Solution Package:
    
    output/
    ├── 📄 rfp_analysis.json           ← AI Prompt #1 output
    ├── 🏗️  architecture.json           ← AI Prompt #2 output
    ├── 📝 proposal.md                  ← AI Prompt #3 output (30+ pages)
    ├── 🐍 generate_python_diagram.py   ← AI Prompt #4 output
    ├── 💰 cost.json                    ← Cost calculations
    ├── 📅 roadmap.json                 ← Delivery timeline
    ├── 🖼️  architecture.png             ← Generated diagram
    ├── 📊 architecture.drawio          ← Draw.io diagram
    └── 📋 extracted_rfp_text.txt       ← Original RFP text


═══════════════════════════════════════════════════════════════════════════════════

                            KEY STATISTICS

    📊 Total AI Agents: 4 specialized agents
    🔄 Total AI Calls: 4 API calls per execution
    ⏱️  Average Execution Time: 30-60 seconds
    💾 Total Output Files: 8+ files
    🎯 Success Rate: >95% (with fallback templates)
    💰 Typical API Cost: $0.10-0.30 per run (using gpt-4o-mini)

═══════════════════════════════════════════════════════════════════════════════════

                        SUPPORTED AI PROVIDERS

    ✅ OpenAI (GPT-4o, GPT-4o-mini, GPT-4-turbo)
    ✅ Azure OpenAI (All GPT-4 models)
    ✅ GitHub Models (GPT-4o via GitHub)

═══════════════════════════════════════════════════════════════════════════════════

                           ERROR HANDLING

    Each agent includes fallback logic:
    
    Try:
        🤖 Call AI with prompt
        ✅ Parse and validate response
        💾 Return structured output
    Catch:
        ⚠️  Log error
        🔄 Fall back to static template
        ✅ Continue execution (no failure)

═══════════════════════════════════════════════════════════════════════════════════

    Created: December 2024
    System: Agentic Pre-Sales POC
    Version: 1.0
```
