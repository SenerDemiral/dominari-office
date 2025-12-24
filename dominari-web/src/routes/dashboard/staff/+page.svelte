<script lang="ts">
    import StaffEditModal from '$lib/components/modals/StaffEditModal.svelte';
    import { onMount } from 'svelte';
    import { userSession } from '$lib/stores/userStore';
    import { phoneDisplay } from '$lib/utils';

    interface StaffMember {
        ou_id: number;
        user_id: number;
        name: string;
        phone: string;
        email: string;
        is_active: boolean;
        is_bookable: boolean;
        role: string;
    }
    // --- Svelte 5 Runes (Reaktif Değişkenler) ---
    let isModalOpen = $state(false);
    let selectedStaff = $state(null);
    let showAddModal = $state(false); // Yeni personel ekleme modalı için
    let staffList = $state<StaffMember[]>([]);
    let loading = $state(true);
    let error = $state(null);

    // Yeni Personel Form Verisi
    let newStaff = $state({
        name: '',
        phone: '',
        email: '',
        is_bookable: true,
        role: 'assistant'
    });

    // 1. Listeyi Çekme
    async function fetchStaff() {
        loading = true;
        const officeId = $userSession.activeOffice?.id;
        
        if (!officeId) {
            error = "Lütfen önce bir ofis seçin.";
            loading = false;
            return;
        }

        try {
            const response = await fetch(`/api/offices/${officeId}/staff`, {
                headers: { 'Authorization': `Bearer ${$userSession.token}` }
            });

            if (response.ok) {
                staffList = await response.json();
                error = null;
            } else {
                error = "Personel listesi yüklenirken bir sorun oluştu.";
            }
        } catch (err) {
            error = "Sunucuya bağlanılamadı.";
        } finally {
            loading = false;
        }
    }

    // 2. Personel Güncelleme (Modal'dan çağrılır)
    async function handleSave(ou_id: number, settings: Partial<StaffMember>) {
        try {
            const response = await fetch(`/api/offices/staff/settings/${ou_id}`, {
                method: 'PATCH',
                headers: { 
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${$userSession.token}`
                },
                body: JSON.stringify(settings)
            });
            if (response.ok) {
                // Map ile sadece değişen satırı bulup güncelliyoruz
                staffList = staffList.map(s => s.ou_id === ou_id ? { ...s, ...settings } : s);
                isModalOpen = false;
            }

        } catch (err) {
            console.error("Güncelleme hatası:", err);
        }
    }

    // 3. Yeni Personel Ekleme
    async function addStaff() {
        const officeId = $userSession.activeOffice?.id;
        try {
            const response = await fetch(`/api/offices/${officeId}/staff`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${$userSession.token}`
                },
                body: JSON.stringify(newStaff)
            });

            if (response.ok) {
                showAddModal = false;
                newStaff = { name: '', phone: '', email: '', is_bookable: true, role: 'assistant' };
                await fetchStaff();
            }
        } catch (err) {
            console.error("Ekleme hatası:", err);
        }
    }

    onMount(fetchStaff);
</script>

<div class="flex justify-between items-center mb-8">
    <div>
        <h1 class="text-2xl font-bold text-slate-800 tracking-tight">Personel Yönetimi</h1>
        <p class="text-slate-500 text-sm">Ofisinizdeki ekibi ve yetkilerini buradan yönetin.</p>
    </div>
    <button 
        onclick={() => showAddModal = true}
        class="bg-emerald-600 hover:bg-emerald-700 text-white px-5 py-2.5 rounded-xl font-bold transition-all shadow-lg shadow-emerald-100 flex items-center gap-2"
    >
        <span class="text-xl">+</span> Yeni Personel
    </button>
</div>

{#if loading}
    <div class="flex flex-col items-center justify-center p-20 text-slate-400">
        <div class="animate-spin rounded-full h-10 w-10 border-b-2 border-emerald-600 mb-4"></div>
        <p class="font-medium">Veriler getiriliyor...</p>
    </div>
{:else if error}
    <div class="bg-red-50 text-red-700 p-4 rounded-xl border border-red-100 mb-6 flex items-center gap-3">
        <span class="text-xl">⚠️</span> {error}
    </div>
{:else}
    <div class="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
        <table class="w-full text-left border-collapse">
            <thead class="bg-slate-50/50 border-b border-slate-200">
                <tr>
                    <th class="p-4 font-bold text-slate-600 text-xs uppercase tracking-wider">Ad Soyad</th>
                    <th class="p-4 font-bold text-slate-600 text-xs uppercase tracking-wider">İletişim</th>
                    <th class="p-4 font-bold text-slate-600 text-xs uppercase tracking-wider">Aktif</th>
                    <th class="p-4 font-bold text-slate-600 text-xs uppercase tracking-wider text-center">Randevu</th>
                    <th class="p-4 font-bold text-slate-600 text-xs uppercase tracking-wider text-center">Durum</th>
                    <th class="p-4 text-right"></th>
                </tr>
            </thead>
            <tbody class="divide-y divide-slate-100">
                {#each staffList as staffMember}
                    <tr class="hover:bg-slate-50/80 transition-colors group">
                        <td class="p-4">
                            <div class="font-bold text-slate-800">{staffMember.name}</div>
                            <div class="text-xs text-slate-400 capitalize">{staffMember.role}</div>
                        </td>
                        <td class="p-4">
                            <div class="text-sm text-slate-600 font-medium">{phoneDisplay(staffMember.phone)}</div>
                            <div class="text-xs text-slate-400">{staffMember.email || '-'}</div>
                        </td>
                        <td class="p-4 text-center">
                            <span class="px-2.5 py-1 text-[10px] font-black rounded-lg {staffMember.is_active ? 'bg-emerald-100 text-emerald-700' : 'bg-red-100 text-red-700'}">
                                {staffMember.is_active ? 'AKTİF' : 'PASİF'}
                            </span>
                        </td>
                        <td class="p-4 text-center">
                            <span class="px-2.5 py-1 text-[10px] font-black rounded-lg {staffMember.is_bookable ? 'bg-blue-100 text-blue-700' : 'bg-slate-100 text-slate-400'}">
                                {staffMember.is_bookable ? 'AÇIK' : 'KAPALI'}
                            </span>
                        </td>
                        <td class="p-4 text-right">
                            <button 
                                onclick={() => { selectedStaff = staffMember; isModalOpen = true; }}
                                class="opacity-0 group-hover:opacity-100 bg-slate-100 hover:bg-emerald-600 hover:text-white text-slate-600 px-4 py-1.5 rounded-lg text-xs font-bold transition-all"
                            >
                                DÜZENLE
                            </button>
                        </td>
                    </tr>
                {/each}
            </tbody>
        </table>
    </div>
{/if}

<StaffEditModal 
    isOpen={isModalOpen} 
    staff={selectedStaff} 
    onClose={() => isModalOpen = false} 
    onSave={handleSave} 
/>

{#if showAddModal}
    <div class="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/50 backdrop-blur-sm p-4">
        <div class="bg-white rounded-2xl shadow-2xl w-full max-w-md p-6 border border-slate-200">
            <h2 class="text-xl font-bold text-slate-800 mb-6">Yeni Personel Ekle</h2>
            <div class="space-y-4">
                <input bind:value={newStaff.name} placeholder="Ad Soyad" class="w-full border-slate-200 rounded-lg text-sm" />
                <input bind:value={newStaff.phone} placeholder="Telefon" class="w-full border-slate-200 rounded-lg text-sm" />
                <select bind:value={newStaff.role} class="w-full border-slate-200 rounded-lg text-sm">
                    <option value="doctor">Doktor</option>
                    <option value="assistant">Asistan</option>
                    <option value="secretary">Sekreter</option>
                </select>
            </div>
            <div class="mt-8 flex justify-end gap-3">
                <button onclick={() => showAddModal = false} class="text-slate-400 font-bold text-sm px-4">İptal</button>
                <button onclick={addStaff} class="bg-emerald-600 text-white px-6 py-2 rounded-lg font-bold text-sm">Kaydet</button>
            </div>
        </div>
    </div>
{/if}