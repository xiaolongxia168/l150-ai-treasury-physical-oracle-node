import asyncio
import sys
from pathlib import Path

# 添加 scripts 目录到路径
sys.path.insert(0, str(Path(__file__).parent / 'scripts'))
from final_crawler import crawl_merchant_platform

async def main():
    print("🚀 商家后台智能爬虫 - 开始执行")
    print("=" * 60)

    # 抖音来客
    print("\n【1/2】抓取抖音来客...")
    await crawl_merchant_platform(
        'douyin_laike',
        'https://laike.douyin.com/',
        'cookies/douyin_laike.json'
    )

    print("\n" + "="*60)
    print("休息 10 秒后继续...")
    print("="*60)
    await asyncio.sleep(10)

    # 美团开店宝
    print("\n【2/2】抓取美团开店宝...")
    await crawl_merchant_platform(
        'meituan_kaidian',
        'https://e.dianping.com/',
        'cookies/meituan_kaidian.json'
    )

    print("\n" + "="*60)
    print("🎉 全部抓取完成！")
    print("="*60)
    print("\n查看结果：")
    print("  ls -lh data/")

if __name__ == '__main__':
    asyncio.run(main())
