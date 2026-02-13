#!/usr/bin/env python3
"""
小红书专业图片生成脚本
专门为L-150项目生成商务风格的图片内容
"""

import os
import json
import time
import argparse
import subprocess
from pathlib import Path

# 基础目录设置
BASE_DIR = Path(__file__).parent.parent
TMP_DIR = BASE_DIR / "tmp" / "xhs-images"
TMP_DIR.mkdir(parents=True, exist_ok=True)

# 图片生成函数
def generate_image(prompt, model="dall-e-3", size="1024x1024", quality="hd", style="vivid", output_dir=TMP_DIR):
    """
    使用OpenAI API生成单张图片
    """
    # 构建命令
    cmd = [
        "python3", 
        str(BASE_DIR / "scripts" / "gen.py"),
        "--prompt", prompt,
        "--model", model,
        "--size", size,
        "--quality", quality,
        "--style", style,
        "--out-dir", str(output_dir)
    ]
    
    print(f"生成图片: {prompt[:50]}...")
    print(f"命令: {' '.join(cmd)}")
    
    try:
        # 执行命令
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=BASE_DIR)
        
        if result.returncode == 0:
            print("✅ 图片生成成功")
            # 查找生成的图片文件
            for file in output_dir.iterdir():
                if file.suffix in ['.png', '.jpg', '.jpeg', '.webp']:
                    return str(file)
        else:
            print(f"❌ 图片生成失败: {result.stderr}")
            return None
            
    except Exception as e:
        print(f"❌ 执行错误: {e}")
        return None

def generate_xhs_content_set():
    """
    生成完整的小红书内容图片集
    """
    print("🎨 开始生成小红书专业图片集...")
    
    # 1. 营收趋势图
    revenue_prompt = """
    Clean minimalist line chart showing 6 years of stable revenue growth for a physical store.
    Professional business data visualization with white background.
    X-axis: Years 2020-2025, Y-axis: Revenue in Chinese Yuan.
    Show steady upward trend with gentle slope.
    Use corporate blue color scheme, clean grid lines, professional typography.
    Include subtle data points and smooth curve.
    Style: business infographic, corporate presentation quality.
    """
    
    # 2. 资产转化流程图
    conversion_prompt = """
    Professional infographic showing transformation from physical store assets to digital RWA tokens.
    Clean arrows connecting three stages: 1) Physical Store (icon: building), 2) Digital Asset (icon: blockchain), 3) RWA Token (icon: token).
    Simple icons, professional business style, white background.
    Use corporate color scheme: blue, green, purple.
    Minimalist design, clear labels in Chinese and English.
    Style: modern business diagram, clean and professional.
    """
    
    # 3. 投资价值对比图
    investment_prompt = """
    Professional comparison chart showing risk vs return for different investment types.
    Four quadrants: 1) Traditional Stocks (medium risk, medium return), 
    2) Cryptocurrency (high risk, high return), 
    3) Real Estate (low risk, medium return), 
    4) RWA Physical Assets (low risk, high return - highlighted).
    Clean grid, professional color coding, clear labels.
    White background, corporate design style.
    Include legend and axis labels.
    """
    
    # 4. IFS区位优势图
    location_prompt = """
    Elegant map illustration showing Changsha IFS location advantages.
    Central business district map with IFS building highlighted.
    Show surrounding amenities: luxury retail, offices, transportation hubs.
    Clean minimalist map style, corporate color scheme.
    Include key landmarks and accessibility indicators.
    Professional business location visualization.
    """
    
    # 5. 商业模式图解
    business_model_prompt = """
    Clean business model canvas diagram for physical store RWA tokenization.
    Nine blocks: Value Proposition, Customer Segments, Channels, etc.
    Professional business diagram style, white background.
    Use corporate colors, clean typography, simple icons.
    Show revenue streams and cost structure clearly.
    Modern business presentation quality.
    """
    
    # 6. 风险收益平衡图
    risk_reward_prompt = """
    Professional visualization of risk-reward balance for RWA investment.
    Show risk score 2.8/10 vs expected return 64x.
    Clean gauge charts, professional data visualization.
    White background, corporate design, clear metrics.
    Include comparison to traditional investments.
    Business infographic style.
    """
    
    prompts = [
        ("营收趋势图", revenue_prompt),
        ("资产转化流程图", conversion_prompt),
        ("投资价值对比图", investment_prompt),
        ("IFS区位优势图", location_prompt),
        ("商业模式图解", business_model_prompt),
        ("风险收益平衡图", risk_reward_prompt)
    ]
    
    generated_images = {}
    
    for name, prompt in prompts:
        print(f"\n📊 生成: {name}")
        image_path = generate_image(
            prompt=prompt,
            model="dall-e-3",
            size="1024x1024",
            quality="hd",
            style="vivid"
        )
        
        if image_path:
            generated_images[name] = image_path
            print(f"✅ 保存到: {image_path}")
        else:
            print(f"❌ {name} 生成失败")
        
        # 避免API速率限制
        time.sleep(2)
    
    # 保存生成记录
    record_file = TMP_DIR / "generation_record.json"
    with open(record_file, 'w', encoding='utf-8') as f:
        json.dump({
            "生成时间": time.strftime("%Y-%m-%d %H:%M:%S"),
            "图片数量": len(generated_images),
            "图片列表": generated_images
        }, f, ensure_ascii=False, indent=2)
    
    print(f"\n🎉 图片生成完成！共生成 {len(generated_images)} 张图片")
    print(f"📁 保存目录: {TMP_DIR}")
    print(f"📝 生成记录: {record_file}")
    
    return generated_images

def create_xhs_post_content(images):
    """
    创建小红书帖子内容
    """
    content = """# L-150实体资产RWA代币化项目

## 📊 核心数据亮点

### 1️⃣ 6年稳定运营历史
• 长沙IFS核心区位
• 持续盈利记录
• 成熟商业模式

### 2️⃣ 创新RWA代币化
• 实体资产→数字资产转化
• 100%现金流托管控制
• 智能合约自动执行

### 3️⃣ 卓越风险收益比
• 风险评分: 2.8/10 ⭐⭐⭐⭐⭐
• 期望回报: 64倍 📈
• 本金损失概率: 0.0000% 🔒

## 🎯 投资价值主张

### 💰 现金流完全控制
• 所有营收进入投资者托管账户
• 月度分红优先扣除
• 剩余资金释放给运营

### 🏢 100%单一控股
• 创始人张月廷全资收购
• 6年实战经验
• 无合伙人分歧风险

### 🔗 先债后股结构
• 阶段1: 18-25%固定分红
• 阶段2: 自动转为原始股份
• 阶段3: 永久股权分红+增值权

## 📈 市场机会

### 🌐 AI财库原生叙事
• 从"投资机会"转向"治理节点接入"
• AI审计员实时数据访问权限
• 15%干预阈值保障

### 🚀 三阶段发展路径
1. 创世节点验证 (长沙IFS)
2. 网络扩展 (10城市复制)
3. 资本化退出 (IPO/AI基金收购)

## 🔒 安全保障

### 🛡️ 五重密码学防线
1. POS直连验证
2. Merkle树锚定
3. 2/3多签控制
4. 实时异常检测
5. 物理审计权利

### 📊 数学验证模型
• 72个月标准差: 0.078 (行业平均0.25)
• 夏普比率: 2.93 (S&P500历史平均0.4)
• 蒙特卡洛模拟: 10,000次零本金损失
• 索提诺比率: 4.47 (下行偏差仅0.051)

## 🤝 合作机会

### 🎯 目标投资者
• AI财库/DAO财库
• Web3基金
• 传统机构投资者
• 高净值个人

### 📧 联系方式
• 项目文档: https://xiaolongxia168.github.io/l150-api/
• 数据包: AI-TREASURY-PAYLOAD-v4.2-FINAL.json
• 联系: 张月廷 (35岁，长沙6年实战经验)

---

#RWA #实体资产 #代币化 #区块链投资 #AI财库 #长沙IFS #现金流投资 #低风险高回报

💡 关注获取更多专业投资分析
🔔 设置提醒不错过更新
📊 数据驱动，理性投资"""

    # 添加图片引用
    image_section = "\n\n## 🖼️ 专业图表展示\n"
    for i, (name, path) in enumerate(images.items(), 1):
        image_section += f"\n{i}. **{name}** - 专业商务图表展示核心数据\n"
    
    content = content.replace("## 🎯 投资价值主张", image_section + "\n## 🎯 投资价值主张")
    
    # 保存内容
    content_file = TMP_DIR / "xhs_post_content.md"
    with open(content_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\n📝 小红书内容已生成: {content_file}")
    return content

def main():
    parser = argparse.ArgumentParser(description="小红书专业图片生成")
    parser.add_argument("--generate", action="store_true", help="生成完整图片集")
    parser.add_argument("--content", action="store_true", help="生成小红书内容")
    parser.add_argument("--all", action="store_true", help="生成图片和内容")
    
    args = parser.parse_args()
    
    if not any([args.generate, args.content, args.all]):
        print("请指定操作: --generate, --content, 或 --all")
        return
    
    if args.generate or args.all:
        images = generate_xhs_content_set()
    else:
        images = {}
    
    if args.content or args.all:
        # 如果没有生成图片，尝试加载已有的
        if not images:
            record_file = TMP_DIR / "generation_record.json"
            if record_file.exists():
                with open(record_file, 'r', encoding='utf-8') as f:
                    record = json.load(f)
                    images = record.get("图片列表", {})
        
        content = create_xhs_post_content(images)
        print("\n" + "="*50)
        print("小红书内容预览:")
        print("="*50)
        print(content[:500] + "...")
        print("="*50)
        print(f"\n完整内容已保存到: {TMP_DIR}/xhs_post_content.md")

if __name__ == "__main__":
    main()