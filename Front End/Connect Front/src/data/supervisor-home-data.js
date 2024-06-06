import { getApiPath, addTokenToHeader } from "@/configs/api-tools";

/**
 * Retrieves supervisor home data from the API.
 *
 * @return {Promise} A Promise that resolves with the JSON response from the API.
 */
export async function SupervisorHomeData() {
  let url = getApiPath() + `dashboard/cards`;
  let request = new Request(url);
  addTokenToHeader(request);
  let response = await fetch(request);
  if (!response.ok) {
    // raise error
    throw new Error(`HTTP error! status: ${response.status}, details ${response.statusText}`);
  }

  // This returns a JSON object that needs to be separated into the cards and graphs
  return await response.json();
}

/**
 * Retrieves agent home data from the API for a specific agent.
 *
 * @param {string} agent_id - The ID of the agent.
 * @return {Promise<Object>} A promise that resolves to the agent home data as a JSON object.
 * @throws {Error} If the API request fails.
 */
export async function AgentHomeData(agent_id) {
  let url = getApiPath() + `dashboard/agent_cards?agent_id=` + agent_id;
  let request = new Request(url);
  addTokenToHeader(request);
  let response = await fetch(request);
  if (!response.ok) {
    // raise error
    throw new Error(`HTTP error! status: ${response.status}, details ${response.statusText}`);
  }

  // This returns a JSON object that needs to be separated into the cards and graphs
  return await response.json();
}

/**
 * Retrieves agent rating data from the API for a specific agent.
 *
 * @param {string} agent_id - The ID of the agent.
 * @return {Promise<Object>} A promise that resolves to the agent rating data as a JSON object.
 * @throws {Error} If the API request fails.
 */
export async function AgentRatingGraphData(agent_id) {
  let url = getApiPath() + `summaries/AgentRatingGraph?agent_id=` + agent_id;
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
 * Retrieves agent rating data from the API for a specific agent.
 *
 * @param {string} agent_id - The ID of the agent.
 * @return {Promise<Object>} A promise that resolves to the agent rating data as a JSON object.
 * @throws {Error} If the API request fails.
 */
export async function AgentRatingData(agent_id) {
  let url = getApiPath() + `summaries/AgentRatingAvg?agent_id=` + agent_id;
  let request = new Request(url);
  addTokenToHeader(request);
  let response = await fetch(request);
  if (!response.ok) {
    // raise error
    throw new Error(`HTTP error! status: ${response.status}, details ${response.statusText}`);
  }

  return await response.json();
}

export async function Alerts(){
  let url = getApiPath() + `dashboard/alerts/get_alerts_supervisor`;
  let request = new Request(url);
  addTokenToHeader(request);
  let response = await fetch(request);
  if (!response.ok) {
    // raise error
    throw new Error(`HTTP error! status: ${response.status}, details ${response.statusText}`);
  }

  return await response.json();

/**
 * Retrieves the last up to 5 conversations from the API for a specific agent.
 *
 * @param {string} agent_id - The ID of the agent.
 * @return {Promise<Object>} A promise that resolves to the agent recommendation data as a JSON object.
 * @throws {Error} If the API request fails.
 */
export async function AgentConversations(agent_id) {
  let url = getApiPath() + `summaries/AgentContactsProfile?agent_id=` + agent_id;
  let request = new Request(url);
  addTokenToHeader(request);
  let response = await fetch(request);
  if (!response.ok) {
    // raise error
    throw new Error(`HTTP error! status: ${response.status}, details ${response.statusText}`);
  }

  return await response.json();
}