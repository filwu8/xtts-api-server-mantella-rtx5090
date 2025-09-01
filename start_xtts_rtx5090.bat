@echo off
echo 启动支持RTX 5090的XTTS API服务器...
cd /d "xtts-api-server-mantella-rtx5090"
"xtts-api-server-mantella-rtx5090\.venv\Scripts\python.exe" -m xtts_api_server --device cuda --listen
pause
