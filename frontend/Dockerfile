FROM node:18-alpine AS deps

WORKDIR /app

# Instalar dependências com base em package-lock.json para cache mais eficiente
COPY package.json package-lock.json* ./
RUN npm ci

# Construir a aplicação
FROM node:18-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .

# Configurar variáveis de ambiente para build
ENV NEXT_TELEMETRY_DISABLED 1

RUN npm run build

# Imagem de produção
FROM node:18-alpine AS runner
WORKDIR /app

ENV NODE_ENV production
ENV NEXT_TELEMETRY_DISABLED 1

# Copiar apenas os arquivos necessários
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json

# Expor porta e iniciar aplicação
EXPOSE 3000
CMD ["npm", "start"] 