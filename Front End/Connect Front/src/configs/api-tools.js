import { v4 as uuidv4 } from 'uuid';

export function getApiPath() {
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

export function getNameFromToken() {
    let access_token = sessionStorage.getItem('access_token');

    // return jwt data
    let data = access_token.split('.')[1];
    data = JSON.parse(atob(data));

    console.log(typeof(data.preferred_username));

    return data.preferred_username;
}

export async function storeToken(data) {
    let token = data.id_token;
    let access_token = data.access_token;
    let refresh = data.refresh;

    // store the token in local storage
    sessionStorage.setItem('token', token);
    sessionStorage.setItem('access_token', access_token);
    sessionStorage.setItem('refresh', refresh);
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