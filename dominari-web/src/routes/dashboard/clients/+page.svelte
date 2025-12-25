<script lang="ts">
    import { onMount } from 'svelte';
    import { userSession } from '$lib/stores/userStore';
    import { phoneDisplay } from '$lib/utils';

    // Durum Değişkenleri
    let clients = [];
    let loading = true;
    let error = null;
    let showModal = false;

    // Yeni Müşteri Form Verisi
    let newClient = {
        name: '',
        phone: '',
        email: '',
        status: 'Aktif'
    };

    // 1. Müşterileri Listeleme Fonksiyonu
    async function fetchClients() {
        loading = true;
        const officeId = $userSession.activeOffice?.id;
        const token = $userSession.token;

        if (!officeId) {
            error = "Lütfen önce bir ofis seçin.";
            loading = false;
            return;
        }

        try {
            const response = await fetch(`/api/offices/${officeId}/clients`, {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            if (response.ok) {
                clients = await response.json();
                error = null;
            } else {
                error = "Müşteri listesi yüklenirken bir sorun oluştu.";
            }
        } catch (err) {
            error = "Sunucuya bağlanılamadı.";
        } finally {
            loading = false;
        }
    }

    // 2. Yeni Müşteri Kaydetme Fonksiyonu
    async function addClient() {
        const officeId = $userSession.activeOffice?.id;
        
        try {
            const response = await fetch(`/api/offices/${officeId}/clients`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${$userSession.token}`
                },
                body: JSON.stringify(newClient)
            });

            if (response.ok) {
                showModal = false; // Modalı kapat
                newClient = { name: '', phone: '', email: '', status: 'Aktif' }; // Formu sıfırla
                await fetchClients(); // Listeyi güncelle
            } else {
                alert("Kayıt sırasında bir hata oluştu.");
            }
        } catch (err) {
            console.error("Hata:", err);
        }
    }

    // Sayfa açıldığında verileri çek
    onMount(fetchClients);
</script>

<div class="flex justify-between items-center mb-8">
    <div>
        <h1 class="text-2xl font-bold text-slate-800">Müşteriler</h1>
        <p class="text-slate-500">Ofisinizdeki müşteri kayıtlarını buradan yönetebilirsiniz.</p>
    </div>
    <button 
        on:click={() => showModal = true}
        class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg font-medium transition-all shadow-sm flex items-center gap-2"
    >
        <span class="text-xl">+</span> Yeni Müşteri Ekle
    </button>
</div>

{#if loading}
    <div class="flex flex-col items-center justify-center p-20 text-slate-400">
        <div class="animate-spin rounded-full h-10 w-10 border-b-2 border-blue-600 mb-4"></div>
        <p>Müşteriler yükleniyor...</p>
    </div>
{:else if error}
    <div class="bg-red-50 text-red-700 p-4 rounded-lg border border-red-100 mb-6">
        {error}
    </div>
{:else}
    <div class="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
        <table class="w-full text-left border-collapse">
            <thead class="bg-slate-50 border-b border-slate-200">
                <tr>
                    <th class="p-4 font-semibold text-slate-600">Müşteri Adı</th>
                    <th class="p-4 font-semibold text-slate-600">Telefon</th>
                    <th class="p-4 font-semibold text-slate-600">E-posta</th>
                    <th class="p-4 font-semibold text-slate-600">Durum</th>
                    <th class="p-4 text-right">İşlemler</th>
                </tr>
            </thead>
            <tbody>
                {#each clients as client}
                    <tr class="border-b border-slate-100 hover:bg-slate-50 transition-colors">
                        <td class="p-4 text-slate-800 font-medium">{client.name}</td>
                        <td class="p-4 text-slate-600 underline decoration-slate-300 underline-offset-4">
                            {phoneDisplay(client.phone)}
                        </td>
                        <td class="p-4 text-slate-600">{client.email}</td>
                        <td class="p-4">
                            <span class="px-2 py-1 text-xs rounded-full {client.status === 'Aktif' ? 'bg-green-100 text-green-700' : 'bg-amber-100 text-amber-700'}">
                                {client.status}
                            </span>
                        </td>
                        <td class="p-4 text-right">
                            <button class="text-blue-600 hover:underline text-sm font-medium">Detay</button>
                        </td>
                    </tr>
                {:else}
                    <tr>
                        <td colspan="4" class="p-16 text-center">
                            <div class="text-slate-400">
                                <p class="text-lg">Henüz hiç müşteri kaydı yok.</p>
                                <p class="text-sm">Yeni bir müşteri ekleyerek başlayabilirsiniz.</p>
                            </div>
                        </td>
                    </tr>
                {/each}
            </tbody>
        </table>
    </div>
{/if}

{#if showModal}
    <div class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm p-4">
        <div class="bg-white rounded-2xl shadow-2xl w-full max-w-md overflow-hidden">
            <div class="p-6 border-b border-slate-100">
                <h2 class="text-xl font-bold text-slate-800">Yeni Müşteri Oluştur</h2>
            </div>
            
            <div class="p-6 space-y-4">
                <div>
                    <label class="block text-sm font-medium text-slate-700 mb-1">Ad Soyad</label>
                    <input 
                        bind:value={newClient.name}
                        type="text" 
                        placeholder="Örn: Ahmet Yılmaz"
                        class="w-full border border-slate-300 p-2.5 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all"
                    />
                </div>
                
                <div>
                    <label class="block text-sm font-medium text-slate-700 mb-1">Telefon Numarası</label>
                    <input 
                        bind:value={newClient.phone}
                        type="text" 
                        placeholder="05xx xxx xx xx"
                        class="w-full border border-slate-300 p-2.5 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all"
                    />
                </div>

                <div>
                    <label class="block text-sm font-medium text-slate-700 mb-1">E-posta Adresi</label>
                    <input 
                        bind:value={newClient.email}
                        type="text" 
                        placeholder="ornek@dominari.cloud"
                        class="w-full border border-slate-300 p-2.5 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all"
                    />
                </div>

            </div>

            <div class="p-6 bg-slate-50 flex justify-end gap-3">
                <button 
                    on:click={() => showModal = false}
                    class="px-4 py-2 text-slate-600 font-medium hover:text-slate-800 transition-colors"
                >
                    İptal
                </button>
                <button 
                    on:click={addClient}
                    class="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg font-bold transition-all shadow-md"
                    disabled={!newClient.name}
                >
                    Kaydet
                </button>
            </div>
        </div>
    </div>
{/if}