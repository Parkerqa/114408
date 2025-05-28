# 1. 建構階段 - 使用官方 Node 映像檔
FROM node:18-alpine AS builder

# 設定工作目錄
WORKDIR /app

# 複製 package 檔案並安裝依賴
COPY package.json package-lock.json* ./
RUN npm install

# 複製其他所有檔案（包含 .env）
COPY . .

# 設定 NODE_ENV 為 production 並打包 Next.js 專案
ENV NODE_ENV=production
RUN npm run build

# 2. 執行階段 - 精簡執行環境
FROM node:18-alpine AS runner

# 設定工作目錄
WORKDIR /app

# 複製執行階段需要的檔案
COPY --from=builder /app/package.json ./
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/.env ./.env

# 設定環境變數
ENV NODE_ENV=production
ENV PORT=3000

# 開放 port
EXPOSE 3000

# 預設啟動指令
CMD ["npm", "start"]
