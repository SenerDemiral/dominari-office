<script lang="ts">
    // dominari-web/src/routes/dashboard/+layout.svelte
    import { userSession } from '$lib/stores/userStore';
    import { goto } from '$app/navigation';
    import { onMount } from 'svelte';
    
    let isMenuOpen = false; // Menü kapalı başlasın

    onMount(() => {
        if (!$userSession.isLoggedIn) {
            goto('/login');
        } else if (!$userSession.activeOffice) {
            goto('/select-office');
        }
    });
</script>

<div class="min-h-screen bg-gray-50 flex flex-col md:flex-row">
    <div class="md:hidden bg-slate-900 text-white p-4 flex justify-between items-center">
        <div class="text-xl font-bold">Dominari</div>
        <button on:click={() => isMenuOpen = !isMenuOpen} class="text-2xl">
            {isMenuOpen ? '✕' : '☰'}
        </button>
    </div>

    <aside class="w-full md:w-64 bg-slate-900 text-white {isMenuOpen ? 'flex' : 'hidden'} md:flex flex-col">
        <div class="p-6 text-xl font-bold border-b border-slate-800 hidden md:block">Dominari</div>
        <nav class="p-4 flex-1 space-y-2">
            <a href="/dashboard" on:click={() => isMenuOpen = false} class="block p-3 hover:bg-slate-800 rounded-lg">Genel Bakış</a>
            <a href="/dashboard/clients" on:click={() => isMenuOpen = false} class="block p-3 hover:bg-slate-800 rounded-lg">👥Müşteriler</a>
            <a href="/dashboard/staff" on:click={() => isMenuOpen = false} class="block p-3 hover:bg-slate-800 rounded-lg">👷🏻Personel</a>
        </nav>
        <div class="p-4 border-t border-slate-800">
            <button on:click={() => goto('/select-office')} class="text-sm text-slate-400 hover:text-white">
                ← Ofis Değiştir
            </button>
        </div>
    </aside>

    <main class="flex-1 flex flex-col">
        <header class="bg-white shadow-sm p-4 flex justify-between items-center">
            <h2 class="text-xl font-semibold text-slate-800">{$userSession.activeOffice?.name}</h2>
            <span class="text-sm bg-blue-50 text-blue-700 px-3 py-1 rounded-full">
                {$userSession.user?.name}
            </span>
        </header>

        <div class="p-4 md:p-8">
            <slot />
        </div>
    </main>
</div>