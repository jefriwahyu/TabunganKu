<template>
  <div class="fixed inset-0 overflow-hidden bg-gradient-to-br from-indigo-900 via-purple-800 to-pink-700">
    <!-- Animated Background Circles -->
    <div class="absolute inset-0 overflow-hidden">
      <div class="absolute top-20 left-10 w-72 h-72 bg-purple-400 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-blob"></div>
      <div class="absolute top-40 right-10 w-72 h-72 bg-pink-400 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-blob animation-delay-2000"></div>
      <div class="absolute -bottom-8 left-1/3 w-72 h-72 bg-indigo-400 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-blob animation-delay-4000"></div>
    </div>

    <!-- Main Content -->
    <div class="relative flex items-center justify-center min-h-screen p-8">
      <div class="text-center transition-all duration-1000 max-w-2xl" :class="{'opacity-0 scale-90': fadeOut, 'opacity-100 scale-100': !fadeOut}">
        
        <!-- Animated Logo with Glow -->
        <div class="mb-12 relative inline-block">
          <div class="absolute inset-0 bg-gradient-to-r from-yellow-300 via-pink-300 to-purple-300 rounded-full blur-2xl opacity-60 animate-pulse"></div>
          <div class="relative bg-white bg-opacity-20 backdrop-blur-lg rounded-3xl p-8 shadow-2xl border border-white border-opacity-30">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-24 w-24 mx-auto text-yellow-300 drop-shadow-2xl animate-bounce-slow" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M17 9V7a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2m2 4h10a2 2 0 002-2v-6a2 2 0 00-2-2H9a2 2 0 00-2 2v6a2 2 0 002 2zm7-5a2 2 0 11-4 0 2 2 0 014 0z" />
            </svg>
            <!-- Sparkle Effects -->
            <div class="absolute -top-2 -right-2 w-4 h-4 bg-yellow-300 rounded-full animate-ping"></div>
            <div class="absolute -bottom-2 -left-2 w-3 h-3 bg-pink-300 rounded-full animate-ping animation-delay-1000"></div>
          </div>
        </div>

        <!-- App Title with Gradient Text -->
        <h1 class="text-6xl pb-3 md:text-7xl font-black mb-8 bg-gradient-to-r from-yellow-200 via-pink-200 to-purple-200 bg-clip-text text-transparent drop-shadow-lg animate-fade-in">
          TabunganKu
        </h1>
        <br>
        <!-- Subtitle with elegant style -->
        <div class="mb-10 relative px-3">
          <div class="absolute inset-0 bg-gradient-to-r from-transparent via-white to-transparent h-px top-1/2 opacity-20"></div>
          <p class="relative text-lg md:text-xl text-yellow-100 font-light italic px-8 py-3 bg-gradient-to-br from-indigo-900/80 via-purple-800/80 to-pink-700/80 inline-block rounded-full backdrop-blur-sm border border-white/10">
            "Sedikit demi sedikit, lama-lama menjadi bukit."
          </p>
        </div>
        <br>
        <!-- Description -->
        <p class="text-base md:text-lg text-purple-100 font-medium mb-12 px-6">
          Kelola tabunganmu dengan <span class="text-yellow-300 font-bold">AI Scanner</span> 💰✨
        </p>
        <br>
        <!-- Loading Animation -->
        <div class="flex items-center justify-center space-x-3 mt-8">
          <div class="w-3 h-3 bg-yellow-300 rounded-full animate-bounce shadow-lg shadow-yellow-300/50"></div>
          <div class="w-3 h-3 bg-pink-300 rounded-full animate-bounce animation-delay-200 shadow-lg shadow-pink-300/50"></div>
          <div class="w-3 h-3 bg-purple-300 rounded-full animate-bounce animation-delay-400 shadow-lg shadow-purple-300/50"></div>
        </div>

      </div>
    </div>

    <!-- Bottom Decoration -->
    <div class="absolute bottom-0 left-0 right-0 h-1 bg-gradient-to-r from-yellow-400 via-pink-400 to-purple-400"></div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const fadeOut = ref(false)

onMounted(() => {
  setTimeout(() => {
    fadeOut.value = true
    setTimeout(() => {
      router.push('/login')
    }, 1000)
  }, 2500)
})
</script>

<style scoped>
@keyframes blob {
  0%, 100% {
    transform: translate(0, 0) scale(1);
  }
  25% {
    transform: translate(20px, -50px) scale(1.1);
  }
  50% {
    transform: translate(-20px, 20px) scale(0.9);
  }
  75% {
    transform: translate(50px, 50px) scale(1.05);
  }
}

@keyframes bounce-slow {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-20px);
  }
}

@keyframes fade-in {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-blob {
  animation: blob 7s infinite;
}

.animate-bounce-slow {
  animation: bounce-slow 2s ease-in-out infinite;
}

.animate-fade-in {
  animation: fade-in 1s ease-out;
}

.animation-delay-200 {
  animation-delay: 0.2s;
}

.animation-delay-400 {
  animation-delay: 0.4s;
}

.animation-delay-1000 {
  animation-delay: 1s;
}

.animation-delay-2000 {
  animation-delay: 2s;
}

.animation-delay-4000 {
  animation-delay: 4s;
}
</style>