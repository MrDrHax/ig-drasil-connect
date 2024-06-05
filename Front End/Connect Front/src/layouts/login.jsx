import { useLocation } from 'react-router-dom';

import { getApiToken, storeToken } from '@/configs'

function useQuery() {
    return new URLSearchParams(useLocation().search);
}


export function Login() {
    let query = useQuery();
    let code = query.get("code");

    // Saving the tokens in local storage
    getApiToken(code)
        .then(data => {            
            storeToken(data)
                .then(() => 
                     window.location.href = sessionStorage.getItem('Supervisor') === 'true' ? '/dashboard/home' : '/dashboard/agent')
                .catch(error => console.error('Error:', error));
        })
        .catch(error => console.error('Error:', error));

    return (
        <div className="flex justify-center items-center min-h-screen">
            <tr key="loading">
                <td className="py-3 px-5 border-b border-blue-gray-50 text-center" colSpan="5">
                    <span className="flex justify-center items-center min-h-screen ">
                    <span className="animate-spin rounded-full h-32 w-32 border-t-2 border-b-2 border-gray-800">
                    </span>
                    </span>
                </td>
            </tr>
        </div>
    )
}