# Base image
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Install pnpm (recommended way: via corepack)
RUN corepack enable && corepack prepare pnpm@latest --activate

# Copy package files
COPY package.json pnpm-lock.yaml* ./

# Install dependencies
RUN pnpm install --frozen-lockfile

# Copy source code
COPY . .

# Build your app (if needed)
RUN pnpm build

# Expose port (example: 3000)
EXPOSE 3000

# Start the app
CMD ["pnpm", "start"]
