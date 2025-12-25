<script lang="ts">
    import { userSession } from '$lib/stores/userStore';
    import { goto } from '$app/navigation';
    import { onMount } from 'svelte';

    // Sayfa tarayıcıya tam yüklendiğinde çalışır
    onMount(() => {
        if (!$userSession.isLoggedIn) {
            goto('/login');
        }
    });

    function selectOffice(office: any) {
        userSession.update(s => ({ ...s, activeOffice: office }));
        console.log("Seçilen ofis:", office.name);
        goto('/dashboard');
    }

</script>

<div class="min-h-screen bg-gray-900 text-white p-8">
    <div class="max-w-4xl mx-auto">
        <h1 class="text-3xl font-bold mb-2">
            Hoş geldin, {$userSession?.user?.name || 'Kullanıcı'}
        </h1>
        <p class="text-gray-400 mb-8">Lütfen devam etmek için bir ofis seçiniz:</p>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            {#each $userSession?.staffOffices || [] as office}
                <button on:click={() => selectOffice(office)} class="bg-gray-800 p-6 rounded-xl border border-gray-700 hover:border-blue-500 text-left transition-all">
                    <div class="flex justify-between">
                        <span class="font-bold text-lg">{office.name}</span>
                        <span class="text-xs text-blue-400 bg-blue-900/30 px-2 py-1 rounded">Yönetici</span>
                    </div>
                    <p class="text-sm text-gray-500 mt-2">Panele git →</p>
                </button>
            {/each}

            {#each $userSession?.clientOffices || [] as office}
                <button on:click={() => selectOffice(office)} class="bg-gray-800 p-6 rounded-xl border border-gray-700 hover:border-green-500 text-left transition-all">
                    <div class="flex justify-between">
                        <span class="font-bold text-lg">{office.name}</span>
                        <span class="text-xs text-green-400 bg-green-900/30 px-2 py-1 rounded">Müşteri</span>
                    </div>
                    <p class="text-sm text-gray-500 mt-2">Hizmetlere git →</p>
                </button>
            {/each}
        </div>
    </div>
</div>