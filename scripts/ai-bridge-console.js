// Browser AI 控制台助手
// 使用方法：
// 1. 在 Chrome 打开 Gemini 或 Manus
// 2. 按 F12 打开控制台
// 3. 复制粘贴此代码并按回车
// 4. 按页面提示操作

(function() {
  'use strict';
  
  const AI_BRIDGE = {
    version: '1.0.0',
    platform: window.location.hostname.includes('gemini') ? 'gemini' : 
              window.location.hostname.includes('manus') ? 'manus' : 'unknown',
    
    init() {
      console.log(`🤖 AI Bridge v${this.version} initialized for ${this.platform}`);
      this.createUI();
      this.startMonitoring();
    },
    
    createUI() {
      const div = document.createElement('div');
      div.id = 'ai-bridge-panel';
      div.style.cssText = `
        position: fixed;
        top: 10px;
        right: 10px;
        width: 300px;
        background: #1a1a2e;
        color: #eee;
        padding: 15px;
        border-radius: 8px;
        font-family: monospace;
        z-index: 999999;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
      `;
      div.innerHTML = `
        <h3 style="margin:0 0 10px 0;color:#4ecca3">🌉 AI Bridge</h3>
        <div id="ai-bridge-status">Status: Ready</div>
        <div style="margin-top:10px">
          <input type="text" id="ai-bridge-input" placeholder="Enter task..." 
                 style="width:100%;padding:5px;border-radius:4px;border:none;box-sizing:border-box">
          <button onclick="AI_BRIDGE.executeTask()" 
                  style="margin-top:8px;width:100%;padding:8px;background:#4ecca3;border:none;border-radius:4px;cursor:pointer">
            Execute
          </button>
        </div>
        <div id="ai-bridge-output" style="margin-top:10px;max-height:200px;overflow:auto;font-size:12px"></div>
      `;
      document.body.appendChild(div);
    },
    
    executeTask() {
      const input = document.getElementById('ai-bridge-input');
      const task = input.value.trim();
      if (!task) return;
      
      this.log(`Task: ${task}`);
      
      // Platform-specific execution
      if (this.platform === 'gemini') {
        this.executeOnGemini(task);
      } else if (this.platform === 'manus') {
        this.executeOnManus(task);
      }
      
      input.value = '';
    },
    
    executeOnGemini(task) {
      // Find Gemini input area
      const inputs = document.querySelectorAll('textarea, input');
      let inputEl = null;
      
      for (const el of inputs) {
        if (el.placeholder && el.placeholder.toLowerCase().includes('enter')) {
          inputEl = el;
          break;
        }
      }
      
      if (!inputEl) {
        this.log('❌ Could not find Gemini input field');
        return;
      }
      
      // Set value and trigger input
      inputEl.value = task;
      inputEl.dispatchEvent(new Event('input', { bubbles: true }));
      
      // Find and click send button
      setTimeout(() => {
        const sendButtons = document.querySelectorAll('button');
        for (const btn of sendButtons) {
          if (btn.innerText.toLowerCase().includes('send') || 
              btn.getAttribute('aria-label')?.toLowerCase().includes('send')) {
            btn.click();
            this.log('✅ Task sent to Gemini');
            this.captureResponse();
            break;
          }
        }
      }, 100);
    },
    
    executeOnManus(task) {
      this.log('Manus automation - detecting interface...');
      // Similar implementation for Manus
      const inputs = document.querySelectorAll('textarea, input[type="text"]');
      if (inputs.length > 0) {
        inputs[0].value = task;
        inputs[0].dispatchEvent(new Event('input', { bubbles: true }));
        this.log('✅ Task entered');
      }
    },
    
    captureResponse() {
      this.log('📡 Monitoring for response...');
      
      // Check for response every 2 seconds
      const checkInterval = setInterval(() => {
        const responses = document.querySelectorAll('[data-testid="conversation-turn"]');
        if (responses.length > 0) {
          const lastResponse = responses[responses.length - 1];
          const text = lastResponse.innerText;
          
          if (text && text.length > 50) {
            this.log(`📝 Response captured (${text.length} chars)`);
            this.saveResponse(text);
            clearInterval(checkInterval);
          }
        }
      }, 2000);
      
      // Stop after 60 seconds
      setTimeout(() => clearInterval(checkInterval), 60000);
    },
    
    saveResponse(text) {
      // Create a downloadable file
      const blob = new Blob([text], { type: 'text/plain' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `ai-response-${Date.now()}.txt`;
      a.click();
      URL.revokeObjectURL(url);
      
      this.log('💾 Response saved to file');
    },
    
    log(message) {
      const output = document.getElementById('ai-bridge-output');
      const time = new Date().toLocaleTimeString();
      output.innerHTML += `<div>[${time}] ${message}</div>`;
      output.scrollTop = output.scrollHeight;
      console.log(`[AI Bridge] ${message}`);
    },
    
    startMonitoring() {
      // Monitor for page changes
      const observer = new MutationObserver((mutations) => {
        // Detect new content
      });
      
      observer.observe(document.body, {
        childList: true,
        subtree: true
      });
    }
  };
  
  // Expose globally
  window.AI_BRIDGE = AI_BRIDGE;
  
  // Auto-init
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => AI_BRIDGE.init());
  } else {
    AI_BRIDGE.init();
  }
  
})();
