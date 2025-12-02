# Nuxt Vercel Boilerplate

Ein Boilerplate für Nuxt 3 Projekte, optimiert für Vercel-Deployment, mit shadcn/ui und Pinia.

## Features

- **Nuxt 3**: Neueste Version des Vue.js Frameworks
- **shadcn/ui**: Moderne UI-Komponenten für Vue
- **Pinia**: State Management
- **Tailwind CSS**: Utility-First CSS Framework
- **Vercel**: Optimierte Konfiguration für Deployment

## Installation

1. Dependencies installieren:
   ```bash
   npm install
   ```

2. Entwicklungsserver starten:
   ```bash
   npm run dev
   ```

3. Build für Produktion:
   ```bash
   npm run build
   ```

## Deployment auf Vercel

1. Repository auf GitHub pushen
2. Auf Vercel importieren
3. Automatisches Deployment mit der vercel.json Konfiguration

## Struktur

- `pages/`: Seiten der App
- `components/ui/`: shadcn/ui Komponenten
- `stores/`: Pinia Stores
- `assets/css/`: Stylesheets

## State Management

Verwendet Pinia für State Management. Beispiel in `stores/counter.js`.

## UI Komponenten

shadcn/ui Komponenten sind in `components/ui/` verfügbar. Beispiel Button in `pages/index.vue`.