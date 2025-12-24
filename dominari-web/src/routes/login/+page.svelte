<script lang="ts">
    // dominari-web/src/routes/login/+page.svelte
    import { login } from '$lib/stores/userStore';
    import { goto } from '$app/navigation';

    let phone = '';
    let password = '';
    let errorMessage = '';
    let isLoading = false;

    async function handleLogin(e) {
        if (!phone || !password) {
            errorMessage = 'Lütfen tüm alanları doldurun."';
            return;
        }

        isLoading = true;
        errorMessage = '';

        const result = await login(phone, password);

        if (result.success) {
            goto('/select-office');
        } else {
            errorMessage = result.message || 'Giriş yapılamadı.';
        }
        
        isLoading = false;
    }
</script>

<div class="min-h-screen flex items-center justify-center bg-gray-50 px-4">
    <div class="max-w-md w-full space-y-8 p-10 bg-white rounded-xl shadow-lg border border-gray-100">
        <div class="text-center">
            <h2 class="mt-6 text-3xl font-extrabold text-gray-900">
                Dominari SaaS
            </h2>
            <p class="mt-2 text-sm text-gray-600">
                Lütfen giriş bilgilerinizi girin
            </p>
        </div>
        
        <form class="mt-8 space-y-6" on:submit|preventDefault={handleLogin}>
            <div class="rounded-md shadow-sm -space-y-px">
                <div>
                    <label for="phone" class="sr-only">Telefon veya Admin ID</label>
                    <input 
                        id="phone" 
                        type="text" 
                        bind:value={phone}
                        required 
                        class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm" 
                        placeholder="Telefon veya Admin ID (A1, A2...)"
                        disabled={isLoading}
                    >
                </div>
                <div>
                    <label for="password" class="sr-only">Şifre</label>
                    <input 
                        id="password" 
                        type="password" 
                        bind:value={password}
                        required 
                        class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm" 
                        placeholder="Şifre"
                        disabled={isLoading}
                    >
                </div>
            </div>

            {#if errorMessage}
                <div class="text-red-500 text-sm text-center bg-red-50 p-2 rounded">
                    {errorMessage}
                </div>
            {/if}

            <div>
                <button 
                    type="submit" 
                    disabled={isLoading}
                    class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                    <span class="absolute left-0 inset-y-0 flex items-center pl-3">
                        {#if isLoading}
                            <svg class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                            </svg>
                        {:else}
                            <svg class="h-5 w-5 text-blue-500 group-hover:text-blue-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                                <path fill-rule="evenodd" d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z" clip-rule="evenodd" />
                            </svg>
                        {/if}
                    </span>
                    {isLoading ? 'Bağlanıyor...' : 'Giriş Yap'}
                </button>
            </div>
        </form>
    </div>
</div>