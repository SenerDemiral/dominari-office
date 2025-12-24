<script lang="ts">
    // dominari-web/src/routes/+layout.svelte
    import { goto } from '$app/navigation';
    import { browser } from '$app/environment';
    import { userSession } from '$lib/stores/userStore';

    export const ssr = false;

    // Svelte 5 efekti: Sadece durum değiştiğinde ve KONTROL BİTTİĞİNDE çalışır
    $effect(() => {
        if (browser && !$userSession.isChecking) {
            if (!$userSession.isLoggedIn) {
                console.log("Yetki yok, Giriş sayfasına...");
                goto('/login');
            } else if ($userSession.staffOffices.length > 0) {
                // Kullanıcıyı ofis seçimine veya ana ekrana atmak istersen:
                goto('/select-office'); 
                console.log("Kullanıcı doğrulandı: ", $userSession.user?.name);
            }
        }
    });
</script>

<div class="flex flex-col items-center justify-center h-screen w-full bg-slate-50 font-sans">
    <div class="relative flex items-center justify-center">
        <div class="w-16 h-16 border-4 border-emerald-100 border-t-emerald-500 rounded-full animate-spin"></div>
        <div class="absolute text-emerald-600 font-bold text-xs">DC</div>
    </div>

    <h1 class="text-2xl font-bold text-emerald-600 mt-6 tracking-tight">
        Dominari Cloud XXXX
    </h1>
    
    <div class="flex items-center space-x-2 mt-2">
        <span class="relative flex h-3 w-3">
            <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
            <span class="relative inline-flex rounded-full h-3 w-3 bg-emerald-500"></span>
        </span>
        <p class="text-slate-500 text-sm font-medium">Güvenli bağlantı doğrulanıyor...</p>
    </div>
</div>