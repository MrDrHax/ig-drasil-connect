import { getApiPath, addTokenToHeader, getNameFromToken } from "@/configs/api-tools";

/**
 * Retrieves a list of agents from the API.
 *
 * @param {number} skip - The number of agents to skip. Defaults to 0.
 * @param {number} limit - The maximum number of agents to retrieve. Defaults to 10.
 * @param {string|null} search - The search query to filter agents. Defaults to null.
 * @param {string|null} sortbydat - The field to sort the agents by. Defaults to null.
 * @param {string|null} sortby - The order to sort the agents in. Defaults to null.
 * @return {Promise<Object>} A promise that resolves to the JSON response containing the list of agents.
 * @throws {Error} If the API request fails.
 */
export async function AgentList(skip = 0, limit = 10, search = null, sortbydat = null, sortby = null) {
    let url = new URL(getApiPath() + 'lists/agents');

    console.log("seatch: " + search);

    let params = {
        skip: skip,
        limit: limit,
        sortByDat: sortbydat,
        sortBy: sortby,
        q: search
    };

    Object.keys(params).forEach(key => url.searchParams.append(key, params[key]));

    let request = new Request(url);

    // add token to header
    addTokenToHeader(request);

    // call the api
    let response = await fetch(request);

    if (!response.ok) {
        // raise error
        throw new Error(`HTTP error! status: ${response.status}, details ${response.statusText}`);
    }

    return await response.json();
}

/**
 * Retrieves detailed information about a specific agent.
 *
 * @param {number} id - The unique identifier of the agent.
 * @return {Promise<Object>} A promise that resolves to the JSON response containing the agent details.
 */
export async function AgentDetails(id) {
    let url = getApiPath() + `dashboard/agent-profile?id=${id}`;

    let request = new Request(url);

    addTokenToHeader(request);

    let response = await fetch(request);

    if (!response.ok) {
        // raise error
        throw new Error(`HTTP error! status: ${response.status}, details ${response.statusText}`);
    }

    return await response.json();

    /*
    return {
        avatar: "/img/team-2.jpeg",
        name: "John Doe",
        queue: "Support",
        status: "on-call",
        id: id
    }
    */
}

/**
 * Retrieves the agent ID associated with the current user's token.
 *
 * @return {Promise<Object>} A promise that resolves to the JSON response containing the agent ID.
 * @throws {Error} If the API request fails.
 */
export async function AgentId() {
    let url = getApiPath() + `extras/agentID?username=${getNameFromToken()}`;

    let request = new Request(url);

    addTokenToHeader(request);

    let response = await fetch(request);

    if (!response.ok) {
        // raise error
        throw new Error(`HTTP error! status: ${response.status}, details ${response.statusText}`);
    }

    return await response.json();
}

export async function JoinCall(agent_id) {

    let url = getApiPath() + `MongoAtlas/join_call?agent_id=${agent_id}}`;
    let request = new Request(url, {method: 'POST'});
    addTokenToHeader(request);
    let response = await fetch(request);
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}, details ${response.statusText}`);
    }
    return await response.json();

}

export function AgentsSummary() {
    console.warn("AgentsSummary function is not implemented!!!");

    return {
        agentCount: 10,
        table: {
            connected: 5,
            disconnected: 3,
            onCall: 2
        },
        usageLevel: 40,
    }
}

export default AgentList;