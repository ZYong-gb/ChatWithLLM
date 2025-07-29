// 当前状态
//let 声明的变量只在​​当前代码块​​（{} 内部）有效。
let currentAgent = "agent1";
let currentHistory = null;
let conversations = {
    agent1: {
        name: "市场分析助手",
        desc: "专业市场趋势分析和商业策略建议",
        history: {
            1: [
                { sender: "bot", text: "您好！我是市场分析助手，有什么可以帮您？", time: "10:30" },
                { sender: "user", text: "我需要一份关于AI行业的市场分析报告", time: "10:31" },
                { sender: "bot", text: "好的，我可以为您准备一份AI行业的市场分析报告。请问您需要关注哪些具体方面？时间范围是什么？", time: "10:31" }
            ],
            2: [
                { sender: "bot", text: "您好！市场分析助手为您服务。", time: "昨天 14:20" },
                { sender: "user", text: "请分析一下电动汽车市场的竞争格局", time: "昨天 14:21" },
                { sender: "bot", text: "电动汽车市场竞争激烈，特斯拉、比亚迪和大众集团是主要玩家。特斯拉在高端市场占据主导地位，而比亚迪在中端市场表现强劲。", time: "昨天 14:22" }
            ]
        }
    },
    agent2: {
        name: "技术支持专家",
        desc: "解决技术问题和提供IT支持",
        history: {
            1: [
                { sender: "bot", text: "您好！技术支持专家为您服务，请描述您的问题。", time: "09:15" },
                { sender: "user", text: "我的软件无法启动，显示错误代码0x80070005", time: "09:16" },
                { sender: "bot", text: "这个错误通常与权限问题相关，请尝试以管理员身份运行程序或检查文件权限设置。", time: "09:16" }
            ]
        }
    },
    agent3: {
        name: "内容创作助手",
        desc: "创作高质量文章和营销内容",
        history: {
            1: [
                { sender: "bot", text: "您好！我是内容创作助手，请问需要创作什么内容？", time: "15:40" },
                { sender: "user", text: "我需要一篇关于健康饮食的博客文章", time: "15:41" },
                { sender: "bot", text: "好的，健康饮食是一个很好的主题。您希望文章面向什么受众？长度要求是多少？", time: "15:41" }
            ]
        }
    }
};

// 页面事件监听
document.addEventListener('DOMContentLoaded', function() {//确保代码在 ​​HTML 文档完全加载并解析完成​​ 后执行（但不会等待图片等外部资源加载）
    // 默认显示首页
    //获取 ID 为 home-page 的元素（可能是某个页面容器），并为其添加 active 类名。
    document.getElementById('home-page').classList.add('active');
    
    // 移动端菜单切换
    document.querySelector('.menu-toggle').addEventListener('click', function() {
        document.querySelector('.sidebar').classList.toggle('active');
    });

    // 添加请求头
    document.getElementById('add-header-btn').addEventListener('click', function() {
        const container = document.getElementById('headers-container');//获取键值对容器​
        const newPair = document.createElement('div');//创建一个新的 <div> 元素，用于存放单个键值对（键输入框、值输入框和删除按钮）。
        newPair.className = 'key-value-pair';//为新创建的 <div> 元素设置类名 key-value-pair，用于 CSS 样式控制（如布局、间距等）。
        //设置新键值对的 HTML 内容​
        newPair.innerHTML = `
            <input type="text" class="key-value-input" placeholder="键">
            <input type="text" class="key-value-input" placeholder="值">
            <button class="remove-btn">
                <i class="fas fa-times"></i>
            </button>
        `;
        container.appendChild(newPair);  //将新键值对添加到容器中​
        //为删除按钮绑定点击事件​
        newPair.querySelector('.remove-btn').addEventListener('click', function() {
            container.removeChild(newPair);//从新创建的键值对 <div> 中，查找类名为 remove-btn 的删除按钮元素
        });
    });

    // 添加请求体
    document.getElementById('add-body-btn').addEventListener('click', function() {
        const container = document.getElementById('body-container');
        const newPair = document.createElement('div');
        newPair.className = 'key-value-pair';
        newPair.innerHTML = `
            <input type="text" class="key-value-input" placeholder="键">
            <input type="text" class="key-value-input" placeholder="值">
            <button class="remove-btn">
                <i class="fas fa-times"></i>
            </button>
        `;
        container.appendChild(newPair);
        
        newPair.querySelector('.remove-btn').addEventListener('click', function() {
            container.removeChild(newPair);
        });
    });

    // 移除按钮事件处理
    document.querySelectorAll('.remove-btn').forEach(button => {
        button.addEventListener('click', function() {
            this.parentElement.remove();
        });
    });

    // 创建Agent按钮事件
    document.getElementById('create-agent-btn').addEventListener('click', function() {
        const agentName = document.getElementById('agent-name').value;
        const agentDesc = document.getElementById('agent-desc').value;
        const agentUrl = document.getElementById('agent-url').value;
        
        // 表单验证
        let isValid = true;//声明一个布尔变量 isValid，并初始化为 true。
        if (agentName.trim() === '') { //agentName.trim()：去除 agentName 字符串两端的空白字符（如空格、换行符）。
            document.getElementById('name-error').style.display = 'block';
            isValid = false;//将 isValid 设置为 false，标记表单验证失败。
        } else {
            document.getElementById('name-error').style.display = 'none';
        }
        
        if (agentDesc.trim() === '') {
            document.getElementById('desc-error').style.display = 'block';
            isValid = false;
        } else {
            document.getElementById('desc-error').style.display = 'none';
        }
        if (agentUrl.trim() === '') {
            document.getElementById('url-error').style.display = 'block';
            isValid = false;
        } else {
            document.getElementById('url-error').style.display = 'none';
        }

        if (!isValid) {
            document.getElementById('error-alert').style.display = 'block';
            document.getElementById('error-message').textContent = '请填写所有必填字段！';
            document.getElementById('success-alert').style.display = 'none';
            return;
        }
        
        document.getElementById('error-alert').style.display = 'none';
        document.getElementById('success-alert').style.display = 'block';
        
        // 模拟创建成功
        setTimeout(() => {
            // 添加到侧边栏
            const newAgentId = 'agent' + (Object.keys(conversations).length + 1);
            const agentList = document.querySelector('.agent-list');
            
            const newAgent = document.createElement('div');
            newAgent.className = 'agent-item';
            newAgent.dataset.agent = newAgentId;
            newAgent.innerHTML = `
                <i class="fas fa-robot"></i>
                <span>${agentName}</span>
                <button class="delete-btn delete-agent" data-agent="${newAgentId}">
                    <i class="fas fa-trash"></i>
                </button>
            `;
            
            // 插入到创建按钮之前
            agentList.insertBefore(newAgent, document.getElementById('sidebar-create-agent'));
            
            // 添加点击事件
            newAgent.addEventListener('click', function() {
                switchAgent(this.dataset.agent);
            });
            
            // 添加删除事件
            newAgent.querySelector('.delete-btn').addEventListener('click', function(e) {
                e.stopPropagation();
                openConfirmDeleteModal(this.dataset.agent);
            });
            
            // 初始化新Agent的数据
            conversations[newAgentId] = {
                name: agentName,
                desc: agentDesc,
                history: {}
            };
            
            // 重置表单
            resetCreateForm();
            
            // 关闭创建弹窗
            document.getElementById('create-agent-modal').classList.remove('active');
            
            // 切换到新创建的Agent
            switchAgent(newAgentId);
        }, 1500);
    });

    // 导入智能体
    document.getElementById('import-agent-btn').addEventListener('click', function() {
        const input = document.getElementById('shared-agent-input');
        const agentId = input.value.trim();
        
        if (agentId) {
            // 模拟导入过程
            input.value = '';
            document.getElementById('success-alert').style.display = 'block';
            document.getElementById('success-alert').innerHTML = `
                <i class="fas fa-check-circle"></i> 正在导入智能体: ${agentId}...
            `;
            
            setTimeout(() => {
                document.getElementById('success-alert').innerHTML = `
                    <i class="fas fa-check-circle"></i> 智能体导入成功！
                `;
                
                // 添加导入的智能体到侧边栏
                const newAgentId = 'agent' + (Object.keys(conversations).length + 1);
                const agentList = document.querySelector('.agent-list');
                
                const newAgent = document.createElement('div');
                newAgent.className = 'agent-item';
                newAgent.dataset.agent = newAgentId;
                newAgent.innerHTML = `
                    <i class="fas fa-robot"></i>
                    <span>${agentName}</span>
                    <button class="delete-btn delete-agent" data-agent="${newAgentId}">
                        <i class="fas fa-trash"></i>
                    </button>
                `;
                
                // 插入到创建按钮之前
                agentList.insertBefore(newAgent, document.getElementById('sidebar-create-agent'));
                
                // 添加点击事件
                newAgent.addEventListener('click', function() {
                    switchAgent(this.dataset.agent);
                });
                
                // 添加删除事件
                newAgent.querySelector('.delete-btn').addEventListener('click', function(e) {
                    e.stopPropagation();
                    openConfirmDeleteModal(this.dataset.agent);
                });
                
                // 初始化导入Agent的数据
                conversations[newAgentId] = {
                    name: "导入的智能体",
                    desc: "通过分享链接导入的智能体",
                    history: {}
                };
                
                // 自动切换到导入的智能体
                setTimeout(() => {
                    switchAgent(newAgentId);
                }, 1000);
            }, 2000);
        }
    });

    // 删除智能体
    document.getElementById('confirm-delete').addEventListener('click', function() {
        const agentId = this.dataset.agent;
        
        // 从数据中删除
        delete conversations[agentId];
        
        // 从DOM中移除
        document.querySelector(`.agent-item[data-agent="${agentId}"]`).remove();
        
        // 关闭确认弹窗
        closeConfirmDeleteModal();
        
        // 如果当前显示的智能体是被删除的那个，切换到第一个智能体（如果还有的话）
        if (currentAgent === agentId) {
            const firstAgent = Object.keys(conversations)[0];
            if (firstAgent) {
                switchAgent(firstAgent);
            } else {
                // 没有智能体了，清空界面
                currentAgent = null;
                updateChatInterface();
                document.getElementById('current-agent-name').textContent = "无可用智能体";
            }
        }
    });

    // 删除历史记录
    function deleteHistory(historyId) {
        // 阻止事件冒泡
        event.stopPropagation();
        
        // 从当前智能体的历史记录中删除
        if (conversations[currentAgent] && conversations[currentAgent].history) {
            delete conversations[currentAgent].history[historyId];
        }
        
        // 从DOM中移除
        document.querySelector(`.history-item[data-history="${historyId}"]`).remove();
        
        // 如果当前显示的历史记录是被删除的那条，则切换到新对话
        if (currentHistory === historyId) {
            currentHistory = null;
            updateChatInterface();
            document.getElementById('conversation-status').textContent = "当前对话: 新对话";
        }
    }

    // 为历史记录删除按钮添加事件
    document.addEventListener('click', function(e) {
        if (e.target.closest('.delete-history')) {
            const button = e.target.closest('.delete-history');
            deleteHistory(button.dataset.history);
        }
    });

    // 为智能体删除按钮添加事件
    document.addEventListener('click', function(e) {
        if (e.target.closest('.delete-agent')) {
            const button = e.target.closest('.delete-agent');
            openConfirmDeleteModal(button.dataset.agent);
        }
    });

    // 分享功能（直接复制链接）
    document.getElementById('share-agent-btn').addEventListener('click', function() {
        const agentId = currentAgent;
        const shareLink = `https://dify.ai/agent/${agentId}`;
        
        // 复制到剪贴板
        navigator.clipboard.writeText(shareLink).then(() => {
            // 添加动画效果
            this.classList.add('copied');
            const originalText = this.innerHTML;
            this.innerHTML = '<i class="fas fa-check"></i> 已复制';
            
            // 2秒后恢复
            setTimeout(() => {
                this.classList.remove('copied');
                this.innerHTML = originalText;
            }, 2000);
        }).catch(err => {
            console.error('复制失败:', err);
            alert('复制失败，请手动复制链接');
        });
    });

    // 温度滑块事件
    // document.getElementById('temperature').addEventListener('input', function() {
    //     document.getElementById('temperature-value').textContent = this.value;
    // });
    
    // // 高级配置切换
    // document.getElementById('toggle-advanced').addEventListener('click', function() {
    //     const config = document.getElementById('advanced-config');
    //     config.style.display = config.style.display === 'block' ? 'none' : 'block';
    //     const icon = this.querySelector('i');
    //     if (config.style.display === 'block') {
    //         icon.className = 'fas fa-chevron-up';
    //     } else {
    //         icon.className = 'fas fa-cog';
    //     }
    // });
    
    // 表单取消按钮事件
    document.getElementById('cancel-create').addEventListener('click', function() {
        resetCreateForm();
        document.getElementById('create-agent-modal').classList.remove('active');
    });
    
    // 打开创建智能体弹窗
    document.getElementById('new-agent-btn').addEventListener('click', function() {
        resetCreateForm();
        document.getElementById('create-agent-modal').classList.add('active');
    });
    
    document.getElementById('sidebar-create-agent').addEventListener('click', function() {
        resetCreateForm();
        document.getElementById('create-agent-modal').classList.add('active');
    });
    
    // 关闭创建智能体弹窗
    document.getElementById('close-create-modal').addEventListener('click', function() {
        document.getElementById('create-agent-modal').classList.remove('active');
    });
    
    // 确认删除弹窗的取消按钮
    document.getElementById('cancel-delete').addEventListener('click', function() {
        closeConfirmDeleteModal();
    });
    
    // 确认删除弹窗的关闭按钮
    document.getElementById('close-confirm-modal').addEventListener('click', function() {
        closeConfirmDeleteModal();
    });
    
    // 默认选中第一个Agent
    document.querySelector('.agent-item').classList.add('active');
    
    // 为Agent添加点击事件
    document.querySelectorAll('.agent-item').forEach(item => {
        item.addEventListener('click', function() {
            switchAgent(this.dataset.agent);
        });
    });
});

// 重置创建表单
function resetCreateForm() {
    document.getElementById('agent-name').value = '';
    document.getElementById('agent-desc').value = '';
    document.getElementById('request-method').value = 'POST';
    document.getElementById("agent-url").value = '';
    // document.getElementById('agent-model').value = 'gpt-3.5';
    // document.getElementById('temperature').value = 0.7;
    // document.getElementById('temperature-value').textContent = '0.7';
    // document.getElementById('max-tokens').value = '1024';
    // document.getElementById('stop-sequences').value = '';
    
    // 重置请求头
    const headersContainer = document.getElementById('headers-container');
    while (headersContainer.children.length > 2) {
        headersContainer.removeChild(headersContainer.lastChild);
    }
    if (headersContainer.children.length >= 1) {
        headersContainer.children[0].querySelectorAll('.key-value-input')[0].value = 'Content-Type';
        headersContainer.children[0].querySelectorAll('.key-value-input')[1].value = 'application/json';
    }
    if (headersContainer.children.length >= 2) {
        headersContainer.children[1].querySelectorAll('.key-value-input')[0].value = 'Authorization';
        headersContainer.children[1].querySelectorAll('.key-value-input')[1].value = 'Bearer YOUR_API_KEY';
    }

    // 重置请求体
    const bodyContainer = document.getElementById('body-container');
    while (bodyContainer.children.length > 2) {
        bodyContainer.removeChild(bodyContainer.lastChild);
    }
    if (bodyContainer.children.length >= 1) {
        bodyContainer.children[0].querySelectorAll('.key-value-input')[0].value = 'model';
        bodyContainer.children[0].querySelectorAll('.key-value-input')[1].value = 'gpt-4';
    }
    if (bodyContainer.children.length >= 2) {
        bodyContainer.children[1].querySelectorAll('.key-value-input')[0].value = 'temperature';
        bodyContainer.children[1].querySelectorAll('.key-value-input')[1].value = '0.7';
    }

    // 隐藏提示
    document.getElementById('error-alert').style.display = 'none';
    document.getElementById('success-alert').style.display = 'none';
    
    // 隐藏错误提示
    document.getElementById('name-error').style.display = 'none';
    document.getElementById('desc-error').style.display = 'none';
    document.getElementById('url-error').style.display = 'none';
}

// 打开确认删除弹窗
function openConfirmDeleteModal(agentId) {
    document.getElementById('confirm-delete-modal').classList.add('active');
    document.body.style.overflow = 'hidden';
    
    // 设置当前要删除的agentId
    document.getElementById('confirm-delete').dataset.agent = agentId;
}

// 关闭确认删除弹窗
function closeConfirmDeleteModal() {
    document.getElementById('confirm-delete-modal').classList.remove('active');
    document.body.style.overflow = '';
}

// 切换Agent
function switchAgent(agentId) {
    currentAgent = agentId;
    currentHistory = null;
    
    // 更新UI
    document.querySelectorAll('.agent-item').forEach(item => {
        item.classList.remove('active');
    });
    document.querySelector(`.agent-item[data-agent="${agentId}"]`).classList.add('active');
    
    // 更新聊天界面
    updateChatInterface();
    
    // 更新历史记录
    updateHistoryList();
}

// 更新历史记录列表
function updateHistoryList() {
    const historyList = document.getElementById('history-list');
    historyList.innerHTML = '';
    
    if (conversations[currentAgent] && conversations[currentAgent].history) {
        const historyKeys = Object.keys(conversations[currentAgent].history);
        
        historyKeys.forEach(key => {
            const historyItem = conversations[currentAgent].history[key];
            if (historyItem.length > 0) {
            const historyTitle = historyItem[0].text.substring(0, 20) + (historyItem[0].text.length > 20 ? "..." : "");
            
            const historyElement = document.createElement('div');
            historyElement.className = 'history-item';
            historyElement.dataset.history = key;
            historyElement.innerHTML = `
                <i class="fas fa-comment"></i>
                <span>${historyTitle}</span>
                <button class="delete-btn delete-history" data-history="${key}">
                    <i class="fas fa-trash"></i>
                </button>
            `;
            
            historyList.appendChild(historyElement);
            
            // 添加点击事件
            historyElement.addEventListener('click', function() {
                const historyId = this.dataset.history;
                currentHistory = historyId;
                
                document.querySelectorAll('.history-item').forEach(item => {
                    item.classList.remove('active');
                });
                this.classList.add('active');
                
                updateChatInterface();
                document.getElementById('conversation-status').textContent = "当前对话: 历史记录 #" + historyId;
            });
        }
    });
}
}
