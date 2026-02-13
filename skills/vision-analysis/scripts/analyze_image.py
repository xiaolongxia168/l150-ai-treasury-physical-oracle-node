#!/usr/bin/env python3
"""
Basic image analysis tool for OpenClaw Vision Analysis skill.
Analyzes images to provide basic information and detect visual patterns.
"""

import os
import sys
import json
from PIL import Image
import numpy as np

def analyze_image(image_path):
    """Analyze an image and return detailed information."""
    
    if not os.path.exists(image_path):
        return {"error": f"File not found: {image_path}"}
    
    try:
        # Open image
        img = Image.open(image_path)
        
        # Basic information
        width, height = img.size
        format_type = img.format
        mode = img.mode
        file_size = os.path.getsize(image_path)
        
        # Convert to RGB if necessary
        if img.mode != 'RGB':
            img_rgb = img.convert('RGB')
        else:
            img_rgb = img
        
        # Convert to numpy array for analysis
        img_array = np.array(img_rgb)
        
        # Color analysis
        unique_colors = len(np.unique(img_array.reshape(-1, 3), axis=0))
        
        # Calculate average color
        avg_color = np.mean(img_array, axis=(0, 1)).astype(int)
        
        # Detect if image contains charts/graphs
        # Simple edge detection for chart patterns
        from PIL import ImageFilter
        edges = img.convert('L').filter(ImageFilter.FIND_EDGES())
        edge_array = np.array(edges)
        edge_density = np.mean(edge_array > 50)  # Percentage of edges
        
        # Check for text-like patterns (high frequency edges)
        text_likelihood = 0.0
        if edge_density > 0.1 and edge_density < 0.5:
            text_likelihood = min(edge_density * 3, 1.0)
        
        # Check for investment content patterns
        investment_score = 0.0
        patterns = []
        
        # Check for common chart colors (blues, greens, reds for financial charts)
        blue_pixels = np.sum((img_array[:, :, 2] > img_array[:, :, 0]) & 
                           (img_array[:, :, 2] > img_array[:, :, 1]))
        green_pixels = np.sum((img_array[:, :, 1] > img_array[:, :, 0]) & 
                            (img_array[:, :, 1] > img_array[:, :, 2]))
        
        blue_ratio = blue_pixels / (width * height)
        green_ratio = green_pixels / (width * height)
        
        if blue_ratio > 0.2:
            patterns.append("blue_dominant")
            investment_score += 0.3
        if green_ratio > 0.2:
            patterns.append("green_dominant")
            investment_score += 0.2
        
        # Check for grid-like patterns (common in charts)
        if edge_density > 0.05 and edge_density < 0.3:
            patterns.append("grid_pattern")
            investment_score += 0.2
        
        # Check for data point patterns
        if text_likelihood > 0.3:
            patterns.append("text_content")
            investment_score += 0.3
        
        # Professional quality assessment
        quality_score = 0.0
        quality_factors = []
        
        # Resolution check
        if width >= 1000 and height >= 1000:
            quality_score += 0.3
            quality_factors.append("high_resolution")
        
        # Color consistency
        if unique_colors < 1000:  # Limited color palette = more professional
            quality_score += 0.2
            quality_factors.append("limited_palette")
        
        # Aspect ratio check (common professional ratios)
        aspect_ratio = width / height
        if 0.6 <= aspect_ratio <= 1.8:  # Common presentation ratios
            quality_score += 0.2
            quality_factors.append("professional_aspect")
        
        # Brightness check
        brightness = np.mean(img_array) / 255
        if 0.3 <= brightness <= 0.8:  # Good brightness range
            quality_score += 0.2
            quality_factors.append("good_brightness")
        
        # Contrast check (simplified)
        contrast = np.std(img_array) / 255
        if contrast > 0.1:
            quality_score += 0.1
            quality_factors.append("good_contrast")
        
        # Prepare results
        result = {
            "file_info": {
                "filename": os.path.basename(image_path),
                "size_bytes": file_size,
                "dimensions": f"{width}x{height}",
                "format": format_type,
                "mode": mode,
                "aspect_ratio": round(aspect_ratio, 2)
            },
            "color_analysis": {
                "unique_colors": unique_colors,
                "average_color": avg_color.tolist(),
                "blue_ratio": round(blue_ratio, 3),
                "green_ratio": round(green_ratio, 3)
            },
            "pattern_detection": {
                "edge_density": round(edge_density, 3),
                "text_likelihood": round(text_likelihood, 3),
                "detected_patterns": patterns,
                "investment_content_score": round(min(investment_score, 1.0), 3)
            },
            "quality_assessment": {
                "professional_quality_score": round(min(quality_score, 1.0), 3),
                "quality_factors": quality_factors
            },
            "recommendations": generate_recommendations(
                width, height, investment_score, quality_score, patterns
            )
        }
        
        return result
        
    except Exception as e:
        return {"error": f"Error analyzing image: {str(e)}"}

def generate_recommendations(width, height, investment_score, quality_score, patterns):
    """Generate recommendations based on analysis."""
    recommendations = []
    
    # Resolution recommendations
    if width < 800 or height < 800:
        recommendations.append("Consider using higher resolution (minimum 1000x1000px)")
    
    # Investment content recommendations
    if investment_score < 0.5:
        recommendations.append("Add more charts or data visualizations for investment content")
    
    if "blue_dominant" not in patterns and investment_score > 0:
        recommendations.append("Consider using blue color scheme for professional financial content")
    
    # Quality recommendations
    if quality_score < 0.6:
        recommendations.append("Improve image quality: ensure good contrast and professional layout")
    
    if quality_score >= 0.8:
        recommendations.append("Image quality is excellent for professional presentation")
    
    # General recommendations
    if len(patterns) == 0:
        recommendations.append("Add visual elements like charts or infographics")
    
    return recommendations

def main():
    if len(sys.argv) != 2:
        print("Usage: python analyze_image.py <image_path>")
        sys.exit(1)
    
    image_path = sys.argv[1]
    result = analyze_image(image_path)
    
    # Output as JSON
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()