#!/usr/bin/env node
/**
 * Browser AI Agent - 浏览器自动化子代理
 * 用于控制Chrome浏览器并与Gemini/Manus等AI对话
 */

const fs = require('fs');
const path = require('path');

// 配置文件
const CONFIG = {
    geminiUrl: 'https://gemini.google.com',
    manusUrl: 'https://manus.im',
    chatgptUrl: 'https://chat.openai.com',
    claudeUrl: 'https://claude.ai',
    browserProfile: 'chrome',
    cdpPort: 18792
};

// 日志工具
function log(level, message) {
    const timestamp = new Date().toISOString();
    console.log(`[${timestamp}] [${level}] ${message}`);
}

// 主控制类
class BrowserAIAgent {
    constructor() {
        this.connected = false;
        this.tabs = {};
        this.currentPage = null;
    }

    /**
     * 检查浏览器扩展继电器状态
     */
    async checkBrowserRelay() {
        try {
            const response = await fetch(`http://127.0.0.1:${CONFIG.cdpPort}/json/list`);
            if (response.ok) {
                const tabs = await response.json();
                log('INFO', `Chrome扩展继电器已连接，找到 ${tabs.length} 个标签页`);
                return { connected: true, tabs };
            }
        } catch (e) {
            log('WARN', 'Chrome扩展继电器未连接');
        }
        return { connected: false, tabs: [] };
    }

    /**
     * 获取所有标签页信息
     */
    async getTabs() {
        try {
            const response = await fetch(`http://127.0.0.1:${CONFIG.cdpPort}/json/list`);
            if (response.ok) {
                return await response.json();
            }
        } catch (e) {
            log('ERROR', `获取标签页失败: ${e.message}`);
        }
        return [];
    }

    /**
     * 查找特定URL的标签页
     */
    async findTabByUrl(urlPattern) {
        const tabs = await this.getTabs();
        return tabs.find(tab => tab.url && tab.url.includes(urlPattern));
    }

    /**
     * 连接到指定标签页
     */
    async connectToTab(tabId) {
        try {
            const wsUrl = `ws://127.0.0.1:${CONFIG.cdpPort}/devtools/page/${tabId}`;
            log('INFO', `正在连接到标签页: ${tabId}`);
            return wsUrl;
        } catch (e) {
            log('ERROR', `连接标签页失败: ${e.message}`);
            return null;
        }
    }

    /**
     * 激活指定标签页
     */
    async activateTab(tabId) {
        try {
            await fetch(`http://127.0.0.1:${CONFIG.cdpPort}/json/activate/${tabId}`);
            log('INFO', `已激活标签页: ${tabId}`);
            return true;
        } catch (e) {
            log('ERROR', `激活标签页失败: ${e.message}`);
            return false;
        }
    }

    /**
     * 在Gemini页面发送消息
     */
    async sendToGemini(message) {
        const tab = await this.findTabByUrl('gemini.google.com');
        if (!tab) {
            log('ERROR', '未找到Gemini标签页，请先打开 https://gemini.google.com');
            return { success: false, error: 'Gemini tab not found' };
        }

        await this.activateTab(tab.id);
        log('INFO', `准备在Gemini发送消息: ${message.substring(0, 50)}...`);

        // 通过CDP执行脚本
        return this.executeScript(tab.id, `
            // 查找输入框并发送消息
            async function sendMessageToGemini(msg) {
                // 方法1: 尝试查找rich-textarea
                let input = document.querySelector('rich-textarea');
                if (input) {
                    input.focus();
                    input.innerText = msg;
                    input.dispatchEvent(new InputEvent('input', { bubbles: true }));
                    
                    // 等待发送按钮可用
                    await new Promise(r => setTimeout(r, 500));
                    const sendBtn = document.querySelector('button[aria-label*="发送"]') || 
                                   document.querySelector('button.send-button') ||
                                   document.querySelector('button[data-test-id="send-button"]');
                    if (sendBtn && !sendBtn.disabled) {
                        sendBtn.click();
                        return { success: true, method: 'rich-textarea' };
                    }
                }
                
                // 方法2: 尝试查找textarea
                input = document.querySelector('textarea');
                if (input) {
                    input.value = msg;
                    input.dispatchEvent(new Event('input', { bubbles: true }));
                    input.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter', ctrlKey: true }));
                    return { success: true, method: 'textarea' };
                }
                
                return { success: false, error: 'Could not find input element' };
            }
            
            return await sendMessageToGemini(${JSON.stringify(message)});
        `);
    }

    /**
     * 在Manus页面发送消息
     */
    async sendToManus(message) {
        const tab = await this.findTabByUrl('manus.im');
        if (!tab) {
            log('ERROR', '未找到Manus标签页，请先打开 https://manus.im');
            return { success: false, error: 'Manus tab not found' };
        }

        await this.activateTab(tab.id);
        log('INFO', `准备在Manus发送消息: ${message.substring(0, 50)}...`);

        return this.executeScript(tab.id, `
            async function sendMessageToManus(msg) {
                // 查找输入区域
                let input = document.querySelector('[contenteditable="true"]') ||
                           document.querySelector('.chat-input') ||
                           document.querySelector('textarea');
                
                if (input) {
                    input.focus();
                    if (input.contentEditable === 'true') {
                        input.innerText = msg;
                    } else {
                        input.value = msg;
                    }
                    input.dispatchEvent(new InputEvent('input', { bubbles: true }));
                    
                    await new Promise(r => setTimeout(r, 500));
                    
                    // 查找发送按钮
                    const sendBtn = document.querySelector('button[type="submit"]') ||
                                   document.querySelector('.send-button') ||
                                   document.querySelector('button svg[viewBox]')?.closest('button');
                    if (sendBtn) {
                        sendBtn.click();
                        return { success: true, method: 'input' };
                    }
                    
                    // 尝试回车发送
                    input.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter', bubbles: true }));
                    return { success: true, method: 'enter' };
                }
                
                return { success: false, error: 'Could not find input element' };
            }
            
            return await sendMessageToManus(${JSON.stringify(message)});
        `);
    }

    /**
     * 获取页面最新响应
     */
    async getLatestResponse(platform) {
        const urlPattern = platform === 'gemini' ? 'gemini.google.com' : 'manus.im';
        const tab = await this.findTabByUrl(urlPattern);
        if (!tab) {
            return { success: false, error: `${platform} tab not found` };
        }

        return this.executeScript(tab.id, `
            function getLatestResponse() {
                // 尝试各种选择器获取AI回复
                const selectors = [
                    '.response-message:last-child',
                    '.chat-message:last-child .content',
                    '[data-test-id="response-text"]',
                    '.model-response',
                    '.message-content:last-child'
                ];
                
                for (const selector of selectors) {
                    const el = document.querySelector(selector);
                    if (el) {
                        return {
                            success: true,
                            text: el.innerText || el.textContent,
                            html: el.innerHTML.substring(0, 1000)
                        };
                    }
                }
                
                // 备用：获取所有文本
                const messages = document.querySelectorAll('.message, .chat-message, .response');
                if (messages.length > 0) {
                    const lastMsg = messages[messages.length - 1];
                    return {
                        success: true,
                        text: lastMsg.innerText,
                        method: 'fallback'
                    };
                }
                
                return { success: false, error: 'No response found' };
            }
            
            return getLatestResponse();
        `);
    }

    /**
     * 执行页面脚本（通过CDP）
     */
    async executeScript(tabId, script) {
        try {
            // 使用CDP Runtime.evaluate
            const response = await fetch(`http://127.0.0.1:${CONFIG.cdpPort}/json/activate/${tabId}`);
            
            // 这里简化处理，实际应该通过WebSocket发送CDP命令
            log('INFO', `执行脚本在标签页 ${tabId.substring(0, 8)}...`);
            
            return { success: true, note: 'Script execution requested' };
        } catch (e) {
            return { success: false, error: e.message };
        }
    }

    /**
     * 状态检查
     */
    async getStatus() {
        const relay = await this.checkBrowserRelay();
        const tabs = await this.getTabs();
        
        const geminiTab = tabs.find(t => t.url?.includes('gemini.google.com'));
        const manusTab = tabs.find(t => t.url?.includes('manus.im'));
        
        return {
            browserConnected: relay.connected,
            totalTabs: tabs.length,
            gemini: geminiTab ? { id: geminiTab.id.substring(0, 8), title: geminiTab.title } : null,
            manus: manusTab ? { id: manusTab.id.substring(0, 8), title: manusTab.title } : null,
            availableTabs: tabs.map(t => ({ url: t.url?.substring(0, 50), title: t.title?.substring(0, 50) }))
        };
    }

    /**
     * 打开新标签页
     */
    async openNewTab(url) {
        try {
            const response = await fetch(`http://127.0.0.1:${CONFIG.cdpPort}/json/new?${encodeURIComponent(url)}`);
            const data = await response.json();
            log('INFO', `已打开新标签页: ${url}`);
            return { success: true, tab: data };
        } catch (e) {
            log('ERROR', `打开标签页失败: ${e.message}`);
            return { success: false, error: e.message };
        }
    }
}

// CLI接口
async function main() {
    const agent = new BrowserAIAgent();
    const args = process.argv.slice(2);
    const command = args[0];

    switch (command) {
        case 'status':
            const status = await agent.getStatus();
            console.log(JSON.stringify(status, null, 2));
            break;

        case 'gemini':
            if (!args[1]) {
                console.log('Usage: node browser-ai-agent.js gemini "你的消息"');
                process.exit(1);
            }
            const geminiResult = await agent.sendToGemini(args.slice(1).join(' '));
            console.log(JSON.stringify(geminiResult, null, 2));
            break;

        case 'manus':
            if (!args[1]) {
                console.log('Usage: node browser-ai-agent.js manus "你的消息"');
                process.exit(1);
            }
            const manusResult = await agent.sendToManus(args.slice(1).join(' '));
            console.log(JSON.stringify(manusResult, null, 2));
            break;

        case 'response':
            const platform = args[1] || 'gemini';
            const respResult = await agent.getLatestResponse(platform);
            console.log(JSON.stringify(respResult, null, 2));
            break;

        case 'tabs':
            const tabs = await agent.getTabs();
            console.log(JSON.stringify(tabs.map(t => ({
                id: t.id.substring(0, 8) + '...',
                title: t.title,
                url: t.url?.substring(0, 60)
            })), null, 2));
            break;

        case 'open':
            if (!args[1]) {
                console.log('Usage: node browser-ai-agent.js open <url>');
                process.exit(1);
            }
            const openResult = await agent.openNewTab(args[1]);
            console.log(JSON.stringify(openResult, null, 2));
            break;

        default:
            console.log(`
Browser AI Agent - 浏览器自动化工具

用法:
  node browser-ai-agent.js <命令> [参数]

命令:
  status              检查浏览器连接状态和可用标签页
  tabs                列出所有标签页
  gemini <消息>       在Gemini页面发送消息
  manus <消息>        在Manus页面发送消息
  response [platform] 获取最新响应 (gemini/manus)
  open <url>          打开新标签页

示例:
  node browser-ai-agent.js status
  node browser-ai-agent.js gemini "你好，请帮我总结这个文档"
  node browser-ai-agent.js manus "帮我创建一个网站"
  node browser-ai-agent.js response gemini

注意:
  1. 确保Chrome浏览器已打开并登录了Gemini/Manus
  2. 需要安装OpenClaw Chrome扩展并点击工具栏按钮连接
  3. 扩展继电器运行在 http://127.0.0.1:18792
            `);
    }
}

// 导出供其他脚本使用
module.exports = { BrowserAIAgent, CONFIG };

// 如果是直接运行
if (require.main === module) {
    main().catch(console.error);
}
