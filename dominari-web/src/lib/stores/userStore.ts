// dominari-web/src/lib/stores/userStore.ts
import { writable } from 'svelte/store';

interface User {
    id: string;
    name: string;
    phone: string;
}

interface Office {
    id: string;
    name: string;
    role: string;
    is_staff: boolean;
}

interface Session {
    isLoggedIn: boolean;
    isChecking: boolean;
    token: string | null;
    user: User | null;
    activeOffice: Office | null;
    staffOffices: Office[];
    clientOffices: Office[];
}

// 1. Ana Veri Yapısı (Kutu)
export const userSession = writable<Session>({
    isLoggedIn: false,
    isChecking: true, // Başlangıçta kontrol ediliyor diyoruz
    token: null,
    user: null,         // {id, name, phone}
    activeOffice: null, // Şu an işlem yapılan ofis {id, name, role, is_staff}
    staffOffices: [],   // Yönetici/Personel olduğu ofisler
    clientOffices: []   // Sadece hizmet aldığı ofisler
});

// 2. Login Fonksiyonu (Dışarıdan çağrılacak)
export async function login(phone: string, password: string) {
    try {
        const response = await fetch('/api/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ phone, password })
        });

        console.log("Response statüsü:", response.status);

        const data = await response.json();

        if (response.ok) {
            // Gelen veriyi staff ve client olarak ayırıp store'a yazıyoruz
            userSession.set({
                isLoggedIn: true,
                isChecking: false,
                token: data.token,
                user: data.user,
                activeOffice: null, // Henüz ofis seçilmedi
                staffOffices: data.offices.filter(o => o.is_staff === true),
                clientOffices: data.offices.filter(o => o.is_staff === false)
            });
            // Token'ı sayfayı yenileyince kaybolmasın diye tarayıcıya atıyoruz
            localStorage.setItem('token', data.token);
            return { success: true };
        } else {
            return { success: false, message: data.detail || 'Giriş başarısız' };
        }
    } catch (err) {
        return { success: false, message: 'Sunucuya bağlanılamadı' };
    }
}

// 3. Ofis Seçme Fonksiyonu
export const setActiveOffice = (officeId: number) => {
    userSession.update(session => {
        // Hem staff hem client listesinde ara
        const allOffices = [...session.staffOffices, ...session.clientOffices];
        const office = allOffices.find(o => o.id.toString() === officeId.toString());
        return { ...session, activeOffice: office || null };
    });
};

// 4. Logout Fonksiyonu
export const logout = () => {
    userSession.set({
        isLoggedIn: false,
        isChecking: false,
        token: null,
        user: null,
        activeOffice: null,
        staffOffices: [],
        clientOffices: []
    });
    localStorage.removeItem('token');
};