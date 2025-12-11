# Product Code to Diagram POC

A Python tool that converts product code definitions (in JSON format) into visual diagrams. This POC demonstrates how to automatically generate architecture diagrams, component diagrams, and flow diagrams from structured product code.

## Features

- **Architecture Diagrams**: Visualize product components and their dependencies
- **Component Diagrams**: Show detailed component structure grouped by type
- **Flow Diagrams**: Display process flows and workflows
- **Multiple Example Products**: Includes simple web app, e-commerce platform, and microservices architecture examples

## Project Structure

```
product-code-diagram-poc/
├── code_to_diagram.py          # Main application
├── requirements.txt             # Python dependencies
├── examples/                    # Example product code files
│   ├── simple_product.json
│   ├── ecommerce_product.json
│   └── microservices_product.json
├── output/                      # Generated diagram output (created automatically)
└── README.md                    # This file
```

## Installation

1. **Install Python Dependencies**

```powershell
pip install -r requirements.txt
```

2. **Install Graphviz**

You need to install Graphviz on your system:

- **Windows**: Download from [graphviz.org](https://graphviz.org/download/) or use Chocolatey:
  ```powershell
  choco install graphviz
  ```
- **macOS**: 
  ```bash
  brew install graphviz
  ```
- **Linux**: 
  ```bash
  sudo apt-get install graphviz  # Debian/Ubuntu
  sudo yum install graphviz      # RedHat/CentOS
  ```

## Usage

### Basic Usage

Run the main script to generate diagrams for all example products:

```powershell
python code_to_diagram.py
```

This will:
1. Parse all JSON files in the `examples/` directory
2. Generate architecture, component, and flow diagrams
3. Save PNG files in the `output/` directory

### Product Code Format

Product code is defined in JSON format with the following structure:

```json
{
  "product_name": "Your Product Name",
  "version": "1.0.0",
  "description": "Product description",
  "components": [
    {
      "id": "component_id",
      "name": "Component Name",
      "type": "frontend|backend|database|api|service|integration",
      "description": "Component description",
      "dependencies": ["other_component_id"],
      "interactions": [
        {
          "target": "target_component_id",
          "action": "interaction description"
        }
      ]
    }
  ],
  "flows": [
    {
      "name": "Flow Name",
      "steps": [
        {
          "name": "Step Name",
          "type": "process|decision|data"
        }
      ]
    }
  ]
}
```

### Component Types

The tool supports and color-codes the following component types:

- **frontend**: User interfaces (lightblue)
- **backend**: Backend services (lightgreen)
- **database**: Data stores (lightyellow)
- **api**: API layers (lightcoral)
- **service**: Microservices (plum)
- **integration**: External integrations (peachpuff)

## Examples

### Simple Web Application
A basic 3-tier web application with frontend, API, and database.

### E-Commerce Platform
A full-featured e-commerce system with multiple services including product catalog, shopping cart, and order processing.

### Microservices Architecture
A cloud-native microservices platform with event-driven communication, API gateway, and multiple specialized services.

## Generated Diagrams

The tool generates three types of diagrams for each product:

1. **Architecture Diagram** (`*_architecture.png`)
   - Shows high-level component relationships
   - Displays dependencies between components
   - Color-coded by component type

2. **Component Diagram** (`*_component.png`)
   - Detailed view of components grouped by type
   - Shows interactions between components
   - Includes component descriptions

3. **Flow Diagram** (`*_flow.png`)
   - Visualizes process flows
   - Shows decision points
   - Illustrates step-by-step workflows

## Customization

### Adding New Product Codes

1. Create a new JSON file in the `examples/` directory
2. Follow the product code format described above
3. Run the script to generate diagrams

### Modifying Diagram Styles

Edit the `DiagramGenerator` class in `code_to_diagram.py`:

- Change colors in the `_get_color_by_type()` method
- Modify graph attributes (rankdir, splines, etc.)
- Adjust node and edge styles

### Example: Custom Colors

```python
def _get_color_by_type(self, comp_type: str) -> str:
    colors = {
        'frontend': 'skyblue',      # Change to your preferred color
        'backend': 'limegreen',
        # ... add more
    }
    return colors.get(comp_type.lower(), 'white')
```

## Requirements

- Python 3.7+
- graphviz (Python package)
- Graphviz (system installation)

## Troubleshooting

### "GraphViz's executables not found"

Make sure Graphviz is installed on your system and added to your PATH:

```powershell
# Check if graphviz is in PATH
where dot
```

If not found, add Graphviz bin directory to your PATH environment variable.

### Import Errors

If you get import errors, ensure all dependencies are installed:

```powershell
pip install --upgrade -r requirements.txt
```

## Future Enhancements

- Support for additional diagram types (sequence diagrams, state diagrams)
- Export to multiple formats (SVG, PDF, etc.)
- Interactive HTML diagrams
- Support for other input formats (YAML, XML)
- Integration with CI/CD pipelines
- Real-time code parsing from actual source code files

## License

This is a POC (Proof of Concept) project for demonstration purposes.

## Contributing

Feel free to extend this POC with additional features:
- More diagram types
- Better styling options
- Integration with other tools
- Support for different product code formats

---

**Happy Diagramming! 📊**
