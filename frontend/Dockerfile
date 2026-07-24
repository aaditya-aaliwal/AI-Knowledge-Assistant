# syntax=docker/dockerfile:1.7
FROM node:22-alpine AS build

WORKDIR /app

ENV CI=true
ENV PNPM_HOME=/pnpm
ENV PATH=$PNPM_HOME:$PATH

RUN corepack enable

# This is a standalone application. Copy its manifest and lockfile only so
# source changes do not invalidate the dependency cache.
COPY package.json pnpm-lock.yaml ./
RUN --mount=type=cache,id=ai-knowledge-assistant-pnpm-store,target=/pnpm/store \
    pnpm config set confirmModulesPurge false && \
    pnpm fetch --frozen-lockfile

# node_modules is excluded by .dockerignore; dependencies are materialized only
# from this application's lockfile inside the Linux image.
COPY . .
RUN --mount=type=cache,id=ai-knowledge-assistant-pnpm-store,target=/pnpm/store \
    pnpm install --offline --frozen-lockfile

ARG VITE_API_BASE_URL=http://localhost:8000
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL
RUN pnpm run build

FROM nginx:1.27-alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
