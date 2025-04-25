// static/script.js
document.addEventListener('DOMContentLoaded', function() {
    const relayToggle = document.getElementById('relay-toggle');
    const statusValue = document.getElementById('status-value');
    const logsBody = document.getElementById('logs-body');
    
    // 初始化開關狀態
    fetchStatus();
    
    // 獲取操作日誌
    fetchLogs();
    
    // 開關切換事件
    relayToggle.addEventListener('change', function() {
        if (this.checked) {
            // 開啟操作不需要二次確認
            controlRelay('on');
        } else {
            // 關閉操作需要二次確認
            Swal.fire({
                title: '確認關閉繼電器？',
                text: '您確定要關閉繼電器嗎？',
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#4CAF50',
                cancelButtonColor: '#d33',
                confirmButtonText: '確認',
                cancelButtonText: '取消'
            }).then((result) => {
                if (result.isConfirmed) {
                    controlRelay('off');
                } else {
                    // 取消操作，恢復開關狀態
                    relayToggle.checked = true;
                }
            });
        }
    });
    
    // 定期更新狀態和日誌（每 10 秒）
    setInterval(() => {
        fetchStatus();
        fetchLogs();
    }, 10000);
    
    // 獲取當前狀態
    function fetchStatus() {
        fetch('/api/status')
            .then(response => response.json())
            .then(data => {
                statusValue.textContent = data.status;
                // 同步開關狀態
                relayToggle.checked = data.status === '開啟';
            })
            .catch(error => console.error('獲取狀態失敗：', error));
    }
    
    // 控制繼電器
    function controlRelay(command) {
        fetch('/api/control', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ command: command }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                statusValue.textContent = command === 'on' ? '開啟' : '關閉';
                
                // 顯示操作結果
                Swal.fire({
                    icon: 'success',
                    title: data.message,
                    showConfirmButton: false,
                    timer: 1500
                });
                
                // 更新日誌
                fetchLogs();
            } else {
                Swal.fire({
                    icon: 'error',
                    title: '操作失敗',
                    text: data.message
                });
                // 恢復開關狀態
                fetchStatus();
            }
        })
        .catch(error => {
            console.error('控制繼電器失敗：', error);
            Swal.fire({
                icon: 'error',
                title: '操作失敗',
                text: '無法連接到伺服器'
            });
            // 恢復開關狀態
            fetchStatus();
        });
    }
    
    // 獲取操作日誌
    function fetchLogs() {
        fetch('/api/logs')
            .then(response => response.json())
            .then(data => {
                // 清空原有日誌
                logsBody.innerHTML = '';
                
                // 填充新日誌
                data.logs.forEach(log => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${log.timestamp}</td>
                        <td>${log.status}</td>
                    `;
                    logsBody.appendChild(row);
                });
            })
            .catch(error => console.error('獲取日誌失敗：', error));
    }
});