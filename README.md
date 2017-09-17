# IP代理池

## 使用方法
1. 将refresh.py添加到定时任务(crontab)，定时刷新代理池的ip
`corntab -e`在末尾添加一行任务，每10分钟运行一次该脚本
```sh
*/10 * * * * /usr/bin/python3 /your_refresh_file_path/refresh.py
```

2. 运行接口程序 `python3 api.py`

3. Enjoy! `http://127.0.0.1:5000/proxy?type=https&all=true`
```json
{
    "code": 0,
    "data": [
        "125.118.147.246:808",
        ...
    ]
}
```
