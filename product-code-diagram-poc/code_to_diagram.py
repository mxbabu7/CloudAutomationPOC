"""
Product Code to Diagram Generator
This module converts product code definitions into visual diagrams.
Supports multiple diagram formats: flowchart, architecture, and component diagrams.
"""

import json
import os
from typing import Dict, List, Any
from graphviz import Digraph


class ProductCodeParser:
    """Parses product code definitions from JSON format."""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.data = None
        
    def load(self) -> Dict[str, Any]:
        """Load product code from JSON file."""
        with open(self.file_path, 'r') as f:
            self.data = json.load(f)
        return self.data
    
    def validate(self) -> bool:
        """Validate the product code structure."""
        required_keys = ['product_name', 'components']
        return all(key in self.data for key in required_keys)


class DiagramGenerator:
    """Generates diagrams from product code definitions."""
    
    def __init__(self, product_data: Dict[str, Any]):
        self.product_data = product_data
        self.diagram = None
        
    def create_architecture_diagram(self, output_path: str = 'output/architecture'):
        """Create an architecture diagram showing product components and their relationships."""
        self.diagram = Digraph(
            comment=f"{self.product_data['product_name']} Architecture",
            format='png'
        )
        
        # Set graph attributes for better visualization
        self.diagram.attr(rankdir='TB', splines='ortho')
        self.diagram.attr('node', shape='box', style='rounded,filled', 
                         fillcolor='lightblue', fontname='Arial')
        self.diagram.attr('edge', color='gray', fontname='Arial')
        
        # Add product name as title
        self.diagram.node('product', self.product_data['product_name'],
                         shape='box', style='filled', fillcolor='lightgreen',
                         fontsize='16', fontname='Arial Bold')
        
        # Add components
        components = self.product_data.get('components', [])
        for component in components:
            comp_id = component['id']
            comp_name = component['name']
            comp_type = component.get('type', 'component')
            
            # Color code by type
            color = self._get_color_by_type(comp_type)
            
            label = f"{comp_name}\n({comp_type})"
            self.diagram.node(comp_id, label, fillcolor=color)
            
            # Connect to product
            self.diagram.edge('product', comp_id)
        
        # Add dependencies between components
        for component in components:
            comp_id = component['id']
            dependencies = component.get('dependencies', [])
            for dep in dependencies:
                self.diagram.edge(comp_id, dep, label='depends on')
        
        # Render the diagram
        self.diagram.render(output_path, cleanup=True)
        print(f"Architecture diagram saved to {output_path}.png")
        
    def create_component_diagram(self, output_path: str = 'output/component'):
        """Create a component diagram showing detailed component structure."""
        self.diagram = Digraph(
            comment=f"{self.product_data['product_name']} Components",
            format='png'
        )
        
        self.diagram.attr(rankdir='LR')
        self.diagram.attr('node', shape='component', style='filled', 
                         fillcolor='lightyellow', fontname='Arial')
        
        components = self.product_data.get('components', [])
        
        # Create subgraphs for different component types
        type_groups = {}
        for component in components:
            comp_type = component.get('type', 'component')
            if comp_type not in type_groups:
                type_groups[comp_type] = []
            type_groups[comp_type].append(component)
        
        # Add components grouped by type
        for comp_type, comps in type_groups.items():
            with self.diagram.subgraph(name=f'cluster_{comp_type}') as subgraph:
                subgraph.attr(label=comp_type.upper(), style='dashed')
                for component in comps:
                    comp_id = component['id']
                    comp_name = component['name']
                    desc = component.get('description', '')
                    label = f"{comp_name}\n{desc[:30]}..." if len(desc) > 30 else f"{comp_name}\n{desc}"
                    subgraph.node(comp_id, label)
        
        # Add interactions
        for component in components:
            comp_id = component['id']
            interactions = component.get('interactions', [])
            for interaction in interactions:
                target = interaction.get('target')
                action = interaction.get('action', 'interacts')
                if target:
                    self.diagram.edge(comp_id, target, label=action)
        
        # Render the diagram
        self.diagram.render(output_path, cleanup=True)
        print(f"Component diagram saved to {output_path}.png")
        
    def create_flow_diagram(self, output_path: str = 'output/flow'):
        """Create a flow diagram showing the process flow."""
        self.diagram = Digraph(
            comment=f"{self.product_data['product_name']} Flow",
            format='png'
        )
        
        self.diagram.attr(rankdir='TB')
        self.diagram.attr('node', shape='ellipse', style='filled', 
                         fillcolor='lightcyan', fontname='Arial')
        
        # Get flow steps
        flows = self.product_data.get('flows', [])
        
        if not flows:
            print("No flow data available in product code.")
            return
        
        for flow in flows:
            flow_name = flow.get('name', 'Default Flow')
            steps = flow.get('steps', [])
            
            # Add start node
            self.diagram.node('start', 'START', shape='circle', fillcolor='lightgreen')
            
            prev_node = 'start'
            for idx, step in enumerate(steps):
                step_id = f"step_{idx}"
                step_name = step.get('name', f'Step {idx+1}')
                step_type = step.get('type', 'process')
                
                # Different shapes for different step types
                shape = 'box' if step_type == 'process' else 'diamond' if step_type == 'decision' else 'parallelogram'
                
                self.diagram.node(step_id, step_name, shape=shape)
                self.diagram.edge(prev_node, step_id)
                
                prev_node = step_id
            
            # Add end node
            self.diagram.node('end', 'END', shape='circle', fillcolor='lightcoral')
            self.diagram.edge(prev_node, 'end')
        
        # Render the diagram
        self.diagram.render(output_path, cleanup=True)
        print(f"Flow diagram saved to {output_path}.png")
    
    def _get_color_by_type(self, comp_type: str) -> str:
        """Return color based on component type."""
        colors = {
            'frontend': 'lightblue',
            'backend': 'lightgreen',
            'database': 'lightyellow',
            'api': 'lightcoral',
            'service': 'plum',
            'integration': 'peachpuff'
        }
        return colors.get(comp_type.lower(), 'lightgray')


def main():
    """Main function to demonstrate the product code to diagram conversion."""
    
    # Check if examples exist
    example_files = [
        'examples/simple_product.json',
        'examples/ecommerce_product.json',
        'examples/microservices_product.json'
    ]
    
    for example_file in example_files:
        if os.path.exists(example_file):
            print(f"\n{'='*60}")
            print(f"Processing: {example_file}")
            print('='*60)
            
            # Parse product code
            parser = ProductCodeParser(example_file)
            product_data = parser.load()
            
            if not parser.validate():
                print(f"Invalid product code structure in {example_file}")
                continue
            
            print(f"Product: {product_data['product_name']}")
            print(f"Components: {len(product_data.get('components', []))}")
            
            # Generate diagrams
            generator = DiagramGenerator(product_data)
            
            # Create output directory if it doesn't exist
            os.makedirs('output', exist_ok=True)
            
            # Generate architecture diagram
            base_name = os.path.splitext(os.path.basename(example_file))[0]
            generator.create_architecture_diagram(f'output/{base_name}_architecture')
            
            # Generate component diagram
            generator.create_component_diagram(f'output/{base_name}_component')
            
            # Generate flow diagram if flow data exists
            if 'flows' in product_data:
                generator.create_flow_diagram(f'output/{base_name}_flow')
        else:
            print(f"Example file not found: {example_file}")
    
    print(f"\n{'='*60}")
    print("All diagrams generated successfully!")
    print("Check the 'output' directory for the generated PNG files.")
    print('='*60)


if __name__ == "__main__":
    main()
