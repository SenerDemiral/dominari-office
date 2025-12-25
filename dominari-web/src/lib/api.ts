const BASE_URL = 'https://api.dominari.cloud';

export async function apiRequest(endpoint: string, method = 'GET', data = null) {
    const token = localStorage.getItem('token'); // Veya store'dan al
    const headers = {
        'Content-Type': 'application/json',
        ...(token && { 'Authorization': `Bearer ${token}` })
    };

    const response = await fetch(`${BASE_URL}${endpoint}`, {
        method,
        headers,
        body: data ? JSON.stringify(data) : null
    });
    return await response.json();
}