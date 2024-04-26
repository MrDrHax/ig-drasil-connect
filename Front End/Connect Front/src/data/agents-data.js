import { getApiPath } from "@/configs/api-tools";

export async function AgentList(skip = 0, limit = 10, search = null, sortbydat = null, sortby = null) {
    let url = getApiPath() + `lists/agents?skip=${skip}&limit=${limit}&sortByDat=${sortbydat}&sortBy=${sortby}`;

    if (search) {
        url += `&q=${search}`;
    }

    // call the api
    let response = await fetch(url);

    if (!response.ok) {
        // raise error
        throw new Error(`HTTP error! status: ${response.status}, details ${response.statusText}`);
    }

    return await response.json();
}

export function AgentDetails(id) {
    console.warn("AgentDetails function is not implemented!!!");

    return {
        avatar: "/img/team-2.jpeg",
        name: "John Doe",
        queue: "Support",
        status: "on-call",
        id: 3
    }
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