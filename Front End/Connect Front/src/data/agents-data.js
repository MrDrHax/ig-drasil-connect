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

    // console.log("search: " + search);

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
 * Retrieves a list of statuses from the API.
 *
 * @return {Promise<Object>} A promise that resolves to the JSON response containing the list of statuses.
 * @throws {Error} If the API request fails.
 */
export async function StatusList() {
    let url = getApiPath() + 'lists/statuses';
    let request = new Request(url);
    addTokenToHeader(request);
    let response = await fetch(request);
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}, details ${response.statusText}`);
    }
    return await response.json();
}

/**
 * Retrieves a list of cards from the API.
 *
 * @return {Promise<Object>} A promise that resolves to the JSON response containing the list of agents.
 * @throws {Error} If the API request fails.
 */
export async function AgentCards() {
    let url = getApiPath() + 'agents/cards';
    let request = new Request(url);
    addTokenToHeader(request);
    let response = await fetch(request);
    if (!response.ok) {
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

/**
 * Joins a phone call in Amazon Connect for the specified agent.
 *
 * @param {string} agent_id - The ID of the agent whose call to join.
 * @return {Promise<Object>} A promise that resolves to the JSON response containing the confirmation message of the call joining.
 * @throws {Error} If the API request fails.
 */
export async function JoinCall(agent_id) {

    let url = getApiPath() + `actions/join-call?agent_id=${agent_id}`;
    let request = new Request(url, {method: 'POST'});
    addTokenToHeader(request);
    let response = await fetch(request);
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}, details ${response.statusText}`);
    }
    return await response.json();

}

export async function AgentSentimentRatingData(agent_id) {
    let url = getApiPath() + `summaries/AgentSentimentRating?agent_id=` + agent_id;
    let request = new Request(url);
    addTokenToHeader(request);
    let response = await fetch(request);
    if (!response.ok) {
      // raise error
      throw new Error(`HTTP error! status: ${response.status}, details ${response.statusText}`);
    }
  
    return await response.json();
  }

  export async function getAgentTranscriptSummaryData(agent_id) {
    let url = getApiPath() + `summaries/AgentTranscriptSummary?agent_id=` + agent_id;
    let request = new Request(url);
    addTokenToHeader(request);
    let response = await fetch(request);
    if (!response.ok) {
      // raise error
      throw new Error(`HTTP error! status: ${response.status}, details ${response.statusText}`);
    }
  
    return await response.json();
  }

/**
 * Changes the status of an agent.
 * 
 * @param {string} agent_id - The ID of the agent whose status to change.
 * @param {string} status - The new status of the agent.
 * @return {Promise<Object>} A promise that resolves to the JSON response containing the confirmation message of the status change.
 * @throws {Error} If the API request fails.
 */
export async function ChangeStatus(agent_id, status) {
    let url = getApiPath() + `actions/change_status?agent_id=${agent_id}&status=${status}`;
    let request = new Request(url, {method: 'POST'});
    addTokenToHeader(request);
    let response = await fetch(request);
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}, details ${response.statusText}`);
    }
    return await response.json();
}

export async function AgentSummary(agent_id) {
    let url = getApiPath() + `summaries/AI/AgentPerformance?agent_id=${agent_id}`;
    let request = new Request(url);
    addTokenToHeader(request);
    let response = await fetch(request, {method: 'GET'});
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}, details ${response.statusText}`);
    }
    return await response.json();
}