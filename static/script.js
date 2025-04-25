// static/script.js
document.addEventListener('DOMContentLoaded', function() {
    console.log('Script.js loaded');
    
    // Check if SweetAlert2 is loaded
    if (typeof Swal === 'undefined') {
        console.error('SweetAlert2 is not defined in script.js!');
        // Try to load it dynamically as fallback
        const script = document.createElement('script');
        script.src = 'https://cdn.jsdelivr.net/npm/sweetalert2@11';
        document.head.appendChild(script);
    }
    
    // Load logs
    fetchLogs();
    
    // Initialize toggle switch based on current status
    const toggleSwitch = document.getElementById('toggleSwitch');
    const currentStatus = document.getElementById('status').textContent;
    toggleSwitch.checked = (currentStatus === '開啟');
    
    // Add event listener for toggle switch
    toggleSwitch.addEventListener('change', function() {
        const newState = this.checked;
        
        if (!newState) {
            // Turning OFF - show confirmation dialog
            Swal.fire({
                title: '確認關閉?',
                text: '您確定要關閉電源嗎?',
                icon: 'question',
                showCancelButton: true,
                confirmButtonColor: '#d33',
                cancelButtonColor: '#3085d6',
                confirmButtonText: '是的，關閉!',
                cancelButtonText: '取消'
            }).then((result) => {
                if (result.isConfirmed) {
                    // User confirmed turning off
                    controlRelay('off');
                } else {
                    // User cancelled, revert toggle switch
                    toggleSwitch.checked = true;
                }
            });
        } else {
            // Turning ON - no confirmation needed
            controlRelay('on');
        }
    });
});

function fetchLogs() {
    fetch('/api/logs')
        .then(response => response.json())
        .then(data => {
            const logsContainer = document.getElementById('logsContainer');
            logsContainer.innerHTML = '';
            
            data.logs.forEach(log => {
                const logItem = document.createElement('div');
                logItem.classList.add('log-item');
                logItem.innerHTML = `
                    <span class="timestamp">${log.timestamp}</span>
                    <span class="status ${log.status === '開啟' ? 'on' : 'off'}">${log.status}</span>
                `;
                logsContainer.appendChild(logItem);
            });
        })
        .catch(error => {
            console.error('Error fetching logs:', error);
            if (typeof Swal !== 'undefined') {
                Swal.fire('錯誤', '無法載入操作記錄', 'error');
            } else {
                alert('錯誤: 無法載入操作記錄');
            }
        });
}

function controlRelay(command) {
    fetch('/api/control', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ command: command })
    })
    .then(response => response.json())
    .then(data => {
        // Update status display
        document.getElementById('status').textContent = command === 'on' ? '開啟' : '關閉';
        
        // Ensure toggle switch matches status
        document.getElementById('toggleSwitch').checked = (command === 'on');
        
        // Show notification only for turning on (optional)
        if (command === 'on' && typeof Swal !== 'undefined') {
            // Simple notification when turning on (can be removed if no notification is desired)
            const Toast = Swal.mixin({
                toast: true,
                position: 'top-end',
                showConfirmButton: false,
                timer: 2000,
                timerProgressBar: true
            });
            
            Toast.fire({
                icon: 'success',
                title: '已開啟'
            });
        }
        
        // Refresh logs
        fetchLogs();
    })
    .catch(error => {
        console.error('Error controlling relay:', error);
        if (typeof Swal !== 'undefined') {
            Swal.fire('操作失敗', '控制繼電器失敗', 'error');
        } else {
            alert('錯誤: 控制繼電器失敗');
        }
    });
}