import { getApiPath, addTokenToHeader } from "@/configs/api-tools";

/**
 * Retrieves chat data for a specific agent from the API.
 *
 * @param {string} agentId - The ID of the agent.
 * @return {Promise<Object>} A promise that resolves to the chat data as a JSON object.
 * @throws {Error} If the API request fails.
 */
export async function getChatData(agentId) {
let url = getApiPath() + `MongoAtlas/get_chat_by_id?agent_id=${agentId}`;
  let request = new Request(url);
  addTokenToHeader(request);
  let response = await fetch(request);
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}, details ${response.statusText}`);
  }

  // This returns a JSON object that has the values needed for the chat
  return await response.json();
}

export async function postMessageData(agentId, message, is_supervisor) {
    let url = getApiPath() + `MongoAtlas/post_chat?agent_id=${agentId}&message=${message}&supervisor=${is_supervisor}`;

    let request = new Request(url, {method: 'POST'});
    addTokenToHeader(request);
    let response = await fetch(request);
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}, details ${response.statusText}`);
    }

    if (is_supervisor) {
        let url2= getApiPath() + `dashboard/alerts/supervisor/message?agent_id=${agentId}`;
        new Request(url2, {method: 'POST'});
    }
    else{
        let url2= getApiPath() + `dashboard/alerts/agent/message`;
        new Request(url2, {method: 'POST'});
    }

    return await response.json();
}



export const messageData = [
    { 
        message: "Hi! I need more information...",
        rol: "agent",
        hour: "15:30",
    },

    {
        message: "Awesome work, can you...",
        rol: "supervisor",
        hour: "15:40",
    },
    {
        message: "About files I can...",
        rol: "agent",
        hour: "15:50",
    },
    {
        message: "Have a great afternoon...",
        rol: "supervisor",
        hour: "16:00",
    },
    {
        message: "Hi! I need more information...",
        rol: "agnt",
        hour: "16:00",
    }

 ]

 export default messageData;
