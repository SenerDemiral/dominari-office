<script lang="ts">
    // dominari-web/src/routes/+layout.svelte
	import './layout.css';
	import favicon from '$lib/assets/favicon.svg';

    import { onMount } from 'svelte';
    import { userSession } from '$lib/stores/userStore';
    import { browser } from '$app/environment';
	
	let { children } = $props();

    onMount(async () => {
        if (!browser) return;

        const token = localStorage.getItem('token');
        
        if (token) {
            try {
                // Sessizce backend'e gidip "Ben kimim?" diye soruyoruz
                const response = await fetch('/api/me', {
                    headers: { 'Authorization': `Bearer ${token}` }
                });

                if (response.ok) {
                    const data = await response.json();
                    
                    // DB'den gelen güncel bilgilerle store'u doldur
                    userSession.set({
                        isLoggedIn: true,
                        isChecking: false,
                        token: token,
                        user: data.user, // İsim burada doluyor!
						activeOffice: null,
                        staffOffices: data.offices.filter(o => o.is_staff),
                        clientOffices: data.offices.filter(o => !o.is_staff)
                    });
                } else {
                    // Token geçersizse veya süresi dolmuşsa temizle
                    localStorage.removeItem('token');
                    userSession.update(s => ({ ...s, isLoggedIn: false, isChecking: false }));
                }
            } catch (error) {
                console.error("Doğrulama hatası:", error);
                userSession.update(s => ({ ...s, isChecking: false }));
            }
        } else {
            // Hiç token yoksa kontrolü bitir
            userSession.update(s => ({ ...s, isChecking: false }));
        }
    });

//<svelte:head><link rel="icon" href={favicon} /></svelte:head>
//{@render children()}

</script>

{#if $userSession.isChecking}
    <div class="flex items-center justify-center h-screen bg-slate-50 text-emerald-600 font-bold">
        Dominari yükleniyor...
    </div>
{:else}
    {@render children()}
{/if}


