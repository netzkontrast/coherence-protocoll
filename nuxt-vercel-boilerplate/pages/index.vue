<template>
  <div class="min-h-screen bg-background">
    <header class="border-b">
      <div class="container mx-auto px-4 py-4">
        <h1 class="text-2xl font-bold">Nuxt Vercel Boilerplate</h1>
      </div>
    </header>
    <main class="container mx-auto px-4 py-8">
      <div class="space-y-6">
        <h2 class="text-xl">Willkommen bei deinem Nuxt 3 Boilerplate mit shadcn/ui</h2>
        <Button>shadcn Button</Button>
        <p>State Counter: {{ counter }}</p>
        <Button @click="increment">Increment</Button>
      </div>
    </main>
  </div>
</template>

<script setup>
const counter = useCounterStore()
</script>