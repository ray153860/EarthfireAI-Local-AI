$ErrorActionPreference = 'Stop'
try {
    Invoke-RestMethod -Uri 'http://127.0.0.1:11434/api/version' -TimeoutSec 2 | Out-Null
    Write-Host 'Ollama 已经在运行。'
    exit 0
} catch { }
$ollama = Get-Command ollama.exe -ErrorAction SilentlyContinue
if (-not $ollama) { throw '未找到 Ollama。请先从官方来源安装，并确认 ollama.exe 已加入 PATH。' }
Start-Process -FilePath $ollama.Source -ArgumentList 'serve' -WindowStyle Hidden
Write-Host '已启动 Ollama 服务；本脚本没有下载模型。'
