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

export const agentQueue = [
    {
      name: "Ticket Sales",
      ongoingCalls: 126,
      online: true,
      avg: 4.26,
      usage: 55,
    },
    {
      name: "Ticket Delivery",
      ongoingCalls: 45,
      avg: 0.34,
      online: false,
      usage: 27,
    },
    {
      name: "My Tickets Profile",
      ongoingCalls: 198,
      avg: 2.47,
      online: true,
      usage: 101,
    },
    {
      name: "Reinbursements",
      ongoingCalls: 455,
      avg: 6.98,
      online: true,
      usage: 89,
    },
    {
      name: "Ticket Transfers",
      ongoingCalls: 10,
      avg: 1.22,
      online: false,
      usage: 100,
    },
    
  ];
  
  export default agentQueue;
  