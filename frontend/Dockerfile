FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --silent || npm install
COPY . .
RUN npm run build
CMD ["npx", "serve", "-s", "dist", "-l", "3000"]
