// 美团开店宝数据提取脚本
// 在浏览器控制台(F12)中运行

(function extractMeituanData() {
    console.log('🍜 开始提取美团开店宝数据...');
    
    const data = {
        platform: '美团开店宝',
        extractTime: new Date().toISOString(),
        url: window.location.href,
        metrics: {},
        orders: [],
        reviews: []
    };
    
    // 提取经营数据
    try {
        // 曝光量
        const exposure = document.querySelector('[class*="exposure"], [class*="曝光"]')?.textContent?.trim();
        // 访问量
        const visit = document.querySelector('[class*="visit"], [class*="访问"]')?.textContent?.trim();
        // 订单量
        const orders = document.querySelector('[class*="order"], [class*="订单"]')?.textContent?.trim();
        // 交易额
        const revenue = document.querySelector('[class*="revenue"], [class*="交易"], [class*="金额"]')?.textContent?.trim();
        
        data.metrics = {
            exposure: exposure || '',
            visit: visit || '',
            orders: orders || '',
            revenue: revenue || ''
        };
    } catch (e) {
        console.log('提取经营数据时出错:', e);
    }
    
    // 提取订单数据
    const orderItems = document.querySelectorAll('[class*="order-item"], [class*="订单"]');
    orderItems.forEach((item, index) => {
        try {
            const order = {
                index: index + 1,
                orderId: item.querySelector('[class*="id"], [class*="编号"]')?.textContent?.trim() || '',
                amount: item.querySelector('[class*="amount"], [class*="金额"]')?.textContent?.trim() || '',
                status: item.querySelector('[class*="status"], [class*="状态"]')?.textContent?.trim() || '',
                time: item.querySelector('[class*="time"], [class*="时间"]')?.textContent?.trim() || ''
            };
            
            if (order.orderId || order.amount) {
                data.orders.push(order);
            }
        } catch (e) {
            console.log('提取第' + (index + 1) + '个订单时出错:', e);
        }
    });
    
    // 提取评价数据
    const reviewItems = document.querySelectorAll('[class*="review"], [class*="评价"], [class*="comment"]');
    reviewItems.forEach((item, index) => {
        try {
            const review = {
                index: index + 1,
                rating: item.querySelector('[class*="rating"], [class*="评分"], [class*="star"]')?.textContent?.trim() || '',
                content: item.querySelector('[class*="content"], [class*="内容"], p')?.textContent?.trim() || '',
                user: item.querySelector('[class*="user"], [class*="用户"], [class*="name"]')?.textContent?.trim() || '',
                time: item.querySelector('[class*="time"], [class*="时间"]')?.textContent?.trim() || ''
            };
            
            if (review.content) {
                data.reviews.push(review);
            }
        } catch (e) {
            console.log('提取第' + (index + 1) + '条评价时出错:', e);
        }
    });
    
    // 保存到本地
    const blob = new Blob([JSON.stringify(data, null, 2)], {type: 'application/json'});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `meituan_data_${new Date().getTime()}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    
    console.log('✅ 美团数据提取完成！');
    console.log('📊 经营数据:', data.metrics);
    console.log('📋 订单数量:', data.orders.length);
    console.log('💬 评价数量:', data.reviews.length);
    console.log('💾 数据已下载到本地');
    
    return data;
})();