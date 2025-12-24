<script lang="ts">
    import { fade, scale } from 'svelte/transition';

    // Props: isOpen (modal açık mı?), staff (seçili personel), onClose, onSave
    let { isOpen, staff, onClose, onSave } = $props();

    // Modal içindeki geçici form state'i (Svelte 5 runes)
    let form = $state({
        is_active: false,
        is_bookable: false,
        role: ''
    });

    // Her personel değiştiğinde formu doldur
    $effect(() => {
        if (staff) {
            form.is_active = staff.is_active;
            form.is_bookable = staff.is_bookable;
            form.role = staff.role;
        }
    });

    async function handleSave() {
        await onSave(staff.ou_id, form); // ou_id üzerinden jsonb gönderiyoruz
        onClose();
    }
</script>

{#if isOpen}
    <div class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm" 
         transition:fade={{ duration: 200 }}
         onclick={onClose}>
        
        <div class="bg-white w-full max-w-md rounded-2xl shadow-2xl border border-slate-200 overflow-hidden"
             transition:scale={{ start: 0.95, duration: 200 }}
             onclick={(e) => e.stopPropagation()}>
            
            <div class="px-6 py-4 border-b border-slate-100 bg-slate-50 flex justify-between items-center">
                <div>
                    <h3 class="text-lg font-bold text-slate-800">{staff?.name} </h3>
                    <p class="text-xs text-slate-500 font-medium tracking-wide uppercase">Personel Ayarları</p>
                </div>
                <button onclick={onClose} class="text-slate-400 hover:text-slate-600 transition-colors text-2xl">&times;</button>
            </div>

            <div class="p-6 space-y-6">
                <div>
                    <label class="block text-sm font-semibold text-slate-700 mb-2">Görev / Rol</label>
                    <select bind:value={form.role} class="w-full rounded-lg border-slate-200 bg-slate-50 text-sm focus:ring-emerald-500 focus:border-emerald-500">
                        <option value="doctor">Doktor</option>
                        <option value="secretary">Sekreter</option>
                        <option value="assistant">Asistan</option>
                    </select>
                </div>

                <div class="space-y-4">
                    <div class="flex items-center justify-between p-3 bg-slate-50 rounded-xl border border-slate-100">
                        <div>
                            <p class="text-sm font-bold text-slate-700">Hesap Aktif</p>
                            <p class="text-xs text-slate-500 text-pretty">Kullanıcı sisteme giriş yapabilir mi?</p>
                        </div>
                        <input type="checkbox" bind:checked={form.is_active} class="w-10 h-5 rounded-full text-emerald-500 focus:ring-emerald-500 border-slate-300 transition-all cursor-pointer" />
                    </div>

                    <div class="flex items-center justify-between p-3 bg-slate-50 rounded-xl border border-slate-100">
                        <div>
                            <p class="text-sm font-bold text-slate-700">Randevu Alınabilir</p>
                            <p class="text-xs text-slate-500">Bu personelden online randevu alınsın mı?</p>
                        </div>
                        <input type="checkbox" bind:checked={form.is_bookable} class="w-10 h-5 rounded-full text-blue-500 focus:ring-blue-500 border-slate-300 transition-all cursor-pointer" />
                    </div>
                </div>
            </div>

            <div class="px-6 py-4 bg-slate-50 border-t border-slate-100 flex justify-end space-x-3">
                <button onclick={onClose} class="px-4 py-2 text-sm font-medium text-slate-600 hover:text-slate-800">İptal</button>
                <button onclick={handleSave} class="px-6 py-2 bg-emerald-600 text-white rounded-lg text-sm font-bold shadow-lg shadow-emerald-200 hover:bg-emerald-700 transition-all">
                    Değişiklikleri Kaydet
                </button>
            </div>
        </div>
    </div>
{/if}
