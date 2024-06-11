import { v4 as uuidv4 } from 'uuid';

export function getApiPath() {

    if (import.meta.env.PROD)
        return "https://connect.igdrasilteam.com/api/";
    else
        return "http://localhost:8080/";
}

export function validateToken() {
    let token = sessionStorage.getItem('token');
    let access_token = sessionStorage.getItem('access_token');
    let refresh = sessionStorage.getItem('refresh');

    if (token === null || access_token === null || refresh === null) {
        console.log("No token");
        return true;
    }

    // TODO refresh token if needed, and return true if worked

    // let response = await fetch(getApiPath() + "extras/IAM/validate", {
    //     method: 'GET',
    //     headers: {
    //         'Authorization': 'Bearer ' + token,
    //         'Access-Token': access_token,
    //         'Refresh-Token': refresh
    //     }
    // });

    // if (!response.ok) {
    //     return false;
    // }

    return false;
}

/**
 * A function that extracts the preferred username from a JWT token stored in session storage.
 *
 * @return {string} The preferred username extracted from the JWT token.
 */
export function getNameFromToken() {
    let access_token = sessionStorage.getItem('access_token');

    // return jwt data
    let data = access_token.split('.')[1];
    data = JSON.parse(atob(data));

    //console.log(typeof(data.preferred_username));

    return data.preferred_username;
}

/**
 * A function that retrieves the roles from a JWT token stored in session storage.
 *
 * @return {array} The roles extracted from the JWT token.
 */
export function getRolesFromToken() {
    let access_token = sessionStorage.getItem('access_token');

    // return jwt data
    let data = access_token.split('.')[1];
    data = JSON.parse(atob(data));

    return data.realm_access.roles;
}

export const parsePaginationString = (paginationString) => {
    const [range, totalItems] = paginationString.split('/');
    const [start, end] = range.split('-');

    const itemsPerPage = end - start + 1;
    const currentPage = Math.ceil(start / itemsPerPage);

    return {
        currentPage,
        itemsPerPage,
        totalItems: parseInt(totalItems),
    };
};

export function addTokenToHeader(request) {
    // TODO check what token is the neccesary one

    // let token = sessionStorage.getItem('token');
    let access_token = sessionStorage.getItem('access_token');
    // let refresh = sessionStorage.getItem('refresh');

    // request.headers.set('Authorization', 'Bearer ' + token);
    request.headers.set('Authorization', 'Bearer ' + access_token);
    // request.headers.set('Refresh-Token', refresh);

    return request;
}

export function isSupervisor() {
    try{
        let roles = getRolesFromToken();

        console.warn(roles);
        for (let i = 0; i < roles.length; i++) {
            if (roles[i] === "manager") {
                return true;
            }
        }

        return false;
    }
    catch{
        return true
    }
}

export async function storeToken(data) {
    let token = data.id_token;
    let access_token = data.access_token;
    let refresh = data.refresh;

    // store the token in local storage
    sessionStorage.setItem('token', token);
    sessionStorage.setItem('access_token', access_token);
    sessionStorage.setItem('refresh', refresh);

    // check if it's a supervisor
    sessionStorage.setItem('Supervisor', isSupervisor());
}

export async function getApiToken(code) {
    const redirectUrl = `${window.location.protocol}//${window.location.host}/login`;
    let initialCall = getApiPath() + "extras/IAM/callback?code=" + code + "&redirect_uri=" + redirectUrl;

    // call the API to get the login page

    let response = await fetch(initialCall);

    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }

    let data = await response.json();

    return data;
}

export async function getApiLoginPage() {
    const redirectUrl = `${window.location.protocol}//${window.location.host}/login`;
    let initialCall = getApiPath() + "extras/login?redirect=" + redirectUrl;

    // call the API to get the login page

    let response = await fetch(initialCall);

    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }

    let data = await response.json();

    return data;
}

export default getApiPath;