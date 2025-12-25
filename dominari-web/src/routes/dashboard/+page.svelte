<script lang="ts">
    import { userSession } from '$lib/stores/userStore';
    import { goto } from '$app/navigation';
    import { browser } from '$app/environment';

    // Sadece kontrol bittikten sonra ve giriş yoksa login'e at
    $effect(() => {
        if (browser && !$userSession.isChecking && !$userSession.isLoggedIn) {
            goto('/login');
        }
    });
</script>

{#if $userSession.isChecking}
    <div class="flex items-center justify-center h-screen bg-slate-50">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-emerald-500"></div>
        <p class="ml-4 text-slate-600 font-medium">Oturum doğrulanıyor...</p>
    </div>
{:else if $userSession.isLoggedIn}
    <div class="p-8">
        <h3 class="text-2xl font-bold text-slate-800 mb-6 font-sans">Genel Bakış</h3>
        
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div class="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
                <p class="text-xs text-slate-500 uppercase font-bold tracking-wider mb-2">Toplam Müşteri</p>
                <p class="text-3xl font-bold text-slate-800">
                    {$userSession.user?.name === 'Klinik A Admin' ? '124' : '--'}
                </p>
            </div>
            </div>
    </div>
{/if}