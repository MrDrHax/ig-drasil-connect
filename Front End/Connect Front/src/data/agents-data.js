export function AgentList(page = 1, limit = 10) {
    //   return fetch(`https://jsonplaceholder.typicode.com/users?_page=${page}&_limit=${limit}`)
    //     .then((res) => res.json())
    //     .then((data) => data);
    console.warn("AgentList function is not implemented!!!");

    return [
        {
            avatar: "/img/team-2.jpeg",
            name: "John Doe",
            queue: "Support",
            status: "connected",
            requireHelp: false,
            id: 1
        },
        {
            avatar: "/img/team-2.jpeg",
            name: "Alex",
            queue: "Support",
            status: "disconnected",
            requireHelp: false,
            id: 2
        },
        {
            avatar: "/img/team-2.jpeg",
            name: "Robbert",
            queue: "Tickets",
            status: "on-call",
            requireHelp: true,
            id: 3
        },
        {
            avatar: "/img/team-2.jpeg",
            name: "Alex",
            queue: "Tickets",
            status: "busy",
            requireHelp: true,
            id: 4
        },
        {
            avatar: "/img/team-2.jpeg",
            name: "Alex",
            queue: "Refunds",
            status: "on-break",
            requireHelp: true,
            id: 5
        }
    ]
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