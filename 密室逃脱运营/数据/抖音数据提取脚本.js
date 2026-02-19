// 抖音来客数据提取脚本
// 在浏览器控制台(F12)中运行

(function extractDouyinData() {
    console.log('🎵 开始提取抖音来客数据...');
    
    const data = {
        platform: '抖音来客',
        extractTime: new Date().toISOString(),
        url: window.location.href,
        videos: [],
        summary: {}
    };
    
    // 提取视频数据（根据实际页面结构调整选择器）
    const videoItems = document.querySelectorAll('.video-item, [class*="video"], [class*="item"]');
    
    videoItems.forEach((item, index) => {
        try {
            const video = {
                index: index + 1,
                title: item.querySelector('[class*="title"], h1, h2, h3')?.textContent?.trim() || '',
                playCount: item.querySelector('[class*="play"], [class*="view"]')?.textContent?.trim() || '',
                likeCount: item.querySelector('[class*="like"], [class*="digg"]')?.textContent?.trim() || '',
                commentCount: item.querySelector('[class*="comment"]')?.textContent?.trim() || '',
                shareCount: item.querySelector('[class*="share"]')?.textContent?.trim() || '',
                publishTime: item.querySelector('[class*="time"], [class*="date"]')?.textContent?.trim() || ''
            };
            
            // 只保存有数据的记录
            if (video.title || video.playCount) {
                data.videos.push(video);
            }
        } catch (e) {
            console.log('提取第' + (index + 1) + '个视频时出错:', e);
        }
    });
    
    // 计算汇总数据
    data.summary = {
        totalVideos: data.videos.length,
        pageTitle: document.title,
        extractSuccess: data.videos.length > 0
    };
    
    // 保存到本地
    const blob = new Blob([JSON.stringify(data, null, 2)], {type: 'application/json'});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `douyin_data_${new Date().getTime()}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    
    console.log('✅ 抖音数据提取完成！');
    console.log('📊 提取了', data.videos.length, '条视频数据');
    console.log('💾 数据已下载到本地');
    
    return data;
})();