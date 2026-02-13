# Vision Analysis Skill

Analyze images to identify investment-related content, professional charts, and visual patterns.

## Installation

**Python dependencies:**
```bash
pip install pillow opencv-python numpy matplotlib
```

**macOS:**
```bash
brew install python
pip3 install pillow opencv-python numpy matplotlib
```

## Available Operations

### 1. Basic Image Analysis
```bash
python3 {baseDir}/scripts/analyze_image.py /path/to/image.png
```

**Output includes:**
- Image dimensions and format
- Color analysis
- Text detection (if any)
- Visual pattern recognition

### 2. Investment Content Detection
```bash
python3 {baseDir}/scripts/detect_investment_content.py /path/to/image.png
```

**Detects:**
- Charts and graphs
- Financial data visualizations
- Business infographics
- Investment-related symbols

### 3. Professional Quality Assessment
```bash
python3 {baseDir}/scripts/assess_quality.py /path/to/image.png
```

**Assesses:**
- Image resolution and clarity
- Color scheme professionalism
- Layout and composition
- Text readability

## Scripts

### analyze_image.py
Basic image analysis tool that provides:
- File information (size, format, dimensions)
- Color palette analysis
- Basic pattern recognition
- Edge detection for chart identification

### detect_investment_content.py
Specialized tool for investment-related content:
- Chart type detection (line, bar, pie, etc.)
- Financial symbol recognition
- Data visualization patterns
- Professional business graphics

### assess_quality.py
Quality assessment for professional content:
- Resolution check (minimum 300 DPI recommended)
- Color scheme analysis (corporate colors)
- Text clarity assessment
- Composition evaluation

## Use Cases

### 1. Investment Content Analysis
Analyze charts and graphs to identify:
- Revenue trends
- Risk-reward comparisons
- Financial projections
- Market analysis

### 2. Professional Design Assessment
Evaluate visual content for:
- Business presentation quality
- Corporate branding consistency
- Information clarity
- Visual appeal

### 3. Content Optimization
Provide recommendations for:
- Image improvement
- Better data visualization
- Enhanced readability
- Professional styling

## Examples

### Analyze a revenue chart:
```bash
python3 {baseDir}/scripts/analyze_image.py revenue_chart.png
```

### Detect investment content:
```bash
python3 {baseDir}/scripts/detect_investment_content.py investment_analysis.png
```

### Assess professional quality:
```bash
python3 {baseDir}/scripts/assess_quality.py business_infographic.png
```

## Output Format

All scripts output JSON format for easy parsing:
```json
{
  "file_info": {
    "filename": "image.png",
    "size_bytes": 1234567,
    "dimensions": "1024x768",
    "format": "PNG"
  },
  "analysis": {
    "color_scheme": "corporate_blue",
    "contains_charts": true,
    "chart_types": ["line_chart", "bar_chart"],
    "text_present": true,
    "investment_content_score": 0.85,
    "professional_quality_score": 0.92
  },
  "recommendations": [
    "Increase contrast for better readability",
    "Add data labels to charts",
    "Use consistent color scheme"
  ]
}
```

## Integration with OpenClaw

This skill can be used to:
1. Automatically analyze uploaded images
2. Provide feedback on visual content quality
3. Identify investment-related patterns
4. Optimize content for target audiences

## Dependencies

- Python 3.8+
- Pillow (PIL Fork) for image processing
- OpenCV for advanced computer vision
- NumPy for numerical operations
- Matplotlib for visualization (optional)

## Troubleshooting

### Common Issues:
1. **Missing dependencies**: Install all required Python packages
2. **Image format unsupported**: Convert to PNG or JPEG
3. **Large file sizes**: Resize images before analysis
4. **Low resolution**: Use higher quality source images

### Performance Tips:
- Process images in batch for multiple files
- Use lower resolution for quick analysis
- Cache analysis results for repeated use
- Parallel processing for large datasets