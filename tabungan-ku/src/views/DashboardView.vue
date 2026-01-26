<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-50 via-purple-50 to-indigo-50 flex flex-col">
    <!-- ==================== NAVIGATION TABS ==================== -->
    <nav class="bg-white/80 backdrop-blur-xl shadow-lg border-b border-purple-100 p-5 flex justify-between items-center sticky top-0 z-10">
      <!-- Logo/Brand -->
      <div class="flex items-center gap-3">
        <h1 class="text-2xl font-black bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 bg-clip-text text-transparent">
          TabunganKu
        </h1>
      </div>

      <!-- Tab Buttons -->
      <div class="flex gap-4">
        <button 
          @click="currentTab = 'tabungan'"
          :disabled="currentTab === 'tabungan'"
          :class="currentTab === 'tabungan' 
            ? 'bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 text-white shadow-lg scale-105' 
            : 'bg-white text-gray-600 hover:bg-gray-50 border-2 border-gray-200'"
          class="px-10 py-3.5 rounded-2xl font-bold transition-all duration-300 transform hover:scale-105"
        >
          💰 Tabungan
        </button>
        <button 
          @click="currentTab = 'riwayat'"
          :disabled="currentTab === 'riwayat'"
          :class="currentTab === 'riwayat' 
            ? 'bg-gradient-to-r from-emerald-600 via-teal-600 to-cyan-600 text-white shadow-lg scale-105' 
            : 'bg-white text-gray-600 hover:bg-gray-50 border-2 border-gray-200'"
          class="px-10 py-3.5 rounded-2xl font-bold transition-all duration-300 transform hover:scale-105"
        >
          📦 Riwayat Bongkar
        </button>
      </div>

      <!-- Logout Button -->
      <button 
        @click="handleLogout" 
        class="bg-gradient-to-r from-red-500 to-pink-500 text-white px-6 py-3 rounded-2xl font-bold hover:shadow-2xl hover:scale-105 transition-all duration-300 flex items-center gap-2"
      >
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/>
        </svg>
        Logout
      </button>
    </nav>

    <!-- ==================== MAIN CONTENT ==================== -->
    <main class="p-8 max-w-7xl mx-auto w-full">
      
      <!-- ========== TAB: TABUNGAN AKTIF ========== -->
      <div v-if="currentTab === 'tabungan'">
        <div class="flex justify-between items-center mb-10">
          <div>
            <h2 class="pb-2 text-4xl font-black bg-linear-to-r from-indigo-600 via-purple-600 to-pink-600 bg-clip-text text-transparent">
              Daftar Tabungan Aktif
            </h2>
            <p class="text-gray-500 mt-2 font-medium">Kelola dan pantau progres tabunganmu</p>
          </div>
          <button 
            @click="showCreateModal = true" 
            class="bg-linear-to-r from-indigo-600 via-purple-600 to-pink-600 text-white px-8 py-4 rounded-2xl font-bold hover:shadow-2xl hover:scale-105 transition-all duration-300 flex items-center gap-3"
          >
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
            </svg>
            Buat Tabungan
          </button>
        </div>
        <br>

        <!-- Empty State -->
        <div v-if="activePlans.length === 0" class="text-center py-24 bg-white/80 backdrop-blur-xl rounded-3xl border-2 border-dashed border-purple-200 shadow-xl">
          <div class="text-8xl mb-6 animate-bounce">💰</div>
          <p class="text-gray-600 font-bold text-xl">Belum ada tabungan aktif.</p>
          <p class="text-gray-400 text-sm mt-3">Klik tombol "Buat Tabungan" untuk memulai!</p>
        </div>

        <!-- Savings List -->
        <div v-else class="grid gap-8">
          <div 
            v-for="plan in paginatedActivePlans" 
            :key="plan.id" 
            class="bg-white/80 backdrop-blur-xl p-8 rounded-3xl shadow-lg border-2 border-purple-100 hover:shadow-2xl hover:border-purple-300 hover:scale-[1.01] transition-all duration-300 group relative"
          >
            <div class="flex justify-between items-start gap-6">
              <div class="flex items-start gap-5 flex-1">
                <div class="w-16 h-16 bg-linear-to-br from-indigo-500 via-purple-500 to-pink-500 rounded-2xl flex items-center justify-center text-white font-bold text-3xl shadow-lg group-hover:scale-110 transition-transform">
                  💰
                </div>
                <div class="flex-1">
                  <h3 class="font-black text-2xl text-gray-800 mb-2">{{ plan.name }}</h3>
                  <div v-if="plan.target_date" class="inline-flex items-center gap-2 bg-gradient-to-r from-orange-50 to-pink-50 px-3 py-1.5 rounded-full mb-3 border border-orange-200">
                    <svg class="w-4 h-4 text-orange-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
                    </svg>
                    <span class="text-xs font-bold text-orange-700">{{ calculateRemainingDays(plan.target_date) }}</span>
                  </div>
                  <!-- <div class="grid grid-cols-2 gap-3 mb-5">
                    <div class="bg-gradient-to-br from-indigo-50 to-purple-50 p-3 rounded-xl border border-indigo-100">
                      <p class="text-xs text-gray-500 font-semibold mb-1">Target</p>
                      <p class="font-black text-lg text-indigo-600">{{ plan.currency }} {{ formatNumber(plan.target_amount) }}</p>
                    </div>
                    <div class="bg-gradient-to-br from-emerald-50 to-teal-50 p-3 rounded-xl border border-emerald-100">
                      <p class="text-xs text-gray-500 font-semibold mb-1">Terkumpul</p>
                      <p class="font-black text-lg text-emerald-600">{{ plan.currency }} {{ formatNumber(plan.total_saved || 0) }}</p>
                    </div>
                  </div> -->
                  
                  <!-- Progress Bar with Percentage -->
                  <div class="space-y-2">
                    <div class="flex justify-between items-center">
                      <span class="text-xs font-bold text-gray-600">Progress Tercapai</span>
                      <span class="text-base font-black bg-linear-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">
                        {{ Math.round((plan.total_saved || 0) / plan.target_amount * 100) }}%
                      </span>
                    </div>
                    <div class="w-full bg-gray-200 rounded-full h-4 overflow-hidden shadow-inner">
                      <div 
                        class="bg-linear-to-r from-indigo-500 via-purple-500 to-pink-500 h-4 rounded-full transition-all duration-500 shadow-lg"
                        :style="{width: Math.min((plan.total_saved || 0) / plan.target_amount * 100, 100) + '%'}"
                      >
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <div class="flex flex-col gap-3 flex-shrink-0">
                <button 
                  @click="openDetail(plan)" 
                  class="bg-gradient-to-r from-emerald-50 to-teal-50 text-emerald-600 px-6 py-3 rounded-2xl font-bold hover:shadow-lg hover:scale-105 transition-all duration-300 border-2 border-emerald-200"
                >
                  Buka
                </button>
                <div class="flex gap-2">
                  <button 
                    @click="editPlan(plan)" 
                    class="flex-1 bg-gradient-to-r from-blue-50 to-indigo-50 text-blue-600 p-3 rounded-2xl font-bold hover:shadow-lg hover:scale-105 transition-all duration-300 border-2 border-blue-200 flex items-center justify-center gap-2"
                    title="Edit Tabungan"
                  >
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
                    </svg>
                    Edit
                  </button>
                  <button 
                    @click="confirmDelete(plan)" 
                    class="flex-1 bg-gradient-to-r from-red-50 to-pink-50 text-red-600 p-3 rounded-2xl font-bold hover:shadow-lg hover:scale-105 transition-all duration-300 border-2 border-red-200 flex items-center justify-center gap-2"
                    title="Hapus Tabungan"
                  >
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                    </svg>
                    Hapus
                  </button>
                </div>
              </div>
          </div>
        </div>

        <!-- Pagination -->
        <div v-if="totalPages > 1" class="mt-10 flex justify-center items-center gap-3">
          <button 
            @click="currentPage--" 
            :disabled="currentPage === 1" 
            class="px-6 py-3 border-2 rounded-2xl font-bold transition-all duration-300"
            :class="currentPage === 1 ? 'border-gray-200 text-gray-300 cursor-not-allowed' : 'border-purple-200 text-gray-700 hover:bg-purple-50'"
          >
            ← Previous
          </button>
          <div class="flex gap-2">
            <button 
              v-for="page in totalPages" 
              :key="page" 
              @click="currentPage = page" 
              class="px-5 py-3 rounded-2xl font-bold transition-all duration-300"
              :class="page === currentPage 
                ? 'bg-linear-to-r from-indigo-600 via-purple-600 to-pink-600 text-white shadow-lg' 
                : 'border-2 border-gray-200 text-gray-700 hover:bg-gray-50'"
            >
              {{ page }}
            </button>
          </div>
          <button 
            @click="currentPage++" 
            :disabled="currentPage === totalPages" 
            class="px-6 py-3 border-2 rounded-2xl font-bold transition-all duration-300"
            :class="currentPage === totalPages ? 'border-gray-200 text-gray-300 cursor-not-allowed' : 'border-purple-200 text-gray-700 hover:bg-purple-50'"
          >
            Next →
          </button>
        </div>
      </div>
    </div>

      <!-- ========== TAB: RIWAYAT BONGKAR ========== -->
      <div v-else-if="currentTab === 'riwayat'">
        <div class="mb-10">
          <h2 class="text-4xl font-black bg-gradient-to-r from-emerald-600 via-teal-600 to-cyan-600 bg-clip-text text-transparent pb-2">
            Riwayat Tabungan Dibongkar
          </h2>
          <p class="text-gray-500 mt-2 font-medium">Tabungan yang sudah selesai dibongkar</p>
        </div>
        <br>
        <!-- Empty State -->
        <div v-if="brokenPlans.length === 0" class="text-center py-24 bg-white/80 backdrop-blur-xl rounded-3xl border-2 border-dashed border-emerald-200 shadow-xl">
          <div class="text-8xl mb-6 animate-bounce">📦</div>
          <p class="text-gray-600 font-bold text-xl">Belum ada riwayat bongkar tabungan.</p>
          <p class="text-gray-400 text-sm mt-3">Tabungan yang sudah dibongkar akan muncul di sini</p>
        </div>

        <!-- Broken Savings List -->
        <div v-else class="grid gap-8">
          <div 
            v-for="plan in paginatedBrokenPlans" 
            :key="plan.id" 
            class="bg-white/80 backdrop-blur-xl p-8 rounded-3xl shadow-lg border-2 border-emerald-100 hover:shadow-2xl hover:border-emerald-300 hover:scale-[1.01] transition-all duration-300 group relative"
          >
            <div class="flex justify-between items-start gap-6">
              <div class="flex items-start gap-5 flex-1">
                <div class="w-16 h-16 bg-gradient-to-br from-emerald-500 via-teal-500 to-cyan-500 rounded-2xl flex items-center justify-center text-white font-bold text-3xl shadow-lg group-hover:scale-110 transition-transform">
                  📦
                </div>
                <div class="flex-1">
                  <h3 class="pb-3 font-black text-2xl text-gray-800 mb-2">{{ plan.name }}</h3>
                  <div class="inline-flex items-center gap-2 bg-gradient-to-r from-emerald-50 to-teal-50 px-4 py-2 rounded-full border border-emerald-200">
                    <svg class="w-4 h-4 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                    </svg>
                    <div class="flex flex-col">
                      <span class="text-xs font-bold text-emerald-700">Selesai Dibongkar</span>
                      <span class="text-[10px] text-emerald-600 mt-0.5">{{ formatDate(plan.broken_at || plan.created_at) }}</span>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Action Buttons -->
              <div class="flex gap-3 pt-4">
                <button 
                  @click="openDetail(plan)"
                  class="px-6 py-3 bg-gradient-to-r from-emerald-50 to-teal-50 text-emerald-600 rounded-2xl font-bold hover:shadow-lg hover:scale-105 transition-all duration-300 border-2 border-emerald-200"
                >
                  Buka
                </button>
                <button 
                  @click="confirmDelete(plan)"
                  class="px-6 py-3 bg-gradient-to-r from-red-50 to-pink-50 text-red-600 rounded-2xl font-bold hover:shadow-lg hover:scale-105 transition-all duration-300 flex items-center gap-2 border-2 border-red-200"
                >
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                  </svg>
                  Hapus
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Pagination -->
        <div v-if="totalBrokenPages > 1" class="flex justify-center items-center gap-4 mt-12">
          <button 
            @click="currentBrokenPage--" 
            :disabled="currentBrokenPage === 1" 
            class="px-6 py-3 border-2 rounded-2xl font-bold transition-all duration-300"
            :class="currentBrokenPage === 1 ? 'border-gray-200 text-gray-300 cursor-not-allowed' : 'border-emerald-200 text-gray-700 hover:bg-emerald-50'"
          >
            ← Prev
          </button>
          <div class="flex gap-2">
            <button 
              v-for="page in totalBrokenPages" 
              :key="page" 
              @click="currentBrokenPage = page" 
              class="px-5 py-3 rounded-2xl font-bold transition-all duration-300"
              :class="page === currentBrokenPage 
                ? 'bg-gradient-to-r from-emerald-600 via-teal-600 to-cyan-600 text-white shadow-lg' 
                : 'border-2 border-gray-200 text-gray-700 hover:bg-gray-50'"
            >
              {{ page }}
            </button>
          </div>
          <button 
            @click="currentBrokenPage++" 
            :disabled="currentBrokenPage === totalBrokenPages" 
            class="px-6 py-3 border-2 rounded-2xl font-bold transition-all duration-300"
            :class="currentBrokenPage === totalBrokenPages ? 'border-gray-200 text-gray-300 cursor-not-allowed' : 'border-emerald-200 text-gray-700 hover:bg-emerald-50'"
          >
            Next →
          </button>
        </div>
      </div>

    </main>

    <!-- ==================== MODAL: CREATE SAVING ==================== -->
    <div 
      v-if="showCreateModal" 
      class="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-4" 
      @click.self="showCreateModal = false"
    >
      <div class="bg-white/95 backdrop-blur-xl rounded-3xl shadow-2xl w-full max-w-lg p-10 scale-up-animation border-2 border-purple-100">
        <div class="text-center mb-8">
          <div class="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 rounded-2xl mb-4 shadow-lg">
            <span class="text-4xl">💰</span>
          </div>
          <h3 class="text-3xl font-black bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 bg-clip-text text-transparent">
            Buat Tabungan Baru
          </h3>
        </div>
        <br>
        <div class="space-y-6 pt-3">
          <div>
            <label class="block text-sm font-bold text-gray-700 mb-3 ml-1">Nama Tabungan</label>
            <input 
              v-model="newPlan.name" 
              type="text" 
              class="w-full border-2 border-gray-200 bg-gray-50 p-4 rounded-2xl focus:border-purple-500 focus:ring-2 focus:ring-purple-200 focus:bg-white outline-none transition-all" 
              placeholder="Contoh: Beli Motor, Liburan ke Bali"
            />
          </div>
          <div class="grid grid-cols-3 gap-4 pt-3">
            <div class="col-span-1">
              <label class="block text-sm font-bold text-gray-700 mb-3 ml-1">Mata Uang</label>
              <select 
                v-model="newPlan.currency" 
                class="w-full border-2 border-gray-200 bg-gray-50 p-4 rounded-2xl focus:border-purple-500 focus:bg-white outline-none transition-all font-semibold"
              >
                <option>IDR (Rp)</option>
                <option>USD ($)</option>
              </select>
            </div>
            <div class="col-span-2">
              <label class="block text-sm font-bold text-gray-700 mb-3 ml-1">Target Nominal</label>
              <input 
                v-model.number="newPlan.target_amount" 
                type="number" 
                class="w-full border-2 border-gray-200 bg-gray-50 p-4 rounded-2xl focus:border-purple-500 focus:ring-2 focus:ring-purple-200 focus:bg-white outline-none transition-all font-semibold" 
                placeholder="0"
              />
            </div>
          </div>
        </div>
        
        <div class="flex justify-end gap-4 mt-10 pt-6 border-t border-gray-200">
          <button 
            @click="showCreateModal = false" 
            class="px-8 py-3.5 bg-white text-gray-700 font-bold hover:bg-gray-50 rounded-2xl transition-all duration-300 border-2 border-gray-200"
          >
            Batal
          </button>
          <button 
            @click="handleCreate" 
            class="px-10 py-3.5 bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 text-white rounded-2xl font-bold hover:shadow-2xl hover:scale-105 transition-all duration-300 flex items-center gap-2"
          >
            <span>Buat Sekarang</span>
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6"/>
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- ==================== MODAL: DETAIL SAVING ==================== -->
    <div 
      v-if="showDetailModal" 
      class="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-4 overflow-y-auto" 
      @click.self="closeDetailModal"
      style="scrollbar-width: none; -ms-overflow-style: none;"
    >
      <div class="bg-white/95 backdrop-blur-xl rounded-3xl shadow-2xl w-full max-w-3xl max-h-[95vh] overflow-y-auto scale-up-animation my-8 border-2 border-purple-100" style="scrollbar-width: none; -ms-overflow-style: none;">
        <!-- Header -->
        <div class="sticky top-0 bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 text-white p-8 rounded-t-3xl shadow-lg z-10">
          <div class="flex justify-between items-start">
            <div>
              <h3 class="text-4xl font-black mb-2">{{ selectedPlan?.name }}</h3>
              <p class="text-purple-100 text-sm font-semibold">{{ selectedPlan?.currency }}</p>
            </div>
            <button 
              @click="closeDetailModal" 
              class="text-white hover:bg-white/20 p-3 rounded-2xl transition-all duration-300"
            >
              <svg class="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
              </svg>
            </button>
          </div>
        </div>

        <div class="p-8 space-y-8">
          <!-- Total Accumulated Balance -->
          <div class="bg-gradient-to-br from-emerald-50 via-teal-50 to-cyan-50 p-8 rounded-3xl border-2 border-emerald-200 shadow-xl">
            <div class="flex items-center gap-2 mb-4">
              <svg class="w-6 h-6 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 9V7a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2m2 4h10a2 2 0 002-2v-6a2 2 0 00-2-2H9a2 2 0 00-2 2v6a2 2 0 002 2zm7-5a2 2 0 11-4 0 2 2 0 014 0z"/>
              </svg>
              <p class="text-sm text-gray-600 font-bold">Total Terkumpul</p>
            </div>
            <h2 class="text-6xl font-black bg-gradient-to-r from-emerald-600 to-teal-600 bg-clip-text text-transparent mb-6">
              {{ selectedPlan?.currency === 'IDR (Rp)' ? 'Rp' : '$' }} {{ formatNumber(planDetail.total_saved) }}
            </h2>
            <br>
            <div class="grid grid-cols-2 gap-4 mb-6">
              <div class="bg-white/70 backdrop-blur-sm p-4 rounded-2xl">
                <span class="text-xs text-gray-500 font-semibold block mb-1">Target</span>
                <span class="font-black text-lg text-gray-800 block">
                  {{ selectedPlan?.currency === 'IDR (Rp)' ? 'Rp' : '$' }} {{ formatNumber(selectedPlan?.target_amount || 0) }}
                </span>
              </div>
              <div class="bg-white/70 backdrop-blur-sm p-4 rounded-2xl">
                <span class="text-xs text-gray-500 font-semibold block mb-1">Sisa</span>
                <span class="font-black text-lg text-orange-600 block">
                  {{ selectedPlan?.currency === 'IDR (Rp)' ? 'Rp' : '$' }} {{ formatNumber(planDetail.remaining) }}
                </span>
              </div>
            </div>

            <!-- Progress Bar with Percentage -->
            <div class="space-y-3v pt-3">
              <div class="flex justify-between items-center">
                <span class="text-sm font-bold text-gray-600">Progress Tercapai</span>
                <span class="text-2xl font-black bg-gradient-to-r from-emerald-600 to-teal-600 bg-clip-text text-transparent">
                  {{ Math.round(planDetail.progress_percentage) }}%
                </span>
              </div>
              <div class="w-full bg-white/50 rounded-full h-5 overflow-hidden shadow-inner">
                <div 
                  class="bg-gradient-to-r from-emerald-500 via-teal-500 to-cyan-500 h-5 rounded-full transition-all duration-500 shadow-lg relative overflow-hidden"
                  :style="{width: Math.min(planDetail.progress_percentage, 100) + '%'}"
                >
                  <div class="absolute inset-0 bg-gradient-to-r from-white/20 to-transparent"></div>
                </div>
              </div>
            </div>
          </div>

          <!-- Action Buttons -->
          <div v-if="selectedPlan?.status === 'active'" class="grid grid-cols-2 gap-5 pt-3">
            <button 
              @click="showCameraModal = true" 
              class="bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 text-white py-5 rounded-2xl font-bold hover:shadow-2xl hover:scale-105 transition-all duration-300 flex items-center justify-center gap-3"
            >
              <svg class="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z"/>
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 13a3 3 0 11-6 0 3 3 0 016 0z"/>
              </svg>
              <span>Menabung</span>
            </button>
            <button 
              @click="handleBongkar" 
              class="bg-gradient-to-r from-orange-500 via-red-500 to-pink-500 text-white py-5 rounded-2xl font-bold hover:shadow-2xl hover:scale-105 transition-all duration-300 flex items-center justify-center gap-3"
            >
              <svg class="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
              <span>Bongkar</span>
            </button>
          </div>

          <!-- Transaction History -->
          <div class="pt-3">
            <h4 class="font-bold text-xl text-gray-800 mb-4 flex items-center gap-2">
              <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
              Riwayat Menabung
            </h4>
            
            <!-- Empty State -->
            <div v-if="planDetail.logs.length === 0" class="pt-3 text-center py-12 bg-gray-50 rounded-2xl">
              <div class="text-5xl mb-3">📝</div>
              <p class="text-gray-400 font-medium">Belum ada riwayat menabung</p>
            </div>
            
            <!-- Transaction List -->
            <div v-else class="pt-3 space-y-2 max-h-80 overflow-y-auto pr-2" style="scrollbar-width: none; -ms-overflow-style: none;">
              <div 
                v-for="log in paginatedLogs" 
                :key="log.id" 
                class="flex justify-between items-center bg-gradient-to-r from-green-50 to-blue-50 p-4 rounded-xl hover:shadow-md transition border border-green-100"
                style="margin-top:5px;"
              > 
                <div class="">
                  <p class="font-bold text-lg text-green-600">
                    + {{ selectedPlan?.currency === 'IDR (Rp)' ? 'Rp' : '$' }} {{ formatNumber(log.amount) }}
                  </p>
                  <p class="text-xs text-gray-500 mt-1">{{ formatDate(log.created_at) }}</p>
                </div>
                <div class="text-2xl">💰</div>
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
      class="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-[60] p-4 overflow-y-auto" 
      @click.self="closeCameraModal"
      style="scrollbar-width: none; -ms-overflow-style: none;"
    >
      <div class="bg-white/95 backdrop-blur-xl rounded-3xl shadow-2xl w-full max-w-3xl max-h-[95vh] overflow-y-auto scale-up-animation my-8 border-2 border-purple-100" style="scrollbar-width: none; -ms-overflow-style: none;">
        <!-- Header -->
        <div class="sticky top-0 bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 text-white p-8 rounded-t-3xl shadow-lg z-10">
          <div class="flex justify-between items-start">
            <div>
              <h3 class="text-4xl font-black mb-2 flex items-center gap-3">
                <span class="text-5xl">📸</span> AI Scanner
              </h3>
              <p class="text-purple-100 text-sm font-semibold">Arahkan uang kertas Rupiah ke kamera</p>
            </div>
            <button 
              @click="closeCameraModal" 
              class="text-white hover:bg-white/20 p-3 rounded-2xl transition-all duration-300"
            >
              <svg class="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
              </svg>
            </button>
          </div>
        </div>
        
        <div class="p-8 space-y-8">
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
          <div class="grid grid-cols-2 gap-5 pt-3">
            <button 
              @click="captureAndDetect" 
              :disabled="!cameraActive || detecting"
              class="bg-gradient-to-r from-emerald-600 via-teal-600 to-cyan-600 text-white py-5 rounded-2xl font-bold hover:shadow-2xl hover:scale-105 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-3"
            >
              <svg class="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z"/>
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 13a3 3 0 11-6 0 3 3 0 016 0z"/>
              </svg>
              <span>{{ detecting ? 'Mendeteksi...' : 'Scan Uang' }}</span>
            </button>
            <button 
              @click="confirmDetection" 
              :disabled="!detectionResult || detecting"
              class="bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 text-white py-5 rounded-2xl font-bold hover:shadow-2xl hover:scale-105 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-3"
            >
              <svg class="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
              </svg>
              <span>Simpan</span>
            </button>
          </div>
          
          <!-- Manual Input Alternative -->
          <div style="margin-top:10px;" class="pt-3 bg-gradient-to-br from-gray-50 to-blue-50 border-2 border-dashed border-blue-200 rounded-2xl p-6">
            <label class="block text-sm font-bold text-gray-700 mb-4 flex items-center gap-2">
              <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"/>
              </svg>
              Atau masukkan nominal manual:
            </label>
            <div class="flex gap-4">
              <input 
                v-model.number="manualAmount" 
                type="number" 
                class="flex-1 border-2 border-gray-200 bg-white p-4 rounded-2xl outline-none focus:border-purple-500 focus:ring-2 focus:ring-purple-200 transition-all text-lg font-bold" 
                placeholder="Contoh: 50000"
              />
              <button 
                @click="handleSaveMoney" 
                :disabled="!manualAmount || manualAmount <= 0"
                class="bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600 text-white px-8 py-4 rounded-2xl font-bold hover:shadow-2xl hover:scale-105 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Simpan
              </button>
            </div>
          </div>
          
          <!-- Close Button -->
          <button 
            @click="closeCameraModal" 
            class="w-full py-3.5 bg-white text-gray-700 font-bold hover:bg-gray-50 rounded-2xl transition-all duration-300 border-2 border-gray-200"
            style="margin-top:10px;"
            >
            Tutup
          </button>
        </div>
      </div>
    </div>

    <!-- ==================== MODAL: EDIT SAVING ==================== -->
    <div 
      v-if="showEditModal" 
      class="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-4" 
      @click.self="showEditModal = false"
    >
      <div class="bg-white/95 backdrop-blur-xl rounded-3xl shadow-2xl w-full max-w-lg p-10 scale-up-animation border-2 border-purple-100">
        <div class="text-center mb-8">
          <div class="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-br from-blue-500 via-indigo-500 to-purple-500 rounded-2xl mb-4 shadow-lg">
            <svg class="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
            </svg>
          </div>
          <h3 class="text-3xl font-black bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600 bg-clip-text text-transparent">
            Edit Tabungan
          </h3>
        </div>
        <br>
        <div class="space-y-6 pt-3">
          <div>
            <label class="block text-sm font-bold text-gray-700 mb-3 ml-1">Nama Tabungan</label>
            <input 
              v-model="editForm.name" 
              type="text" 
              class="w-full border-2 border-gray-200 bg-gray-50 p-4 rounded-2xl focus:border-purple-500 focus:ring-2 focus:ring-purple-200 focus:bg-white outline-none transition-all"
            />
          </div>
          
          <div class="grid grid-cols-3 gap-4 pt-3">
            <div class="col-span-1">
              <label class="block text-sm font-bold text-gray-700 mb-3 ml-1">Mata Uang</label>
              <select 
                v-model="editForm.currency" 
                class="w-full border-2 border-gray-200 bg-gray-50 p-4 rounded-2xl focus:border-purple-500 focus:bg-white outline-none transition-all font-semibold"
              >
                <option>IDR (Rp)</option>
                <option>USD ($)</option>
              </select>
            </div>
            <div class="col-span-2">
              <label class="block text-sm font-bold text-gray-700 mb-3 ml-1">Target Nominal</label>
              <input 
                v-model.number="editForm.target_amount" 
                type="number" 
                class="w-full border-2 border-gray-200 bg-gray-50 p-4 rounded-2xl focus:border-purple-500 focus:ring-2 focus:ring-purple-200 focus:bg-white outline-none transition-all font-semibold"
              />
            </div>
          </div>
        </div>
        
        <div class="flex justify-end gap-4 mt-10 pt-6 border-t border-gray-200">
          <button 
            @click="showEditModal = false" 
            class="px-8 py-3.5 bg-white text-gray-700 font-bold hover:bg-gray-50 rounded-2xl transition-all duration-300 border-2 border-gray-200"
          >
            Batal
          </button>
          <button 
            @click="handleEditSave" 
            class="px-10 py-3.5 bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600 text-white rounded-2xl font-bold hover:shadow-2xl hover:scale-105 transition-all duration-300 flex items-center gap-2"
          >
            <span>Simpan Perubahan</span>
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- ==================== MODAL: DELETE CONFIRMATION ==================== -->
    <div 
      v-if="showDeleteModal" 
      class="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-4" 
      @click.self="showDeleteModal = false"
    >
      <div class="bg-white/95 backdrop-blur-xl rounded-3xl shadow-2xl w-full max-w-md p-10 scale-up-animation border-2 border-red-100">
        <div class="text-center mb-8">
          <div class="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-br from-red-500 via-pink-500 to-rose-500 rounded-2xl mb-4 shadow-lg animate-pulse">
            <svg class="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
            </svg>
          </div>
          <h3 class="text-3xl font-black bg-gradient-to-r from-red-600 via-pink-600 to-rose-600 bg-clip-text text-transparent">
            Hapus Tabungan?
          </h3>
        </div>
        <br>
        <div class="bg-gradient-to-br from-red-50 to-pink-50 p-6 rounded-2xl border-2 border-red-200 mb-8">
          <p class="text-gray-700 font-bold text-center mb-2">{{ planToDelete?.name }}</p>
          <p class="text-sm text-gray-600 text-center">
            ⚠️ Semua riwayat tabungan juga akan terhapus secara permanen!
          </p>
        </div>
        <br>
        <div class="flex gap-4">
          <button 
            @click="showDeleteModal = false" 
            class="flex-1 px-6 py-3.5 bg-white text-gray-700 font-bold hover:bg-gray-50 rounded-2xl transition-all duration-300 border-2 border-gray-200"
          >
            Batal
          </button>
          <button 
            @click="deletePlan" 
            class="flex-1 px-6 py-3.5 bg-gradient-to-r from-red-600 via-pink-600 to-rose-600 text-white rounded-2xl font-bold hover:shadow-2xl hover:scale-105 transition-all duration-300 flex items-center justify-center gap-2"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
            </svg>
            <span>Ya, Hapus</span>
          </button>
        </div>
      </div>
    </div>

    <!-- ==================== MODAL: LOGOUT CONFIRMATION ==================== -->
    <div 
      v-if="showLogoutModal" 
      class="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-4" 
      @click.self="showLogoutModal = false"
    >
      <div class="bg-white/95 backdrop-blur-xl rounded-3xl shadow-2xl w-full max-w-md p-10 scale-up-animation border-2 border-orange-100">
        <div class="text-center mb-8">
          <div class="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-br from-orange-500 via-red-500 to-pink-500 rounded-2xl mb-4 shadow-lg">
            <svg class="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/>
            </svg>
          </div>
          <h3 class="text-3xl font-black bg-gradient-to-r from-orange-600 via-red-600 to-pink-600 bg-clip-text text-transparent">
            Keluar dari Aplikasi?
          </h3>
        </div>
        <br>
        <div class="bg-gradient-to-br from-orange-50 to-pink-50 p-6 rounded-2xl border-2 border-orange-200 mb-8">
          <p class="text-sm text-gray-600 text-center">
            👋 Kamu akan keluar dari TabunganKu dan perlu login kembali untuk mengakses aplikasi
          </p>
        </div>
        <br>
        <div class="flex gap-4">
          <button 
            @click="showLogoutModal = false" 
            class="flex-1 px-6 py-3.5 bg-white text-gray-700 font-bold hover:bg-gray-50 rounded-2xl transition-all duration-300 border-2 border-gray-200"
          >
            Batal
          </button>
          <button 
            @click="confirmLogout" 
            class="flex-1 px-6 py-3.5 bg-gradient-to-r from-orange-600 via-red-600 to-pink-600 text-white rounded-2xl font-bold hover:shadow-2xl hover:scale-105 transition-all duration-300 flex items-center justify-center gap-2"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/>
            </svg>
            <span>Ya, Keluar</span>
          </button>
        </div>
      </div>
    </div>

    <!-- ==================== MODAL: BONGKAR CONFIRMATION ==================== -->
    <div 
      v-if="showBongkarModal" 
      class="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-4" 
      @click.self="showBongkarModal = false"
    >
      <div class="bg-white/95 backdrop-blur-xl rounded-3xl shadow-2xl w-full max-w-md p-10 scale-up-animation border-2 border-orange-100">
        <div class="text-center mb-8">
          <div class="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-br from-orange-500 via-red-500 to-pink-500 rounded-2xl mb-4 shadow-lg">
            <svg class="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"/>
            </svg>
          </div>
          <h3 class="text-3xl font-black bg-gradient-to-r from-orange-600 via-red-600 to-pink-600 bg-clip-text text-transparent">
            Bongkar Tabungan?
          </h3>
        </div>
        <br>
        <div class="bg-gradient-to-br from-orange-50 to-pink-50 p-6 rounded-2xl border-2 border-orange-200 mb-4">
          <p class="text-sm text-gray-600 text-center mb-3">
            📦 Yakin ingin membongkar tabungan <span class="font-bold text-gray-800">"{{ selectedPlan?.name }}"</span>?
          </p>
          <div class="mt-4 pt-4 border-t border-orange-200">
            <div class="flex items-center justify-between">
              <span class="text-xs font-bold text-gray-600">Total Terkumpul:</span>
              <span class="text-lg font-black text-emerald-600">
                {{ selectedPlan?.currency === 'IDR (Rp)' ? 'Rp' : '$' }} {{ formatNumber(planDetail.total_saved) }}
              </span>
            </div>
          </div>
        </div>
        <br>
        <div class="flex gap-4">
          <button 
            @click="showBongkarModal = false" 
            class="flex-1 px-6 py-3.5 bg-white text-gray-700 font-bold hover:bg-gray-50 rounded-2xl transition-all duration-300 border-2 border-gray-200"
          >
            Batal
          </button>
          <button 
            @click="confirmBongkar" 
            class="flex-1 px-6 py-3.5 bg-gradient-to-r from-orange-600 via-red-600 to-pink-600 text-white rounded-2xl font-bold hover:shadow-2xl hover:scale-105 transition-all duration-300 flex items-center justify-center gap-2"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"/>
            </svg>
            <span>Ya, Bongkar</span>
          </button>
        </div>
      </div>
    </div>

    <!-- ==================== MODAL: SUCCESS NOTIFICATION ==================== -->
    <div 
      v-if="showSuccessModal" 
      class="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-[70] p-4" 
      @click.self="showSuccessModal = false"
    >
      <div class="bg-white/95 backdrop-blur-xl rounded-3xl shadow-2xl w-full max-w-lg p-10 scale-up-animation border-2 border-emerald-100">
        <div class="text-center mb-8">
          <div class="inline-flex items-center justify-center w-24 h-24 bg-gradient-to-br from-emerald-500 via-teal-500 to-cyan-500 rounded-full mb-4 shadow-lg animate-bounce">
            <span class="text-6xl">🎉</span>
          </div>
          <h3 class="text-3xl font-black bg-gradient-to-r from-emerald-600 via-teal-600 to-cyan-600 bg-clip-text text-transparent mb-2">
            Berhasil Menabung!
          </h3>
          <p class="text-gray-600 font-semibold text-lg">
            {{ successData.currency }} {{ formatNumber(successData.amount) }}
          </p>
        </div>
        
        <div class="space-y-4 mb-8" style="margin-top:10px;">
          <div class="bg-gradient-to-br from-blue-50 to-indigo-50 p-5 rounded-2xl border-2 border-blue-200">
            <div class="flex items-center justify-between mb-3">
              <span class="text-sm font-bold text-gray-600 flex items-center gap-2">
                <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                </svg>
                Terdeteksi
              </span>
              <span class="text-lg font-black text-blue-600">{{ successData.banknoteCount }} lembar</span>
            </div>
          </div>

          <div style="margin-top:10px;" class="bg-gradient-to-br from-emerald-50 to-teal-50 p-5 rounded-2xl border-2 border-emerald-200">
            <div class="flex items-center justify-between mb-3">
              <span class="text-sm font-bold text-gray-600 flex items-center gap-2">
                <svg class="w-5 h-5 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 9V7a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2m2 4h10a2 2 0 002-2v-6a2 2 0 00-2-2H9a2 2 0 00-2 2v6a2 2 0 002 2zm7-5a2 2 0 11-4 0 2 2 0 014 0z"/>
                </svg>
                Total Tabungan
              </span>
              <span class="text-lg font-black text-emerald-600">{{ successData.currency }} {{ formatNumber(successData.totalSaved) }}</span>
            </div>
          </div>

          <div style="margin-top:10px;" class="bg-gradient-to-br from-orange-50 to-pink-50 p-5 rounded-2xl border-2 border-orange-200">
            <div class="flex items-center justify-between mb-3">
              <span class="text-sm font-bold text-gray-600 flex items-center gap-2">
                <svg class="w-5 h-5 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"/>
                </svg>
                Sisa Target
              </span>
              <span class="text-lg font-black text-orange-600">{{ successData.currency }} {{ formatNumber(successData.remaining) }}</span>
            </div>
          </div>
        </div>
        
        <button 
          @click="showSuccessModal = false" 
          class="w-full px-8 py-4 bg-gradient-to-r from-emerald-600 via-teal-600 to-cyan-600 text-white rounded-2xl font-bold hover:shadow-2xl hover:scale-105 transition-all duration-300 flex items-center justify-center gap-2"
            style="margin-top:10px;"
          >
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
          </svg>
          <span>Oke, Mantap!</span>
        </button>
      </div>
    </div>

    <!-- ==================== MODAL: UNIVERSAL NOTIFICATION ==================== -->
    <div 
      v-if="showNotificationModal" 
      class="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-[70] p-4" 
      @click.self="showNotificationModal = false"
    >
      <div class="bg-white/95 backdrop-blur-xl rounded-3xl shadow-2xl w-full max-w-md p-10 scale-up-animation border-2"
        :class="{
          'border-emerald-100': notificationData.type === 'success',
          'border-red-100': notificationData.type === 'error',
          'border-orange-100': notificationData.type === 'warning',
          'border-blue-100': notificationData.type === 'info'
        }"
      >
        <div class="text-center mb-6">
          <!-- Icon based on type -->
          <div class="inline-flex items-center justify-center w-20 h-20 rounded-full mb-4 shadow-lg"
            :class="{
              'bg-gradient-to-br from-emerald-500 via-teal-500 to-cyan-500': notificationData.type === 'success',
              'bg-gradient-to-br from-red-500 via-pink-500 to-rose-500 animate-pulse': notificationData.type === 'error',
              'bg-gradient-to-br from-orange-500 via-amber-500 to-yellow-500 animate-pulse': notificationData.type === 'warning',
              'bg-gradient-to-br from-blue-500 via-indigo-500 to-purple-500': notificationData.type === 'info'
            }"
          >
            <!-- Success Icon -->
            <svg v-if="notificationData.type === 'success'" class="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
            </svg>
            <!-- Error Icon -->
            <svg v-else-if="notificationData.type === 'error'" class="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
            <!-- Warning Icon -->
            <svg v-else-if="notificationData.type === 'warning'" class="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
            </svg>
            <!-- Info Icon -->
            <svg v-else class="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
          </div>
          
          <!-- Title -->
          <h3 class="text-2xl font-black mb-2 bg-clip-text text-transparent"
            :class="{
              'bg-gradient-to-r from-emerald-600 via-teal-600 to-cyan-600': notificationData.type === 'success',
              'bg-gradient-to-r from-red-600 via-pink-600 to-rose-600': notificationData.type === 'error',
              'bg-gradient-to-r from-orange-600 via-amber-600 to-yellow-600': notificationData.type === 'warning',
              'bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600': notificationData.type === 'info'
            }"
          >
            {{ notificationData.title }}
          </h3>
          
          <!-- Message -->
          <!-- <p class="text-gray-700 font-semibold text-lg" style="margin-top:7px;margin-bottom:7px;">
            {{ notificationData.message }}
          </p> -->
        </div>
        
        <!-- Details (if any) -->
        <div v-if="notificationData.details" class="mb-6 p-4 rounded-2xl border-2" 
          :class="{
            'bg-gradient-to-br from-emerald-50 to-teal-50 border-emerald-200': notificationData.type === 'success',
            'bg-gradient-to-br from-red-50 to-pink-50 border-red-200': notificationData.type === 'error',
            'bg-gradient-to-br from-orange-50 to-amber-50 border-orange-200': notificationData.type === 'warning',
            'bg-gradient-to-br from-blue-50 to-indigo-50 border-blue-200': notificationData.type === 'info'
          }"
          
        >
          <p class="text-sm text-gray-600 whitespace-pre-line">{{ notificationData.details }}</p>
        </div>
        
        <!-- Close Button -->
        <button
            style="margin-top:25px;" 
          @click="showNotificationModal = false" 
          class="w-full px-8 py-3.5 text-white rounded-2xl font-bold hover:shadow-2xl hover:scale-105 transition-all duration-300 flex items-center justify-center gap-2"
          :class="{
            'bg-gradient-to-r from-emerald-600 via-teal-600 to-cyan-600': notificationData.type === 'success',
            'bg-gradient-to-r from-red-600 via-pink-600 to-rose-600': notificationData.type === 'error',
            'bg-gradient-to-r from-orange-600 via-amber-600 to-yellow-600': notificationData.type === 'warning',
            'bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600': notificationData.type === 'info'
          }"
        >
          <span>Oke</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()

// ==================== STATE MANAGEMENT ====================
const currentTab = ref('tabungan')
const showCreateModal = ref(false)
const showDetailModal = ref(false)
const showCameraModal = ref(false)
const showEditModal = ref(false)
const showDeleteModal = ref(false)
const showLogoutModal = ref(false)
const showBongkarModal = ref(false)
const showSuccessModal = ref(false)
const showNotificationModal = ref(false)
const showMenu = ref(null)
const planToDelete = ref(null)
const successData = ref({
  amount: 0,
  currency: '',
  banknoteCount: 0,
  totalSaved: 0,
  remaining: 0
})
const notificationData = ref({
  type: 'success', // 'success', 'error', 'warning', 'info'
  title: '',
  message: '',
  details: ''
})

// Notification helper function
const showNotification = (type, title, message, details = '') => {
  notificationData.value = { type, title, message, details }
  showNotificationModal.value = true
}

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
  currency: 'IDR (Rp)',
  target_date: ''
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

// Helper functions for list items
const calculateCollected = (planId) => {
  const plan = activePlans.value.find(p => p.id === planId)
  if (!plan) return 0
  // This will be populated from backend, for now return 0
  // You should fetch this from backend in real implementation
  return plan.total_saved || 0
}

const calculateProgress = (planId) => {
  const plan = activePlans.value.find(p => p.id === planId)
  if (!plan || !plan.target_amount) return 0
  const collected = calculateCollected(planId)
  return Math.min((collected / plan.target_amount) * 100, 100)
}

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

// Calculate remaining days from target date
const calculateRemainingDays = (targetDate) => {
  if (!targetDate) return 'Tanpa target waktu'
  
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  
  const target = new Date(targetDate)
  target.setHours(0, 0, 0, 0)
  
  const diffTime = target - today
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
  
  if (diffDays < 0) {
    return `⏰ Terlambat ${Math.abs(diffDays)} hari`
  } else if (diffDays === 0) {
    return '⏰ Target hari ini!'
  } else if (diffDays === 1) {
    return '⏰ Besok adalah batas waktu!'
  } else if (diffDays <= 7) {
    return `⏰ ${diffDays} hari lagi`
  } else if (diffDays <= 30) {
    return `📅 ${diffDays} hari lagi`
  } else {
    const months = Math.floor(diffDays / 30)
    const days = diffDays % 30
    if (days === 0) {
      return `📅 ${months} bulan lagi`
    }
    return `📅 ${months} bulan ${days} hari lagi`
  }
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
    const activePlansData = response.data.active_plans || []
    const brokenPlansData = response.data.history_plans || []
    
    // Fetch total_saved untuk setiap active plan
    for (let plan of activePlansData) {
      try {
        const detailResponse = await axios.get(`http://127.0.0.1:8000/plans/${plan.id}/logs`)
        plan.total_saved = detailResponse.data.total_saved || 0
        plan.progress_percentage = detailResponse.data.progress_percentage || 0
      } catch (err) {
        console.error(`Error fetching details for plan ${plan.id}:`, err)
        plan.total_saved = 0
        plan.progress_percentage = 0
      }
    }
    
    activePlans.value = activePlansData
    brokenPlans.value = brokenPlansData
  } catch (error) {
    console.error('Error fetching plans:', error)
    showNotification('error', 'Gagal Mengambil Data', 'Tidak dapat mengambil data tabungan')
  }
}

// Create new saving plan
const handleCreate = async () => {
  if (!newPlan.value.name || newPlan.value.target_amount <= 0) {
    showNotification('warning', 'Data Tidak Lengkap', 'Harap isi semua data dengan benar!')
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
    showNotification('success', 'Berhasil!', 'Tabungan berhasil dibuat')
    await fetchPlans()
  } catch (error) {
    console.error('Error creating plan:', error)
    showNotification('error', 'Gagal Membuat Tabungan', 'Terjadi kesalahan saat membuat tabungan')
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
    showNotification('error', 'Gagal Mengambil Data', 'Tidak dapat mengambil detail tabungan')
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
    showNotification('warning', 'Nominal Tidak Valid', 'Masukkan nominal yang valid!')
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
    successData.value = {
      amount: manualAmount.value,
      currency: currency,
      banknoteCount: 0,
      totalSaved: response.data.total_saved,
      remaining: response.data.remaining
    }
    showSuccessModal.value = true
    
    manualAmount.value = 0
    
    // Refresh data
    await openDetail(selectedPlan.value)
    await fetchPlans()
  } catch (error) {
    console.error('Error saving money:', error)
    showNotification('error', 'Gagal Menyimpan', 'Terjadi kesalahan saat menyimpan uang')
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
    showNotification('warning', 'Kamera Belum Siap', 'Tunggu hingga kamera aktif')
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
      showNotification('warning', 'Tidak Ada Uang Terdeteksi', 
        'Silakan coba lagi dengan pencahayaan yang lebih baik',
        '• Letakkan uang di permukaan datar\n• Pastikan uang terlihat jelas di kamera')
    }
  } catch (error) {
    detecting.value = false
    console.error('Detection error:', error)
    
    if (error.response && error.response.status === 404) {
      showNotification('error', 'Endpoint Tidak Tersedia', 
        'Fitur deteksi belum tersedia',
        'Silakan gunakan input manual atau hubungi administrator')
    } else {
      showNotification('error', 'Gagal Mendeteksi', 
        'Terjadi kesalahan saat mendeteksi uang',
        error.response?.data?.detail || error.message)
    }
  }
}

// Confirm detection and save to database
const confirmDetection = async () => {
  if (!detectionResult.value || !detectionResult.value.total) {
    showNotification('warning', 'Belum Ada Hasil', 'Belum ada hasil deteksi!')
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
    successData.value = {
      amount: totalAmount,
      currency: currency,
      banknoteCount: banknoteCount,
      totalSaved: response.data.total_saved,
      remaining: response.data.remaining
    }
    showSuccessModal.value = true
    
    // Reset state
    detectionResult.value = null
    manualAmount.value = 0
    
    // Refresh data
    await openDetail(selectedPlan.value)
    await fetchPlans()
  } catch (error) {
    console.error('Error saving detected money:', error)
    showNotification('error', 'Gagal Menyimpan', 'Gagal menyimpan uang hasil deteksi')
  }
}

// ==================== END CAMERA FUNCTIONS ====================

// Break/archive saving plan
const handleBongkar = () => {
  showBongkarModal.value = true
}

const confirmBongkar = async () => {
  const currency = selectedPlan.value.currency === 'IDR (Rp)' ? 'Rp' : '$'
  
  showBongkarModal.value = false

  try {
    await axios.put(`http://127.0.0.1:8000/plans/bongkar/${selectedPlan.value.id}`)
    
    showNotification('success', 'Berhasil Dibongkar!', 
      `Tabungan "${selectedPlan.value.name}" berhasil dibongkar`,
      `Total yang terkumpul: ${currency} ${formatNumber(planDetail.value.total_saved)}`)
    
    closeDetailModal()
    await fetchPlans()
    currentTab.value = 'riwayat'
  } catch (error) {
    console.error('Error breaking plan:', error)
    showNotification('error', 'Gagal Membongkar', 'Terjadi kesalahan saat membongkar tabungan')
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

// Confirm delete - show modal
const confirmDelete = (plan) => {
  planToDelete.value = plan
  showDeleteModal.value = true
}

// Delete saving plan
const deletePlan = async () => {
  if (!planToDelete.value) return
  
  try {
    await axios.delete(`http://127.0.0.1:8000/plans/${planToDelete.value.id}`)
    showDeleteModal.value = false
    planToDelete.value = null
    showNotification('success', 'Berhasil Dihapus!', 'Tabungan berhasil dihapus')
    await fetchPlans()
  } catch (error) {
    console.error('Error deleting plan:', error)
    showNotification('error', 'Gagal Menghapus', 'Terjadi kesalahan saat menghapus tabungan')
  }
}

// Save edited plan
const handleEditSave = async () => {
  if (!editForm.value.name || editForm.value.target_amount <= 0) {
    showNotification('warning', 'Data Tidak Lengkap', 'Harap isi semua data dengan benar!')
    return
  }

  try {
    await axios.put(
      `http://127.0.0.1:8000/plans/edit/${selectedPlan.value.id}`, 
      editForm.value
    )
    
    showNotification('success', 'Berhasil Diupdate!', 'Tabungan berhasil diupdate')
    showEditModal.value = false
    await fetchPlans()
  } catch (error) {
    console.error('Error updating plan:', error)
    showNotification('error', 'Gagal Mengupdate', 'Terjadi kesalahan saat mengupdate tabungan')
  }
}

// Logout function
const handleLogout = () => {
  showLogoutModal.value = true
}

// Confirm logout
const confirmLogout = () => {
  localStorage.removeItem('user')
  router.push('/login')
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

/* Hide scrollbars for detail and camera modals */
div[style*="scrollbar-width"]::-webkit-scrollbar {
  display: none;
}
</style>
