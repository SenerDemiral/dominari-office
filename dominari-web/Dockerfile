# 1. Aşama: Build (İnşa)
FROM node:20-slim AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# 2. Aşama: Run (Çalıştırma)
FROM node:20-slim
WORKDIR /app
# Sadece build edilmiş dosyaları ve gerekli paketleri alıyoruz
COPY --from=builder /app/build ./build
COPY --from=builder /app/package.json ./package.json
COPY --from=builder /app/node_modules ./node_modules

EXPOSE 3000
ENV NODE_ENV=production
# SvelteKit adapter-node bu komutla çalışır
CMD ["node", "build/index.js"]