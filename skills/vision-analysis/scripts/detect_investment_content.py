#!/usr/bin/env python3
"""
Specialized investment content detection for OpenClaw Vision Analysis skill.
Detects investment-related charts, financial data, and business infographics.
"""

import os
import sys
import json
from PIL import Image, ImageFilter
import numpy as np

def detect_investment_content(image_path):
    """Detect investment-related content in images."""
    
    if not os.path.exists(image_path):
        return {"error": f"File not found: {image_path}"}
    
    try:
        # Open image
        img = Image.open(image_path)
        width, height = img.size
        
        # Convert to RGB and grayscale
        img_rgb = img.convert('RGB')
        img_gray = img.convert('L')
        
        # Convert to numpy arrays
        rgb_array = np.array(img_rgb)
        gray_array = np.array(img_gray)
        
        # Initialize detection results
        detections = {
            "chart_types": [],
            "financial_elements": [],
            "data_visualizations": [],
            "business_graphics": [],
            "confidence_scores": {}
        }
        
        # 1. Detect line charts (horizontal/vertical lines)
        line_chart_score = detect_line_charts(gray_array)
        if line_chart_score > 0.3:
            detections["chart_types"].append("line_chart")
            detections["confidence_scores"]["line_chart"] = round(line_chart_score, 3)
        
        # 2. Detect bar charts (rectangular patterns)
        bar_chart_score = detect_bar_charts(gray_array)
        if bar_chart_score > 0.3:
            detections["chart_types"].append("bar_chart")
            detections["confidence_scores"]["bar_chart"] = round(bar_chart_score, 3)
        
        # 3. Detect pie charts (circular patterns)
        pie_chart_score = detect_pie_charts(gray_array)
        if pie_chart_score > 0.3:
            detections["chart_types"].append("pie_chart")
            detections["confidence_scores"]["pie_chart"] = round(pie_chart_score, 3)
        
        # 4. Detect grid patterns (common in charts)
        grid_score = detect_grid_patterns(gray_array)
        if grid_score > 0.4:
            detections["financial_elements"].append("data_grid")
            detections["confidence_scores"]["data_grid"] = round(grid_score, 3)
        
        # 5. Detect financial colors (blue, green, red for financial charts)
        financial_color_score = detect_financial_colors(rgb_array)
        if financial_color_score > 0.3:
            detections["financial_elements"].append("financial_colors")
            detections["confidence_scores"]["financial_colors"] = round(financial_color_score, 3)
        
        # 6. Detect data points (small circles or markers)
        data_points_score = detect_data_points(gray_array)
        if data_points_score > 0.3:
            detections["data_visualizations"].append("data_points")
            detections["confidence_scores"]["data_points"] = round(data_points_score, 3)
        
        # 7. Detect arrows (common in trend analysis)
        arrow_score = detect_arrows(gray_array)
        if arrow_score > 0.3:
            detections["financial_elements"].append("trend_arrows")
            detections["confidence_scores"]["trend_arrows"] = round(arrow_score, 3)
        
        # 8. Detect percentage symbols or numbers
        percentage_score = detect_percentage_patterns(gray_array)
        if percentage_score > 0.3:
            detections["financial_elements"].append("percentage_data")
            detections["confidence_scores"]["percentage_data"] = round(percentage_score, 3)
        
        # 9. Detect business infographic elements
        infographic_score = detect_infographic_elements(rgb_array)
        if infographic_score > 0.3:
            detections["business_graphics"].append("infographic_elements")
            detections["confidence_scores"]["infographic_elements"] = round(infographic_score, 3)
        
        # Calculate overall investment content score
        overall_score = calculate_overall_score(detections)
        
        # Prepare results
        result = {
            "file_info": {
                "filename": os.path.basename(image_path),
                "dimensions": f"{width}x{height}"
            },
            "detections": detections,
            "investment_analysis": {
                "overall_investment_score": round(overall_score, 3),
                "content_type": classify_content_type(detections, overall_score),
                "target_audience": determine_target_audience(detections),
                "professional_level": assess_professional_level(detections, overall_score)
            },
            "recommendations": generate_investment_recommendations(detections, overall_score)
        }
        
        return result
        
    except Exception as e:
        return {"error": f"Error detecting investment content: {str(e)}"}

def detect_line_charts(gray_array):
    """Detect line chart patterns using edge detection."""
    from scipy import ndimage
    
    # Sobel edge detection
    dx = ndimage.sobel(gray_array, axis=0)
    dy = ndimage.sobel(gray_array, axis=1)
    edges = np.hypot(dx, dy)
    
    # Look for horizontal and vertical lines
    horizontal_lines = np.mean(np.abs(dx) > np.percentile(np.abs(dx), 90))
    vertical_lines = np.mean(np.abs(dy) > np.percentile(np.abs(dy), 90))
    
    # Line charts typically have both axes
    score = (horizontal_lines + vertical_lines) / 2
    return min(score * 5, 1.0)  # Scale to 0-1

def detect_bar_charts(gray_array):
    """Detect bar chart patterns (rectangular shapes)."""
    # Use edge detection
    edges = np.gradient(gray_array)
    edge_strength = np.mean(np.abs(edges[0]) + np.abs(edges[1]))
    
    # Bar charts have strong vertical edges
    vertical_gradient = np.abs(np.gradient(gray_array, axis=1))
    vertical_score = np.mean(vertical_gradient > np.percentile(vertical_gradient, 80))
    
    return min(vertical_score * 3, 1.0)

def detect_pie_charts(gray_array):
    """Detect pie chart patterns (circular shapes)."""
    from skimage import feature
    
    # Detect circles using Hough transform (simplified)
    edges = feature.canny(gray_array, sigma=2)
    
    # Count edge pixels in circular patterns
    center_x, center_y = gray_array.shape[1] // 2, gray_array.shape[0] // 2
    y, x = np.ogrid[:gray_array.shape[0], :gray_array.shape[1]]
    
    # Check for circular patterns
    distances = np.sqrt((x - center_x)**2 + (y - center_y)**2)
    max_dist = min(center_x, center_y)
    
    if max_dist > 0:
        # Look for edges at various radii
        circle_score = 0
        for r in range(10, max_dist, max_dist // 10):
            mask = np.abs(distances - r) < 5
            if np.any(mask):
                circle_score += np.mean(edges[mask])
        
        return min(circle_score / 5, 1.0)
    
    return 0.0

def detect_grid_patterns(gray_array):
    """Detect grid patterns common in charts."""
    # Look for regular patterns in both directions
    horizontal_profile = np.mean(gray_array, axis=1)
    vertical_profile = np.mean(gray_array, axis=0)
    
    # Check for periodic variations
    from scipy import signal
    
    h_autocorr = signal.correlate(horizontal_profile, horizontal_profile, mode='same')
    v_autocorr = signal.correlate(vertical_profile, vertical_profile, mode='same')
    
    # Grids show strong periodic correlations
    h_periodicity = np.std(h_autocorr) / np.mean(np.abs(h_autocorr))
    v_periodicity = np.std(v_autocorr) / np.mean(np.abs(v_autocorr))
    
    return min((h_periodicity + v_periodicity) / 2, 1.0)

def detect_financial_colors(rgb_array):
    """Detect financial chart colors (blue, green, red)."""
    # Financial charts often use blue for positive, red for negative
    blue_mask = (rgb_array[:, :, 2] > rgb_array[:, :, 0] * 1.2) & \
                (rgb_array[:, :, 2] > rgb_array[:, :, 1] * 1.2)
    
    green_mask = (rgb_array[:, :, 1] > rgb_array[:, :, 0] * 1.2) & \
                 (rgb_array[:, :, 1] > rgb_array[:, :, 2] * 1.2)
    
    red_mask = (rgb_array[:, :, 0] > rgb_array[:, :, 1] * 1.2) & \
               (rgb_array[:, :, 0] > rgb_array[:, :, 2] * 1.2)
    
    blue_ratio = np.mean(blue_mask)
    green_ratio = np.mean(green_mask)
    red_ratio = np.mean(red_mask)
    
    # Financial content often has significant blue/green
    financial_color_ratio = blue_ratio + green_ratio + red_ratio * 0.5
    return min(financial_color_ratio * 2, 1.0)

def detect_data_points(gray_array):
    """Detect data points (small circular markers)."""
    # Use blob detection (simplified)
    from scipy import ndimage
    
    # Find local maxima
    data = ndimage.gaussian_filter(gray_array, sigma=1)
    maxima = ndimage.maximum_filter(data, size=20) == data
    
    # Data points are small and isolated
    point_score = np.mean(maxima) * 100  # Scale up
    return min(point_score, 1.0)

def detect_arrows(gray_array):
    """Detect arrow patterns (common in trend analysis)."""
    # Arrows have triangular shapes - detect using gradient patterns
    grad_x = np.gradient(gray_array, axis=1)
    grad_y = np.gradient(gray_array, axis=0)
    
    # Look for directional patterns
    direction_changes = np.mean(np.abs(np.gradient(grad_x, axis=1)) + 
                               np.abs(np.gradient(grad_y, axis=0)))
    
    return min(direction_changes * 10, 1.0)

def detect_percentage_patterns(gray_array):
    """Detect percentage symbols or number patterns."""
    # Percentage symbols often have circles and slashes
    # Simplified: look for circular patterns near vertical lines
    edges = np.gradient(gray_array)
    edge_strength = np.abs(edges[0]) + np.abs(edges[1])
    
    # Look for high edge density areas (text-like)
    text_score = np.mean(edge_strength > np.percentile(edge_strength, 80))
    return min(text_score * 2, 1.0)

def detect_infographic_elements(rgb_array):
    """Detect infographic elements (icons, flowcharts, etc.)."""
    # Infographics often have distinct color blocks
    color_variance = np.std(rgb_array, axis=(0, 1))
    color_diversity = np.mean(color_variance) / 255
    
    # Also look for sharp color boundaries
    color_gradients = np.gradient(rgb_array, axis=(0, 1))
    boundary_strength = np.mean(np.abs(color_gradients[0]) + np.abs(color_gradients[1]))
    
    return min((color_diversity + boundary_strength) / 2, 1.0)

def calculate_overall_score(detections):
    """Calculate overall investment content score."""
    scores = list(detections["confidence_scores"].values())
    
    if not scores:
        return 0.0
    
    # Weight different detections
    chart_weight = 0.4
    financial_weight = 0.3
    data_weight = 0.2
    business_weight = 0.1
    
    weighted_score = 0.0
    count = 0
    
    for chart_type in ["line_chart", "bar_chart", "pie_chart"]:
        if chart_type in detections["confidence_scores"]:
            weighted_score += detections["confidence_scores"][chart_type] * chart_weight
            count += 1
    
    for financial in ["data_grid", "financial_colors", "trend_arrows", "percentage_data"]:
        if financial in detections["confidence_scores"]:
            weighted_score += detections["confidence_scores"][financial] * financial_weight
            count += 1
    
    for data_viz in ["data_points"]:
        if data_viz in detections["confidence_scores"]:
            weighted_score += detections["confidence_scores"][data_viz] * data_weight
            count += 1
    
    for business in ["infographic_elements"]:
        if business in detections["confidence_scores"]:
            weighted_score += detections["confidence_scores"][business] * business_weight
            count += 1
    
    if count > 0:
        return weighted_score / (chart_weight + financial_weight + data_weight + business_weight)
    
    return 0.0

def classify_content_type(detections, overall_score):
    """Classify the type of investment content."""
    if overall_score > 0.7:
        return "Professional Investment Analysis"
    elif overall_score > 0.5:
        return "Financial Data Visualization"
    elif overall_score > 0.3:
        return "Business Infographic"
    elif overall_score > 0.1:
        return "General Business Content"
    else:
        return "Non-Investment Content"

def determine_target_audience(detections):
    """Determine the target audience based on content."""
    chart_count = len([c for c in detections["chart_types"] if c in ["line_chart", "bar_chart", "pie_chart"]])
    
    if chart_count >= 2:
        return "Professional Investors / Financial Analysts"
    elif chart_count >= 1:
        return "Business Professionals / Entrepreneurs"
    elif len(detections["financial_elements"]) > 0:
        return "General Business Audience"
    else:
        return "General Audience"

def assess_professional_level(detections, overall_score):
    """Assess the professional level of the content."""
    if overall_score > 0.8:
        return "Enterprise Level"
    elif overall_score > 0.6:
        return "Professional Level"
    elif overall_score > 0.4:
        return "Business Level"
    elif overall_score > 0.2:
        return "Basic Level"
    else:
        return "Amateur Level"

def generate_investment_recommendations(detections, overall_score):
    """Generate recommendations for investment content."""
    recommendations = []
    
    if overall_score < 0.3:
        recommendations.append("Add financial charts or data visualizations")
        recommendations.append("Use professional color schemes (blues, greens)")
        recommendations.append("Include key financial metrics and trends")
    
    if "line_chart" not in detections["chart_types"] and overall_score < 0.6:
        recommendations.append("Consider adding line charts for trend analysis")
    
    if "bar_chart" not in detections["chart_types"] and overall_score < 0.6:
        recommendations.append("Add bar charts for comparative analysis")
    
    if "data_grid" not in detections["financial_elements"]:
        recommendations.append("Include data grids or tables for detailed analysis")
    
    if "financial_colors" not in detections["financial_elements"]:
        recommendations.append("Use standard financial colors (blue for positive, red for negative)")
    
    if overall_score >= 0.7:
        recommendations.append("Content is well-suited for professional investment audience")
        recommendations.append("Consider adding more advanced analytics or projections")
    
    return recommendations

def main():
    if len(sys.argv) != 2:
        print("Usage: python detect_investment_content.py <image_path>")
        sys.exit(1)
    
    image_path = sys.argv[1]
    result = detect_investment_content(image_path)
    
    # Output as JSON
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()