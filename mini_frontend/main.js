
document.addEventListener('DOMContentLoaded', () => {
    const API_URL = 'http://127.0.0.1:8001/api'; // твой бекенд

// Функция для сброса пароля
    async function resetPassword(uid, token, newPassword) {
        const response = await fetch(`${API_URL}/reset-password/`, {
            method: "PATCH",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                uid: uid,
                token: token,
                new_password: newPassword
            })
        });

        return response.json();
    }

// Функция для запроса сброса пароля (forgot password)
    async function forgotPassword(email) {
        const response = await fetch(`${API_URL}/forgot-password/`, {
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                email: email
            })
        });

        return response.json();
    }

// Если страница reset-password
    if (window.location.pathname.startsWith('/reset-password')) {
        const form = document.getElementById('reset-form');
        const status = document.getElementById('status');

        form.addEventListener('submit', async (e) => {
            e.preventDefault();

            const urlParts = window.location.pathname.split('/');
            const uid = urlParts[2];
            const token = urlParts[3];
            const newPassword = document.getElementById('new-password').value;

            try {
                const result = await resetPassword(uid, token, newPassword);
                status.textContent = result.message || 'Password reset successful!';
            } catch (error) {
                status.textContent = 'Error resetting password.';
            }
        });
    }

// Если страница forgot-password
    if (window.location.pathname.startsWith('/forgot-password')) {
        const form = document.getElementById('forgot-form');
        const status = document.getElementById('status');

        form.addEventListener('submit', async (e) => {
            e.preventDefault();

            const email = document.getElementById('email').value;

            try {
                const result = await forgotPassword(email);
                status.textContent = result.message || 'If your email exists, reset link was sent.';
            } catch (error) {
                status.textContent = 'Error sending reset link.';
            }
        });
    }
});
