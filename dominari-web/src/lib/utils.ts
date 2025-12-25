export function phoneDisplay(phone:string): string {
    if (!phone) return "";

    // Sadece rakamları temizleyip alalım
    const clean = phone.toString().replace(/\D/g, "");

    // Türkiye formatı: 90 533 271 97 97 (12 hane)
    if (clean.length === 12) {
        return `+${clean.slice(0, 2)} ${clean.slice(2, 5)} ${clean.slice(5, 8)} ${clean.slice(8, 10)} ${clean.slice(10, 12)}`;
    }

    // Eğer numara 10 hane ise (başında 90 yoksa) başına +90 ekleyerek formatla
    if (clean.length === 10) {
        return `+90 ${clean.slice(0, 3)} ${clean.slice(3, 6)} ${clean.slice(6, 8)} ${clean.slice(8, 10)}`;
    }

    // Beklenen uzunlukta değilse ham halini döndür
    return phone;
}