import { getApiPath, addTokenToHeader } from "@/configs/api-tools";

export async function QueueList(skip = 0, limit = 10, search = null, sortbydat = null, sortby = null) {
  let url = getApiPath() + `lists/queues?skip=${skip}&limit=${limit}&sortByDat=${sortbydat}&sortBy=${sortby}`;

  // fill in the query
  let query = ""

  if (search) {
      query += search;
  }

  if (query) {
      url += `&q=${query}`;
  }

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

export async function ChangeRoutingProfile(agentID, routingProfileName) {
  let url = getApiPath() + `actions/change_routing_profile?agent_id=${agentID}&routing_profile_name=${routingProfileName}`;

  let request = new Request(url, {method: 'POST'});
  addTokenToHeader(request);
  let response = await fetch(request);
  if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}, details ${response.statusText}`);
  }
  return await response.json();
}