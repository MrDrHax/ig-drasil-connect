import { useLocation } from 'react-router-dom';

import { getApiToken, storeToken } from '@/configs'

function useQuery() {
    return new URLSearchParams(useLocation().search);
}

export function Login() {
    let query = useQuery();
    let code = query.get("code");

    getApiToken(code)
        .then(data => {
            storeToken(data)
                .then(() => window.location.href = '/dashboard/home')
                .catch(error => console.error('Error:', error));
        })
        .catch(error => console.error('Error:', error));

    return (
        <div>
            <h1>Making login</h1>
        </div>
    )
}