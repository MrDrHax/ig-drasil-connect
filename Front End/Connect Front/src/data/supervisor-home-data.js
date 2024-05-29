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