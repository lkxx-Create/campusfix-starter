FROM python:3.13-slim

WORKDIR /app

# 先复制依赖清单：依赖不变时可复用缓存层
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 再复制代码：改代码只重建这一层
COPY . .

EXPOSE 5000

# 首次启动时初始化数据库（instance/ 被 .dockerignore 排除，镜像里不带数据）
# 已存在则跳过，避免清空数据；课20 会用 Volume 持久化
CMD ["sh", "-c", "[ -f instance/campusfix.db ] || python init_db.py; exec gunicorn -w 2 -b 0.0.0.0:5000 app:app"]
