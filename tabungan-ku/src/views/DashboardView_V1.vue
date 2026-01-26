<template>
  <div class="min-h-screen bg-gray-50 flex flex-col">
    <!-- ==================== NAVIGATION TABS ==================== -->
    <nav class="bg-white shadow-md p-4 flex justify-center gap-4 sticky top-0 z-10">
      <button 
        @click="currentTab = 'tabungan'"
        :disabled="currentTab === 'tabungan'"
        :class="currentTab === 'tabungan' 
          ? 'bg-gray-300 text-gray-600 cursor-not-allowed' 
          : 'bg-blue-600 text-white hover:bg-blue-700'"
        class="px-8 py-3 rounded-full font-bold transition-all shadow-sm"
      >
        Tabungan
      </button>
      <button 
        @click="currentTab = 'riwayat'"
        :disabled="currentTab === 'riwayat'"
        :class="currentTab === 'riwayat' 
          ? 'bg-gray-300 text-gray-600 cursor-not-allowed' 
          : 'bg-green-600 text-white hover:bg-green-700'"
        class="px-8 py-3 rounded-full font-bold transition-all shadow-sm"
      >
        Riwayat Bongkar
      </button>
    </nav>

    <!-- ==================== MAIN CONTENT ==================== -->
    <main class="p-6 max-w-6xl mx-auto w-full">
      
      <!-- ========== TAB: TABUNGAN AKTIF ========== -->
      <div v-if="currentTab === 'tabungan'">
        <div class="flex justify-between items-center mb-8">
          <h2 class="text-3xl font-black text-gray-800 uppercase tracking-tight">
            Daftar Tabungan Aktif
          </h2>
          <button 
            @click="showCreateModal = true" 
            class="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-6 py-3 rounded-xl font-bold hover:shadow-lg hover:scale-105 transition-all"
          >
            + Buat Tabungan
          </button>
        </div>

        <!-- Empty State -->
        <div v-if="activePlans.length === 0" class="text-center py-20 bg-white rounded-3xl border-2 border-dashed border-gray-200 shadow-sm">
          <div class="text-7xl mb-4">💰</div>
          <p class="text-gray-400 font-semibold text-lg">Belum ada tabungan aktif.</p>
          <p class="text-gray-300 text-sm mt-2">Klik tombol "+ Buat Tabungan" untuk memulai!</p>
        </div>

        <!-- Savings List -->
        <div v-else class="grid gap-4">
          <div 
            v-for="plan in paginatedActivePlans" 
            :key="plan.id" 
            class="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 flex justify-between items-center hover:shadow-md hover:border-blue-200 transition-all"
          >
            <div class="flex items-center gap-4">
              <div class="w-14 h-14 bg-gradient-to-br from-blue-400 to-purple-500 rounded-2xl flex items-center justify-center text-white font-bold text-2xl shadow-lg">
                💰
              </div>
              <div>
                <h3 class="font-bold text-xl text-gray-800">{{ plan.name }}</h3>
                <p class="text-sm text-gray-500 mt-1">
                  Target: <span class="font-semibold">{{ plan.currency }} {{ formatNumber(plan.target_amount) }}</span>
                </p>
              </div>
            </div>
            <div class="flex items-center gap-3">
              <button 
                @click="openDetail(plan)" 
                class="bg-blue-50 text-blue-600 px-5 py-2.5 rounded-xl font-bold hover:bg-blue-100 transition"
              >
                Buka
              </button>
              <div class="relative">
                <button 
                  @click="toggleMenu(plan.id)" 
                  class="text-gray-400 hover:text-gray-600 hover:bg-gray-100 p-2 rounded-lg text-2xl font-bold transition"
                >
                  ⋮
                </button>
                <div 
                  v-if="showMenu === plan.id" 
                  class="absolute right-0 mt-2 w-40 bg-white rounded-xl shadow-xl border border-gray-200 z-20 overflow-hidden"
                >
                  <button 
                    @click="editPlan(plan)" 
                    class="block w-full text-left px-4 py-3 hover:bg-blue-50 text-gray-700 font-medium transition"
                  >
                    ✏️ Edit
                  </button>
                  <button 
                    @click="deletePlan(plan)" 
                    class="block w-full text-left px-4 py-3 hover:bg-red-50 text-red-600 font-medium transition"
                  >
                    🗑️ Hapus
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Pagination -->
        <div v-if="totalPages > 1" class="mt-8 flex justify-center items-center gap-2">
          <button 
            @click="currentPage--" 
            :disabled="currentPage === 1" 
            class="px-5 py-2.5 border border-gray-300 rounded-xl font-semibold transition"
            :class="currentPage === 1 ? 'text-gray-300 cursor-not-allowed' : 'text-gray-700 hover:bg-gray-100'"
          >
            ← Previous
          </button>
          <div class="flex gap-2">
            <button 
              v-for="page in totalPages" 
              :key="page" 
              @click="currentPage = page" 
              class="px-4 py-2.5 rounded-xl font-bold transition"
              :class="page === currentPage 
                ? 'bg-blue-600 text-white shadow-md' 
                : 'border border-gray-300 text-gray-700 hover:bg-gray-100'"
            >
              {{ page }}
            </button>
          </div>
          <button 
            @click="currentPage++" 
            :disabled="currentPage === totalPages" 
            class="px-5 py-2.5 border border-gray-300 rounded-xl font-semibold transition"
            :class="currentPage === totalPages ? 'text-gray-300 cursor-not-allowed' : 'text-gray-700 hover:bg-gray-100'"
          >
            Next →
          </button>
        </div>
      </div>

      <!-- ========== TAB: RIWAYAT BONGKAR ========== -->
      <div v-else>
        <h2 class="text-3xl font-black text-gray-800 mb-8 uppercase tracking-tight">
          Riwayat Tabungan Dibongkar
        </h2>

        <!-- Empty State -->
        <div v-if="brokenPlans.length === 0" class="text-center py-20 bg-white rounded-3xl border-2 border-dashed border-gray-200 shadow-sm">
          <div class="text-7xl mb-4">📦</div>
          <p class="text-gray-400 font-semibold text-lg">Belum ada riwayat bongkar tabungan.</p>
        </div>

        <!-- Broken Savings List -->
        <div v-else class="grid gap-4">
          <div 
            v-for="plan in paginatedBrokenPlans" 
            :key="plan.id" 
            class="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 flex justify-between items-center hover:shadow-md transition"
          >
            <div class="flex items-center gap-4">
              <div class="w-14 h-14 bg-gray-100 rounded-2xl flex items-center justify-center text-gray-600 font-bold text-2xl">
                📦
              </div>
              <div>
                <h3 class="font-bold text-xl text-gray-800">{{ plan.name }}</h3>
                <p class="text-sm text-gray-500 mt-1">Dibongkar: {{ formatDate(plan.created_at) }}</p>
              </div>
            </div>
            <div class="flex items-center gap-3">
              <button 
                @click="openDetail(plan)" 
                class="bg-gray-50 text-gray-600 px-5 py-2.5 rounded-xl font-bold hover:bg-gray-100 transition"
              >
                Buka
              </button>
            </div>
          </div>
        </div>

        <!-- Pagination for Broken Plans -->
        <div v-if="totalBrokenPages > 1" class="mt-8 flex justify-center items-center gap-2">
          <button 
            @click="currentBrokenPage--" 
            :disabled="currentBrokenPage === 1" 
            class="px-5 py-2.5 border border-gray-300 rounded-xl font-semibold transition"
            :class="currentBrokenPage === 1 ? 'text-gray-300 cursor-not-allowed' : 'text-gray-700 hover:bg-gray-100'"
          >
            ← Previous
          </button>
          <div class="flex gap-2">
            <button 
              v-for="page in totalBrokenPages" 
              :key="page" 
              @click="currentBrokenPage = page" 
              class="px-4 py-2.5 rounded-xl font-bold transition"
              :class="page === currentBrokenPage 
                ? 'bg-green-600 text-white shadow-md' 
                : 'border border-gray-300 text-gray-700 hover:bg-gray-100'"
            >
              {{ page }}
            </button>
          </div>
          <button 
            @click="currentBrokenPage++" 
            :disabled="currentBrokenPage === totalBrokenPages" 
            class="px-5 py-2.5 border border-gray-300 rounded-xl font-semibold transition"
            :class="currentBrokenPage === totalBrokenPages ? 'text-gray-300 cursor-not-allowed' : 'text-gray-700 hover:bg-gray-100'"
          >
            Next →
          </button>
        </div>
      </div>
    </main>

    <!-- ==================== MODAL: CREATE SAVING ==================== -->
    <div 
      v-if="showCreateModal" 
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4" 
      @click.self="showCreateModal = false"
    >
      <div class="bg-white rounded-3xl shadow-2xl w-full max-w-lg p-8 scale-up-animation">
        <h3 class="text-3xl font-bold mb-6 text-gray-800 flex items-center gap-3">
          <span class="text-4xl">💰</span> Buat Tabungan Baru
        </h3>
        
        <div class="space-y-5">
          <div>
            <label class="block text-sm font-bold text-gray-700 mb-2">Nama Tabungan</label>
            <input 
              v-model="newPlan.name" 
              type="text" 
              class="w-full border-2 border-gray-200 p-3 rounded-xl focus:border-blue-500 focus:ring-2 focus:ring-blue-200 outline-none transition" 
              placeholder="Contoh: Beli Motor"
            />
          </div>
          
          <div class="grid grid-cols-3 gap-3">
            <div class="col-span-1">
              <label class="block text-sm font-bold text-gray-700 mb-2">Mata Uang</label>
              <select 
                v-model="newPlan.currency" 
                class="w-full border-2 border-gray-200 p-3 rounded-xl focus:border-blue-500 outline-none transition"
              >
                <option>IDR (Rp)</option>
                <option>USD ($)</option>
              </select>
            </div>
            <div class="col-span-2">
              <label class="block text-sm font-bold text-gray-700 mb-2">Target Nominal</label>
              <input 
                v-model.number="newPlan.target_amount" 
                type="number" 
                class="w-full border-2 border-gray-200 p-3 rounded-xl focus:border-blue-500 focus:ring-2 focus:ring-blue-200 outline-none transition" 
                placeholder="0"
              />
            </div>
          </div>
        </div>
        
        <div class="flex justify-end gap-3 mt-8">
          <button 
            @click="showCreateModal = false" 
            class="px-6 py-3 text-gray-600 font-bold hover:bg-gray-100 rounded-xl transition"
          >
            Batal
          </button>
          <button 
            @click="handleCreate" 
            class="px-8 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-xl font-bold hover:shadow-lg transition"
          >
            Buat Sekarang
          </button>
        </div>
      </div>
    </div>

    <!-- ==================== MODAL: DETAIL SAVING ==================== -->
    <div 
      v-if="showDetailModal" 
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4 overflow-y-auto" 
      @click.self="closeDetailModal"
    >
      <div class="bg-white rounded-3xl shadow-2xl w-full max-w-3xl max-h-[95vh] overflow-y-auto scale-up-animation my-8">
        <!-- Header -->
        <div class="sticky top-0 bg-gradient-to-r from-blue-600 to-purple-600 text-white p-6 rounded-t-3xl">
          <div class="flex justify-between items-start">
            <div>
              <h3 class="text-3xl font-bold">{{ selectedPlan?.name }}</h3>
              <p class="text-blue-100 text-sm mt-1">{{ selectedPlan?.currency }}</p>
            </div>
            <button 
              @click="closeDetailModal" 
              class="text-white hover:bg-white/20 p-2 rounded-full transition"
            >
              <svg class="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
              </svg>
            </button>
          </div>
        </div>

        <div class="p-6 space-y-6">
          <!-- Total Accumulated Balance -->
          <div class="bg-gradient-to-br from-green-50 to-blue-50 p-6 rounded-2xl border-2 border-green-200 shadow-sm">
            <p class="text-sm text-gray-600 font-semibold mb-2">Total Terkumpul</p>
            <h2 class="text-5xl font-black text-green-600 mb-4">
              {{ selectedPlan?.currency === 'IDR (Rp)' ? 'Rp' : '$' }} {{ formatNumber(planDetail.total_saved) }}
            </h2>
            
            <div class="space-y-2 mb-4">
              <div class="flex justify-between text-sm">
                <span class="text-gray-600 font-medium">Target:</span>
                <span class="font-bold text-gray-800">
                  {{ selectedPlan?.currency === 'IDR (Rp)' ? 'Rp' : '$' }} {{ formatNumber(selectedPlan?.target_amount || 0) }}
                </span>
              </div>
              <div class="flex justify-between text-sm">
                <span class="text-gray-600 font-medium">Sisa:</span>
                <span class="font-bold text-orange-600">
                  {{ selectedPlan?.currency === 'IDR (Rp)' ? 'Rp' : '$' }} {{ formatNumber(planDetail.remaining) }}
                </span>
              </div>
            </div>

            <!-- Progress Bar -->
            <div class="w-full bg-gray-200 rounded-full h-4 overflow-hidden">
              <div 
                class="bg-gradient-to-r from-green-500 to-blue-500 h-4 rounded-full transition-all duration-500 flex items-center justify-end pr-2"
                :style="{width: Math.min(planDetail.progress_percentage, 100) + '%'}"
              >
                <span v-if="planDetail.progress_percentage >= 20" class="text-white text-xs font-bold">
                  {{ Math.round(planDetail.progress_percentage) }}%
                </span>
              </div>
            </div>
            <p class="text-xs text-center text-gray-500 mt-2 font-semibold">
              {{ Math.round(planDetail.progress_percentage) }}% Tercapai
            </p>
          </div>

          <!-- Action Buttons -->
          <div class="grid grid-cols-2 gap-4">
            <button 
              @click="showCameraModal = true" 
              class="bg-gradient-to-r from-blue-600 to-purple-600 text-white py-4 rounded-xl font-bold hover:shadow-lg hover:scale-105 transition-all flex items-center justify-center gap-2"
            >
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z"/>
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 13a3 3 0 11-6 0 3 3 0 016 0z"/>
              </svg>
              Menabung
            </button>
            <button 
              v-if="selectedPlan?.status === 'active'"
              @click="handleBongkar" 
              class="bg-gradient-to-r from-orange-500 to-red-500 text-white py-4 rounded-xl font-bold hover:shadow-lg hover:scale-105 transition-all flex items-center justify-center gap-2"
            >
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
              Bongkar
            </button>
          </div>

          <!-- Transaction History -->
          <div>
            <h4 class="font-bold text-xl text-gray-800 mb-4 flex items-center gap-2">
              <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
              Riwayat Menabung
            </h4>
            
            <!-- Empty State -->
            <div v-if="planDetail.logs.length === 0" class="text-center py-12 bg-gray-50 rounded-2xl">
              <div class="text-5xl mb-3">📝</div>
              <p class="text-gray-400 font-medium">Belum ada riwayat menabung</p>
            </div>
            
            <!-- Transaction List -->
            <div v-else class="space-y-2 max-h-80 overflow-y-auto pr-2">
              <div 
                v-for="log in paginatedLogs" 
                :key="log.id" 
                class="flex justify-between items-center bg-gradient-to-r from-green-50 to-blue-50 p-4 rounded-xl hover:shadow-md transition border border-green-100"
              >
                <div>
                  <p class="font-bold text-lg text-green-600">
                    + {{ selectedPlan?.currency === 'IDR (Rp)' ? 'Rp' : '$' }} {{ formatNumber(log.amount) }}
                  </p>
                  <p class="text-xs text-gray-500 mt-1">{{ formatDate(log.created_at) }}</p>
                </div>
                <div class="text-3xl">💰</div>
              </div>
            </div>

            <!-- Pagination for Transaction History -->
            <div v-if="totalLogPages > 1" class="flex justify-center gap-2 mt-5">
              <button 
                v-for="page in totalLogPages" 
                :key="page"
                @click="currentLogPage = page"
                :class="currentLogPage === page 
                  ? 'bg-blue-600 text-white shadow-md' 
                  : 'bg-gray-200 text-gray-700 hover:bg-gray-300'"
                class="px-4 py-2 rounded-lg font-bold transition"
              >
                {{ page }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- ==================== MODAL: CAMERA / ADD MONEY ==================== -->
    <div 
      v-if="showCameraModal" 
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4" 
      @click.self="closeCameraModal"
    >
      <div class="bg-white rounded-3xl shadow-2xl w-full max-w-2xl scale-up-animation">
        <div class="bg-gradient-to-r from-blue-600 to-purple-600 text-white p-6 rounded-t-3xl flex justify-between items-center">
          <div>
            <h3 class="text-2xl font-bold flex items-center gap-2">
              <span class="text-3xl">📸</span> AI Scanner - Deteksi Uang
            </h3>
            <p class="text-blue-100 text-sm mt-1">Arahkan kamera ke uang kertas Rupiah</p>
          </div>
          <button 
            @click="closeCameraModal" 
            class="text-white hover:bg-white/20 p-2 rounded-full transition"
          >
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
        </div>
        
        <div class="p-6 space-y-5">
          <!-- Camera Feed -->
          <div class="relative bg-gray-900 rounded-2xl aspect-video overflow-hidden">
            <!-- Video Stream -->
            <video 
              ref="videoElement" 
              autoplay 
              playsinline
              class="w-full h-full object-cover"
              :class="{ 'hidden': !cameraActive }"
            ></video>
            
            <!-- Canvas for Capture (Hidden) -->
            <canvas ref="canvasElement" class="hidden"></canvas>
            
            <!-- Loading State -->
            <div v-if="cameraLoading" class="absolute inset-0 flex items-center justify-center bg-gray-900">
              <div class="text-white text-center">
                <div class="animate-spin rounded-full h-16 w-16 border-t-4 border-blue-500 mx-auto mb-4"></div>
                <p class="text-sm font-medium">Mengaktifkan kamera...</p>
              </div>
            </div>
            
            <!-- Detection Status -->
            <div v-if="detecting" class="absolute inset-0 flex items-center justify-center bg-black bg-opacity-50">
              <div class="text-white text-center">
                <div class="animate-pulse mb-4">
                  <svg class="w-20 h-20 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                  </svg>
                </div>
                <p class="text-lg font-bold">Mendeteksi uang...</p>
                <p class="text-sm text-gray-300 mt-2">Mohon tunggu sebentar</p>
              </div>
            </div>
            
            <!-- Detection Result Overlay -->
            <div v-if="detectionResult && detectionResult.banknotes.length > 0" class="absolute top-4 left-4 right-4">
              <div class="bg-green-500 bg-opacity-90 text-white p-4 rounded-xl shadow-lg">
                <p class="font-bold text-lg">✅ Terdeteksi {{ detectionResult.banknotes.length }} lembar uang!</p>
                <div class="mt-2 space-y-1">
                  <p v-for="(note, index) in detectionResult.banknotes" :key="index" class="text-sm">
                    • Rp {{ formatNumber(note.value) }}
                  </p>
                </div>
                <p class="font-bold text-xl mt-3 pt-3 border-t border-white/30">
                  Total: Rp {{ formatNumber(detectionResult.total) }}
                </p>
              </div>
            </div>

            <!-- Error Display -->
            <div v-if="cameraError" class="absolute inset-0 flex items-center justify-center bg-gray-900">
              <div class="text-white text-center p-6">
                <svg class="w-16 h-16 mx-auto mb-4 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
                <p class="text-sm font-medium mb-2">❌ {{ cameraError }}</p>
                <button @click="startCamera" class="mt-4 bg-blue-600 px-6 py-2 rounded-lg hover:bg-blue-700">
                  Coba Lagi
                </button>
              </div>
            </div>
          </div>

          <!-- Action Buttons -->
          <div class="grid grid-cols-2 gap-3">
            <button 
              @click="captureAndDetect" 
              :disabled="!cameraActive || detecting"
              class="bg-gradient-to-r from-green-500 to-blue-500 text-white py-4 rounded-xl font-bold hover:shadow-lg transition disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
            >
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z"/>
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 13a3 3 0 11-6 0 3 3 0 016 0z"/>
              </svg>
              {{ detecting ? 'Mendeteksi...' : 'Scan Uang' }}
            </button>
            <button 
              @click="confirmDetection" 
              :disabled="!detectionResult || detecting"
              class="bg-gradient-to-r from-purple-500 to-pink-500 text-white py-4 rounded-xl font-bold hover:shadow-lg transition disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
            >
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
              </svg>
              Simpan
            </button>
          </div>

          <!-- Manual Input Alternative -->
          <div class="border-2 border-dashed border-gray-300 rounded-xl p-4 bg-gray-50">
            <label class="block text-sm font-bold text-gray-700 mb-3">Atau masukkan nominal manual:</label>
            <div class="flex gap-3">
              <input 
                v-model.number="manualAmount" 
                type="number" 
                class="flex-1 border-2 border-gray-300 p-3 rounded-xl outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition text-lg font-semibold" 
                placeholder="Contoh: 50000"
              />
              <button 
                @click="handleSaveMoney" 
                :disabled="!manualAmount || manualAmount <= 0"
                class="bg-blue-600 text-white px-6 py-3 rounded-xl font-bold hover:bg-blue-700 transition disabled:opacity-50"
              >
                Simpan
              </button>
            </div>
          </div>

          <!-- Close Button -->
          <button 
            @click="closeCameraModal" 
            class="w-full py-3 text-gray-600 font-bold hover:bg-gray-100 rounded-xl transition"
          >
            Tutup
          </button>
        </div>
      </div>
    </div>

    <!-- ==================== MODAL: EDIT SAVING ==================== -->
    <div 
      v-if="showEditModal" 
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4" 
      @click.self="showEditModal = false"
    >
      <div class="bg-white rounded-3xl shadow-2xl w-full max-w-lg p-8 scale-up-animation">
        <h3 class="text-3xl font-bold mb-6 text-gray-800 flex items-center gap-3">
          <span class="text-4xl">✏️</span> Edit Tabungan
        </h3>
        
        <div class="space-y-5">
          <div>
            <label class="block text-sm font-bold text-gray-700 mb-2">Nama Tabungan</label>
            <input 
              v-model="editForm.name" 
              type="text" 
              class="w-full border-2 border-gray-200 p-3 rounded-xl focus:border-blue-500 focus:ring-2 focus:ring-blue-200 outline-none transition"
            />
          </div>
          
          <div class="grid grid-cols-3 gap-3">
            <div class="col-span-1">
              <label class="block text-sm font-bold text-gray-700 mb-2">Mata Uang</label>
              <select 
                v-model="editForm.currency" 
                class="w-full border-2 border-gray-200 p-3 rounded-xl focus:border-blue-500 outline-none transition"
              >
                <option>IDR (Rp)</option>
                <option>USD ($)</option>
              </select>
            </div>
            <div class="col-span-2">
              <label class="block text-sm font-bold text-gray-700 mb-2">Target Nominal</label>
              <input 
                v-model.number="editForm.target_amount" 
                type="number" 
                class="w-full border-2 border-gray-200 p-3 rounded-xl focus:border-blue-500 focus:ring-2 focus:ring-blue-200 outline-none transition"
              />
            </div>
          </div>
        </div>
        
        <div class="flex justify-end gap-3 mt-8">
          <button 
            @click="showEditModal = false" 
            class="px-6 py-3 text-gray-600 font-bold hover:bg-gray-100 rounded-xl transition"
          >
            Batal
          </button>
          <button 
            @click="handleEditSave" 
            class="px-8 py-3 bg-blue-600 text-white rounded-xl font-bold hover:shadow-lg hover:bg-blue-700 transition"
          >
            Simpan
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch, onUnmounted } from 'vue'
import axios from 'axios'

// ==================== STATE MANAGEMENT ====================
const currentTab = ref('tabungan')
const showCreateModal = ref(false)
const showDetailModal = ref(false)
const showCameraModal = ref(false)
const showEditModal = ref(false)
const showMenu = ref(null)

// Pagination
const currentPage = ref(1)
const currentBrokenPage = ref(1)
const currentLogPage = ref(1)
const itemsPerPage = 10
const logsPerPage = 10

// Data
const activePlans = ref([])
const brokenPlans = ref([])
const selectedPlan = ref(null)
const planDetail = ref({
  logs: [],
  total_saved: 0,
  remaining: 0,
  progress_percentage: 0
})

// Forms
const newPlan = ref({
  user_id: 1,
  name: '',
  target_amount: 0,
  currency: 'IDR (Rp)'
})

const editForm = ref({
  name: '',
  target_amount: 0,
  currency: 'IDR (Rp)'
})

const manualAmount = ref(0)

// Camera AI Detection State
const videoElement = ref(null)
const canvasElement = ref(null)
const cameraStream = ref(null)
const cameraActive = ref(false)
const cameraLoading = ref(false)
const cameraError = ref('')
const detecting = ref(false)
const detectionResult = ref(null)

// ==================== COMPUTED PROPERTIES ====================

// Active Plans Pagination
const paginatedActivePlans = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  return activePlans.value.slice(start, end)
})

const totalPages = computed(() => {
  return Math.ceil(activePlans.value.length / itemsPerPage)
})

// Broken Plans Pagination
const paginatedBrokenPlans = computed(() => {
  const start = (currentBrokenPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  return brokenPlans.value.slice(start, end)
})

const totalBrokenPages = computed(() => {
  return Math.ceil(brokenPlans.value.length / itemsPerPage)
})

// Transaction Logs Pagination
const paginatedLogs = computed(() => {
  const start = (currentLogPage.value - 1) * logsPerPage
  const end = start + logsPerPage
  return planDetail.value.logs.slice(start, end)
})

const totalLogPages = computed(() => {
  return Math.ceil(planDetail.value.logs.length / logsPerPage)
})

// ==================== UTILITY FUNCTIONS ====================

// Format number with thousand separator
const formatNumber = (num) => {
  return new Intl.NumberFormat('id-ID').format(num || 0)
}

// Format date to Indonesian locale
const formatDate = (dateString) => {
  if (!dateString) return '-'
  const date = new Date(dateString)
  return date.toLocaleDateString('id-ID', { 
    year: 'numeric', 
    month: 'long', 
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// Toggle dropdown menu
const toggleMenu = (id) => {
  showMenu.value = showMenu.value === id ? null : id
}

// ==================== API FUNCTIONS ====================

// Fetch all savings plans
const fetchPlans = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/plans/1')
    activePlans.value = response.data.active_plans || []
    brokenPlans.value = response.data.history_plans || []
  } catch (error) {
    console.error('Error fetching plans:', error)
    alert('Gagal mengambil data tabungan')
  }
}

// Create new saving plan
const handleCreate = async () => {
  if (!newPlan.value.name || newPlan.value.target_amount <= 0) {
    alert('⚠️ Harap isi semua data dengan benar!')
    return
  }

  try {
    await axios.post('http://127.0.0.1:8000/plans/create', {
      user_id: newPlan.value.user_id,
      name: newPlan.value.name,
      target_amount: newPlan.value.target_amount,
      currency: newPlan.value.currency,
      duration_days: 30
    })
    
    // Reset form
    newPlan.value = {
      user_id: 1,
      name: '',
      target_amount: 0,
      currency: 'IDR (Rp)'
    }
    
    showCreateModal.value = false
    alert('✅ Tabungan Berhasil Dibuat!')
    await fetchPlans()
  } catch (error) {
    console.error('Error creating plan:', error)
    alert('❌ Gagal membuat tabungan')
  }
}

// Open detail modal and fetch transaction history
const openDetail = async (plan) => {
  selectedPlan.value = plan
  showDetailModal.value = true
  currentLogPage.value = 1
  
  try {
    const response = await axios.get(`http://127.0.0.1:8000/plans/${plan.id}/logs`)
    planDetail.value = {
      logs: response.data.logs || [],
      total_saved: response.data.total_saved || 0,
      remaining: response.data.remaining || 0,
      progress_percentage: response.data.progress_percentage || 0
    }
  } catch (error) {
    console.error('Error fetching plan details:', error)
    alert('❌ Gagal mengambil detail tabungan')
  }
}

// Close detail modal
const closeDetailModal = () => {
  showDetailModal.value = false
  selectedPlan.value = null
  manualAmount.value = 0
}

// Save money to plan
const handleSaveMoney = async () => {
  if (!manualAmount.value || manualAmount.value <= 0) {
    alert('⚠️ Masukkan nominal yang valid!')
    return
  }

  try {
    const response = await axios.post(
      `http://127.0.0.1:8000/plans/${selectedPlan.value.id}/save`, 
      { amount: manualAmount.value }
    )
    
    showCameraModal.value = false
    
    // Show success notification
    const currency = selectedPlan.value.currency === 'IDR (Rp)' ? 'Rp' : '$'
    alert(
      `✅ Berhasil menabung ${currency} ${formatNumber(manualAmount.value)}!\n\n` +
      `Total: ${currency} ${formatNumber(response.data.total_saved)}\n` +
      `Sisa: ${currency} ${formatNumber(response.data.remaining)}`
    )
    
    manualAmount.value = 0
    
    // Refresh data
    await openDetail(selectedPlan.value)
    await fetchPlans()
  } catch (error) {
    console.error('Error saving money:', error)
    alert('❌ Gagal menyimpan uang')
  }
}

// ==================== CAMERA AI DETECTION FUNCTIONS ====================

// Start camera stream
const startCamera = async () => {
  cameraLoading.value = true
  cameraError.value = ''
  
  try {
    // Request camera access
    const stream = await navigator.mediaDevices.getUserMedia({ 
      video: { 
        facingMode: 'environment', // Use back camera on mobile
        width: { ideal: 1280 },
        height: { ideal: 720 }
      } 
    })
    
    cameraStream.value = stream
    
    // Wait for videoElement to be available
    await new Promise(resolve => setTimeout(resolve, 100))
    
    if (videoElement.value) {
      videoElement.value.srcObject = stream
      cameraActive.value = true
    }
  } catch (error) {
    console.error('Camera error:', error)
    if (error.name === 'NotAllowedError') {
      cameraError.value = 'Akses kamera ditolak. Silakan izinkan akses kamera.'
    } else if (error.name === 'NotFoundError') {
      cameraError.value = 'Kamera tidak ditemukan pada perangkat ini.'
    } else {
      cameraError.value = 'Gagal mengaktifkan kamera: ' + error.message
    }
  } finally {
    cameraLoading.value = false
  }
}

// Stop camera stream
const stopCamera = () => {
  if (cameraStream.value) {
    cameraStream.value.getTracks().forEach(track => track.stop())
    cameraStream.value = null
  }
  
  if (videoElement.value) {
    videoElement.value.srcObject = null
  }
  
  cameraActive.value = false
  detecting.value = false
  detectionResult.value = null
}

// Close camera modal and cleanup
const closeCameraModal = () => {
  stopCamera()
  showCameraModal.value = false
  manualAmount.value = 0
  cameraError.value = ''
}

// Capture frame and send to detection API
const captureAndDetect = async () => {
  if (!cameraActive.value || !videoElement.value || !canvasElement.value) {
    alert('⚠️ Kamera belum siap!')
    return
  }
  
  detecting.value = true
  detectionResult.value = null
  
  try {
    // Capture frame from video
    const video = videoElement.value
    const canvas = canvasElement.value
    
    canvas.width = video.videoWidth
    canvas.height = video.videoHeight
    
    const ctx = canvas.getContext('2d')
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height)
    
    // Convert to blob
    const blob = await new Promise((resolve) => {
      canvas.toBlob(resolve, 'image/jpeg', 0.9)
    })
    
    // Create FormData
    const formData = new FormData()
    formData.append('image', blob, 'capture.jpg')
    
    // Send to detection API
    const response = await axios.post('http://127.0.0.1:8000/detect', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    
    // Check if any banknotes detected
    if (response.data && response.data.banknotes && response.data.banknotes.length > 0) {
      detectionResult.value = response.data
      
      // Auto-scroll to show result
      setTimeout(() => {
        detecting.value = false
      }, 500)
    } else {
      detecting.value = false
      alert('❌ Tidak ada uang terdeteksi. Silakan coba lagi dengan:\n\n' +
            '• Pencahayaan yang lebih baik\n' +
            '• Letakkan uang di permukaan datar\n' +
            '• Pastikan uang terlihat jelas di kamera')
    }
  } catch (error) {
    detecting.value = false
    console.error('Detection error:', error)
    
    if (error.response && error.response.status === 404) {
      alert('❌ Endpoint deteksi belum tersedia.\n\nSilakan gunakan input manual atau hubungi administrator.')
    } else {
      alert('❌ Gagal mendeteksi uang: ' + (error.response?.data?.detail || error.message))
    }
  }
}

// Confirm detection and save to database
const confirmDetection = async () => {
  if (!detectionResult.value || !detectionResult.value.total) {
    alert('⚠️ Belum ada hasil deteksi!')
    return
  }
  
  try {
    const totalAmount = detectionResult.value.total
    const banknoteCount = detectionResult.value.banknotes.length // Simpan dulu sebelum di-reset
    
    const response = await axios.post(
      `http://127.0.0.1:8000/plans/${selectedPlan.value.id}/save`, 
      { amount: totalAmount }
    )
    
    // Stop camera and close modal
    stopCamera()
    showCameraModal.value = false
    
    // Show custom success notification
    const currency = selectedPlan.value.currency === 'IDR (Rp)' ? 'Rp' : '$'
    alert(
      `🎉 Hari ini anda berhasil menabung sebesar ${currency} ${formatNumber(totalAmount)}!\n\n` +
      `Terdeteksi ${banknoteCount} lembar uang kertas\n\n` +
      `Total Tabungan: ${currency} ${formatNumber(response.data.total_saved)}\n` +
      `Sisa Target: ${currency} ${formatNumber(response.data.remaining)}`
    )
    
    // Reset state
    detectionResult.value = null
    manualAmount.value = 0
    
    // Refresh data
    await openDetail(selectedPlan.value)
    await fetchPlans()
  } catch (error) {
    console.error('Error saving detected money:', error)
    alert('❌ Gagal menyimpan uang hasil deteksi')
  }
}

// ==================== END CAMERA FUNCTIONS ====================

// Break/archive saving plan
const handleBongkar = async () => {
  const currency = selectedPlan.value.currency === 'IDR (Rp)' ? 'Rp' : '$'
  
  if (!confirm(
    `Yakin ingin membongkar tabungan "${selectedPlan.value.name}"?\n\n` +
    `Total yang terkumpul: ${currency} ${formatNumber(planDetail.value.total_saved)}`
  )) {
    return
  }

  try {
    await axios.put(`http://127.0.0.1:8000/plans/bongkar/${selectedPlan.value.id}`)
    
    alert('🎉 Tabungan berhasil dibongkar!')
    
    closeDetailModal()
    await fetchPlans()
    currentTab.value = 'riwayat'
  } catch (error) {
    console.error('Error breaking plan:', error)
    alert('❌ Gagal membongkar tabungan')
  }
}

// Open edit modal
const editPlan = (plan) => {
  showMenu.value = null
  selectedPlan.value = plan
  editForm.value = {
    name: plan.name,
    target_amount: plan.target_amount,
    currency: plan.currency
  }
  showEditModal.value = true
}

// Save edited plan
const handleEditSave = async () => {
  if (!editForm.value.name || editForm.value.target_amount <= 0) {
    alert('⚠️ Harap isi semua data dengan benar!')
    return
  }

  try {
    await axios.put(
      `http://127.0.0.1:8000/plans/edit/${selectedPlan.value.id}`, 
      editForm.value
    )
    
    alert('✅ Tabungan berhasil diupdate!')
    showEditModal.value = false
    await fetchPlans()
  } catch (error) {
    console.error('Error updating plan:', error)
    alert('❌ Gagal mengupdate tabungan')
  }
}

// Delete saving plan
const deletePlan = async (plan) => {
  if (!confirm(
    `Yakin ingin menghapus tabungan "${plan.name}"?\n\n` +
    `⚠️ Semua riwayat tabungan juga akan terhapus!`
  )) {
    return
  }
  
  showMenu.value = null
  
  try {
    await axios.delete(`http://127.0.0.1:8000/plans/${plan.id}`)
    alert('✅ Tabungan berhasil dihapus!')
    await fetchPlans()
  } catch (error) {
    console.error('Error deleting plan:', error)
    alert('❌ Gagal menghapus tabungan')
  }
}

// ==================== LIFECYCLE ====================

// Watch for camera modal open/close
watch(showCameraModal, (newValue) => {
  if (newValue) {
    // Modal opened - start camera
    startCamera()
  } else {
    // Modal closed - stop camera
    stopCamera()
  }
})

// Cleanup camera on component unmount
onUnmounted(() => {
  stopCamera()
})

onMounted(() => {
  fetchPlans()
})
</script>

<style scoped>
.scale-up-animation {
  animation: scaleUp 0.3s cubic-bezier(0.390, 0.575, 0.565, 1.000) both;
}

@keyframes scaleUp {
  0% { 
    transform: scale(0.8);
    opacity: 0;
  }
  100% { 
    transform: scale(1);
    opacity: 1;
  }
}

/* Custom scrollbar */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 10px;
}

::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
  background: #555;
}
</style>
