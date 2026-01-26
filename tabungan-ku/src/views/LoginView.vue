<template>
  <div class="min-h-screen w-full flex items-center justify-center bg-gradient-to-br from-indigo-900 via-purple-800 to-pink-700 p-6 overflow-hidden relative">
    
    <!-- Animated Background Circles -->
    <div class="absolute inset-0 overflow-hidden">
      <div class="absolute top-20 -left-20 w-96 h-96 bg-purple-400 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob"></div>
      <div class="absolute top-40 -right-20 w-96 h-96 bg-pink-400 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob animation-delay-2000"></div>
      <div class="absolute -bottom-20 left-1/3 w-96 h-96 bg-indigo-400 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob animation-delay-4000"></div>
    </div>

    <!-- Login Card -->
    <div class="relative bg-white/95 backdrop-blur-xl p-10 rounded-3xl shadow-2xl w-full max-w-md transform transition-all duration-500 hover:scale-[1.02] border border-white/20">
      
      <!-- Logo/Icon with Animation -->
      <div class="flex justify-center mb-8">
        <div class="relative">
          <div class="absolute inset-0 bg-gradient-to-r from-yellow-300 via-pink-300 to-purple-300 rounded-full blur-xl opacity-60 animate-pulse"></div>
          <div class="relative bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 p-5 rounded-2xl shadow-lg">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-14 w-14 text-white drop-shadow-lg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 9V7a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2m2 4h10a2 2 0 002-2v-6a2 2 0 00-2-2H9a2 2 0 00-2 2v6a2 2 0 002 2zm7-5a2 2 0 11-4 0 2 2 0 014 0z" />
            </svg>
          </div>
        </div>
      </div>

      <!-- Title -->
      <div class="text-center mb-8 pt-3">
        <h2 class="text-4xl font-black mb-3 pb-3 bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 bg-clip-text text-transparent">
          Login Bos 
        </h2>
      </div>

      <!-- Login Form -->
      <form @submit.prevent="handleLogin" class="space-y-7">
        
        <!-- Username Field -->
        <div class="space-y-2.5">
          <label class="block text-gray-700 text-sm font-bold ml-1">Username</label>
          <div class="relative group">
            <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-400 group-focus-within:text-purple-600 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
            </div>
            <input 
              v-model="username"
              type="text" 
              class="w-full pl-12 pr-4 py-3.5 bg-gray-50 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-purple-500 focus:bg-white outline-none transition-all duration-200 placeholder-gray-400" 
              placeholder="Masukkan username"
              required
            />
          </div>
        </div>

        <!-- Password Field -->
        <div class="space-y-2.5">
          <label class="block text-gray-700 text-sm font-bold ml-1">Password</label>
          <div class="relative group">
            <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-400 group-focus-within:text-purple-600 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
              </svg>
            </div>
            <input 
              v-model="password"
              type="password" 
              class="w-full pl-12 pr-4 py-3.5 bg-gray-50 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-purple-500 focus:bg-white outline-none transition-all duration-200 placeholder-gray-400" 
              placeholder="Masukkan password"
              required
            />
          </div>
        </div>

        <!-- Login Button -->
        <div class="pt-4">
          <button 
            type="submit" 
            class="w-full bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 text-white font-bold py-4 rounded-xl hover:from-indigo-700 hover:via-purple-700 hover:to-pink-700 transform hover:-translate-y-1 hover:shadow-2xl transition-all duration-200 shadow-lg relative overflow-hidden group"
          >
            <span class="relative z-10 flex items-center justify-center gap-2">
              <span>Masuk Sekarang</span>
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 group-hover:translate-x-1 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6" />
              </svg>
            </span>
            <div class="absolute inset-0 bg-gradient-to-r from-yellow-400 via-pink-400 to-purple-400 opacity-0 group-hover:opacity-20 transition-opacity"></div>
          </button>
        </div>
      </form>

      <!-- Decorative Elements -->
      <div class="absolute -top-1 -right-1 w-20 h-20 bg-gradient-to-br from-yellow-300 to-pink-300 rounded-full blur-2xl opacity-30"></div>
      <div class="absolute -bottom-1 -left-1 w-20 h-20 bg-gradient-to-br from-purple-300 to-indigo-300 rounded-full blur-2xl opacity-30"></div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const username = ref('')
const password = ref('')

const handleLogin = () => {
  // Simple validation
  if (username.value && password.value) {
    // Save user to localStorage
    const userData = {
      username: username.value,
      loginTime: new Date().toISOString()
    }
    localStorage.setItem('user', JSON.stringify(userData))
    router.push('/dashboard')
  }
}
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

.animate-blob {
  animation: blob 7s infinite;
}

.animation-delay-2000 {
  animation-delay: 2s;
}

.animation-delay-4000 {
  animation-delay: 4s;
}
</style>