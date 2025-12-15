"""
Stage 3: Diagram Generation Agent
Generates draw.io compatible XML architecture diagrams
"""

import json
from typing import List, Dict, Any, Optional
from pathlib import Path


def generate_diagram(
    architecture_mappings: List[Dict[str, Any]],
    cloud_provider: str = "azure",
    output_dir: str = "stage3_diagrams"
) -> str:
    """
    Generate draw.io XML diagram from architecture mappings
    
    Args:
        architecture_mappings: Architecture mappings from Stage 2
        cloud_provider: Cloud provider for icon selection
        output_dir: Output directory for diagram file
        
    Returns:
        Path to generated diagram file
    """
    
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    # Generate draw.io XML
    diagram_xml = _generate_drawio_xml(architecture_mappings, cloud_provider)
    
    # Save diagram
    diagram_file = output_path / f"{cloud_provider}_architecture.drawio.xml"
    with open(diagram_file, 'w', encoding='utf-8') as f:
        f.write(diagram_xml)
    
    # Also generate summary markdown
    summary = _generate_diagram_summary(architecture_mappings, cloud_provider)
    summary_file = output_path / "architecture_summary.md"
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write(summary)
    
    print(f"[OK] Diagram saved to {diagram_file}")
    print(f"[OK] Summary saved to {summary_file}")
    
    return str(diagram_file)


def _generate_drawio_xml(mappings: List[Dict[str, Any]], cloud_provider: str) -> str:
    """Generate draw.io XML format"""
    
    # draw.io XML structure
    # Group services by category for better layout
    service_categories = _categorize_services(mappings)
    
    xml_parts = []
    xml_parts.append('<?xml version="1.0" encoding="UTF-8"?>')
    xml_parts.append('<mxfile host="app.diagrams.net" modified="2025-12-15T12:00:00.000Z" agent="RFP Automation Agent" version="24.0.0">')
    xml_parts.append('  <diagram name="Architecture" id="architecture-diagram">')
    xml_parts.append('    <mxGraphModel dx="1422" dy="794" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1169" pageHeight="827" math="0" shadow="0">')
    xml_parts.append('      <root>')
    xml_parts.append('        <mxCell id="0" />')
    xml_parts.append('        <mxCell id="1" parent="0" />')
    
    # Add title
    xml_parts.append(f'        <mxCell id="title" value="{cloud_provider.upper()} Solution Architecture" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=24;fontStyle=1" vertex="1" parent="1">')
    xml_parts.append('          <mxGeometry x="40" y="20" width="400" height="40" as="geometry" />')
    xml_parts.append('        </mxCell>')
    
    # Add cloud provider logo/header
    xml_parts.append(f'        <mxCell id="cloud-header" value="{cloud_provider.upper()} Cloud Platform" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=16;fontStyle=1" vertex="1" parent="1">')
    xml_parts.append('          <mxGeometry x="40" y="80" width="1080" height="60" as="geometry" />')
    xml_parts.append('        </mxCell>')
    
    # Generate service boxes by category
    y_position = 180
    cell_id = 100
    
    for category, services in service_categories.items():
        # Category container
        xml_parts.append(f'        <mxCell id="cat-{cell_id}" value="{category}" style="swimlane;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;fontSize=14;fontStyle=1" vertex="1" parent="1">')
        xml_parts.append(f'          <mxGeometry x="40" y="{y_position}" width="1080" height="120" as="geometry" />')
        xml_parts.append('        </mxCell>')
        
        # Add services within category
        x_offset = 20
        for i, service in enumerate(services[:6]):  # Limit to 6 services per row
            service_id = f"service-{cell_id}-{i}"
            service_name = service['service']
            pattern = service.get('pattern', 'Standard')
            
            xml_parts.append(f'        <mxCell id="{service_id}" value="{service_name}\\n({pattern})" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;fontSize=11" vertex="1" parent="cat-{cell_id}">')
            xml_parts.append(f'          <mxGeometry x="{x_offset}" y="30" width="160" height="70" as="geometry" />')
            xml_parts.append('        </mxCell>')
            
            x_offset += 180
        
        y_position += 140
        cell_id += 1
    
    # Add legend
    legend_y = y_position + 20
    xml_parts.append(f'        <mxCell id="legend" value="Legend" style="swimlane;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;fontSize=12;fontStyle=1" vertex="1" parent="1">')
    xml_parts.append(f'          <mxGeometry x="40" y="{legend_y}" width="300" height="120" as="geometry" />')
    xml_parts.append('        </mxCell>')
    
    xml_parts.append(f'        <mxCell id="legend-1" value="Fully Compliant" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;" vertex="1" parent="legend">')
    xml_parts.append('          <mxGeometry x="10" y="30" width="120" height="30" as="geometry" />')
    xml_parts.append('        </mxCell>')
    
    xml_parts.append(f'        <mxCell id="legend-2" value="Partial Compliance" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;" vertex="1" parent="legend">')
    xml_parts.append('          <mxGeometry x="10" y="70" width="120" height="30" as="geometry" />')
    xml_parts.append('        </mxCell>')
    
    # Close XML structure
    xml_parts.append('      </root>')
    xml_parts.append('    </mxGraphModel>')
    xml_parts.append('  </diagram>')
    xml_parts.append('</mxfile>')
    
    return '\n'.join(xml_parts)


def _categorize_services(mappings: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, str]]]:
    """Categorize services for better diagram layout"""
    
    categories = {
        "High Availability & Disaster Recovery": [],
        "Compute & Application Services": [],
        "Data & Storage Services": [],
        "Networking & Security": [],
        "Monitoring & Management": [],
        "Other Services": []
    }
    
    for mapping in mappings:
        service = mapping.get("cloud_service", "")
        pattern = mapping.get("architecture_pattern", "")
        req_id = mapping.get("req_id", "")
        
        service_info = {
            "service": service,
            "pattern": pattern,
            "req_id": req_id
        }
        
        service_lower = service.lower()
        
        # Categorize based on service type
        if any(word in service_lower for word in ["front door", "traffic manager", "recovery", "backup", "availability"]):
            categories["High Availability & Disaster Recovery"].append(service_info)
        elif any(word in service_lower for word in ["vm", "app service", "container", "function", "kubernetes", "compute"]):
            categories["Compute & Application Services"].append(service_info)
        elif any(word in service_lower for word in ["storage", "database", "sql", "cosmos", "blob", "disk"]):
            categories["Data & Storage Services"].append(service_info)
        elif any(word in service_lower for word in ["network", "vpn", "firewall", "security", "key vault", "ad"]):
            categories["Networking & Security"].append(service_info)
        elif any(word in service_lower for word in ["monitor", "insights", "log", "analytics"]):
            categories["Monitoring & Management"].append(service_info)
        else:
            categories["Other Services"].append(service_info)
    
    # Remove empty categories
    return {k: v for k, v in categories.items() if v}


def _generate_diagram_summary(mappings: List[Dict[str, Any]], cloud_provider: str) -> str:
    """Generate markdown summary of architecture"""
    
    lines = []
    lines.append(f"# {cloud_provider.upper()} Solution Architecture Summary")
    lines.append("")
    lines.append(f"**Generated:** {_get_timestamp()}")
    lines.append(f"**Cloud Provider:** {cloud_provider.upper()}")
    lines.append(f"**Total Services Mapped:** {len(mappings)}")
    lines.append("")
    
    # Group by category
    categories = _categorize_services(mappings)
    
    lines.append("## Architecture Components")
    lines.append("")
    
    for category, services in categories.items():
        lines.append(f"### {category}")
        lines.append("")
        
        for service_info in services:
            # Find full mapping details
            full_mapping = next(
                (m for m in mappings if m.get("req_id") == service_info["req_id"]), 
                {}
            )
            
            lines.append(f"**{service_info['service']}**")
            lines.append(f"- **Pattern:** {service_info['pattern']}")
            lines.append(f"- **Requirement ID:** {service_info['req_id']}")
            
            if full_mapping.get("compliance_level"):
                lines.append(f"- **Compliance:** {full_mapping['compliance_level']}")
            
            if full_mapping.get("additional_services"):
                additional = full_mapping["additional_services"]
                if additional:
                    lines.append(f"- **Additional Services:** {', '.join(additional)}")
            
            if full_mapping.get("implementation_notes"):
                lines.append(f"- **Notes:** {full_mapping['implementation_notes']}")
            
            lines.append("")
    
    # Compliance summary
    lines.append("## Compliance Summary")
    lines.append("")
    
    compliance_counts = {}
    for mapping in mappings:
        level = mapping.get("compliance_level", "Unknown")
        compliance_counts[level] = compliance_counts.get(level, 0) + 1
    
    lines.append("| Compliance Level | Count |")
    lines.append("|-----------------|-------|")
    for level, count in sorted(compliance_counts.items()):
        lines.append(f"| {level} | {count} |")
    
    lines.append("")
    
    # Architecture patterns summary
    lines.append("## Architecture Patterns Used")
    lines.append("")
    
    pattern_counts = {}
    for mapping in mappings:
        pattern = mapping.get("architecture_pattern", "Unknown")
        pattern_counts[pattern] = pattern_counts.get(pattern, 0) + 1
    
    for pattern, count in sorted(pattern_counts.items(), key=lambda x: x[1], reverse=True):
        lines.append(f"- **{pattern}:** {count} requirement(s)")
    
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## How to Use the Diagram")
    lines.append("")
    lines.append("1. Open the `.drawio.xml` file in [diagrams.net](https://app.diagrams.net)")
    lines.append("2. The diagram shows all cloud services organized by category")
    lines.append("3. Each service box includes the architecture pattern")
    lines.append("4. Color coding indicates compliance level (see legend)")
    lines.append("5. Edit the diagram to add connections, update layouts, or customize icons")
    lines.append("")
    
    return '\n'.join(lines)


def _get_timestamp() -> str:
    """Get current timestamp"""
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
