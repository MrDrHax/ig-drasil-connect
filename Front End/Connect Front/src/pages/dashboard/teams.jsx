import {
    Card,
    CardHeader,
    CardBody,
    Typography,
    Input,
    Avatar,
    Chip,
    Tooltip,
    Progress,
} from "@material-tailwind/react";
// import { EllipsisVerticalIcon } from "@heroicons/react/24/outline";
// import { authorsTableData, projectsTableData } from "@/data";
import { AgentList, AgentsSummary } from "@/data/agents-data";
import { StatisticsCard } from "@/widgets/cards";
import { StatisticsChart } from "@/widgets/charts";
import { UsersIcon, CogIcon, CheckCircleIcon, ExclamationCircleIcon, ChevronLeftIcon, ChevronRightIcon } from "@heroicons/react/24/solid";
import { parsePaginationString } from "@/configs/api-tools";
import { chartsConfig } from "@/configs";
import React, { useEffect, useState } from 'react';
import { getBgColor, getBorderColor, getTextColor, useMaterialTailwindController } from "@/context";

function getColorOfStatus(status) {
    switch (status) {
        case "connected":
            return "green";
        case "disconnected":
            return "gray";
        case "on-call":
            return "blue";
        case "busy":
            return "orange";
        case "on-break":
            return "red";
        default:
            return "gray";
    }
}


export function Teams() {
    const [controller, dispatch] = useMaterialTailwindController();
    const { navColor, fixedNavbar, openSidenav, theme } = controller;

    const [dataToDisplay, setData] = useState([]);
    const [isLoaded, setIsLoaded] = useState(false);
    const [searchQuery, setSearchQuery] = useState('');

    // pagination vars
    const [pagination_currentPage, pagination_setCurrentPage] = useState(0);
    const [pagination_totalPages, pagination_setTotalPages] = useState(0);
    const [pagination_itemsPerPage, pagination_setItemsPerPage] = useState(0);
    const [pagination_totalItems, pagination_setTotalItems] = useState(0);

    // let isLoaded = false;
    // let dataToDisplay = searchQuery ? filteredAgents : data;

    function handleSearch(event) {
        let query = event.target.value.toLowerCase();
        setSearchQuery(query);
        // let filtered = data.filter(agent => agent.name.toLowerCase().includes(query));
        // setFilteredAgents(filtered);
    }

    function updateData(page = 1) {
        let query = searchQuery ? "name=" + searchQuery : null;
        let skip = (page - 1) * 10;

        AgentList(skip, 10, query, "name", "asc").then((data) => {
            const { currentPage, itemsPerPage, totalItems } = parsePaginationString(data.pagination);
            const totalPages = Math.ceil(totalItems / itemsPerPage);

            pagination_setCurrentPage(currentPage);
            pagination_setItemsPerPage(itemsPerPage);
            pagination_setTotalItems(totalItems);

            pagination_setTotalPages(totalPages);

            setData(data.data);
            setIsLoaded(true);
        }).catch((error) => {
            console.error("Error while fetching data from agents", error);
        });
    }

    useEffect(() => {
        updateData();
    }, [searchQuery]);

    // var theThingToDo = {
    //     type: "pie",
    //     height: 220,
    //     series: [
    //         {
    //             name: "Views",
    //             data: [50, 20, 10, 22, 50, 10, 40],
    //         },
    //     ],
    //     options: {
    //         ...chartsConfig,
    //         colors: "#388e3c",
    //         plotOptions: {
    //             bar: {
    //                 columnWidth: "16%",
    //                 borderRadius: 5,
    //             },
    //         },
    //         xaxis: {
    //             ...chartsConfig.xaxis,
    //             categories: ["M", "T", "W", "T", "F", "S", "S"],
    //         },
    //     },
    // };

    return (
        <div>


            <div className="mb-12 grid gap-y-10 gap-x-6 md:grid-cols-2 xl:grid-cols-4">
                <StatisticsCard
                    key="Connected"
                    title="Connected users"
                    color="gray"
                    // icon={React.createElement(UsersIcon, {
                    //     className: "w-6 h-6 text-white",
                    // })}
                    value="10"
                    icon={<UsersIcon className="h-6 w-6 text-white-500" />}
                    footer={
                        <Typography className="font-normal text-blue-gray-600">
                            <strong className="text-green-500">10</strong>
                            &nbsp; connected
                        </Typography>
                    }
                />
                <StatisticsCard
                    key="Stress"
                    title="Usage level"
                    color="gray"
                    // icon={React.createElement(UsersIcon, {
                    //     className: "w-6 h-6 text-white",
                    // })}
                    value="30%"
                    icon={<CogIcon className="h-6 w-6 text-white-500" />}
                    footer={
                        <Typography className="font-normal text-blue-gray-600">
                            <strong className="text-green-500">3/5</strong>
                            &nbsp; agents on call
                        </Typography>
                    }
                />
            </div>
            <div className="mt-12 mb-8 flex flex-col gap-12">
                <Card className={`${getBgColor("background-cards")}`}>
                    <CardHeader variant="gradient" color="gray" className={`mb-8 p-6 flex ${getBgColor("search-bar")}`}>
                        <Typography variant="h6" color="white" className="flex-none">
                            Agents
                        </Typography>

                        <div className="flex-grow"></div>

                        <div className="mr-auto md:mr-4 md:w-56">
                            {/* Search bar */}
                            <Input
                                color="white"
                                label="Search by name"
                                value={searchQuery}
                                onChange={handleSearch}
                            />
                        </div>
                    </CardHeader>
                    <CardBody className="overflow-x-scroll px-0 pt-0 pb-2">
                        {/* List */}
                        <table className="w-full min-w-[640px] table-auto">
                            <thead>
                                <tr>
                                    {["name", "queue", "status", "needs help", ""].map((el, i) => (
                                        <th
                                            key={i}
                                            className="border-b border-blue-gray-50 py-3 px-5 text-left"
                                        >
                                            <Typography
                                                variant="small"
                                                className="text-[11px] font-bold uppercase text-blue-gray-400"
                                            >
                                                {el}
                                            </Typography>
                                        </th>
                                    ))}
                                </tr>
                            </thead>
                            <tbody>
                                {!isLoaded ?
                                    (
                                        <tr key="loading">
                                            <td className="py-3 px-5 border-b border-blue-gray-50 text-center" colSpan="5">
                                                <span className="flex justify-center items-center">
                                                    <span className={"animate-spin rounded-full h-32 w-32 border-t-2 border-b-2 " + getBorderColor(navColor)}></span>
                                                </span>
                                            </td>
                                        </tr>
                                    ) : (
                                        dataToDisplay.length === 0 ? (
                                            <tr key="empty">
                                                <td className="py-3 px-5 border-b border-blue-gray-50 text-center" colSpan="5">
                                                    <Typography
                                                        variant="small"
                                                        className="text-[1em] font-semibold text-blue-gray-600"
                                                    >
                                                        List is empty
                                                    </Typography>
                                                </td>
                                            </tr>
                                        ) : (
                                            dataToDisplay.map(
                                                ({ name, queue, status, requireHelp, agentID }, key) => {
                                                    const className = `py-3 px-5 ${key === dataToDisplay.length - 1
                                                        ? ""
                                                        : "border-b border-blue-gray-50"
                                                        }`;

                                                    return (
                                                        <tr key={agentID}>
                                                            <td className={className}>
                                                                <div className="flex items-center gap-4">
                                                                    {/* <Avatar src={avatar} alt={name} size="sm" variant="rounded" /> */}
                                                                    <div>
                                                                        <Typography
                                                                            variant="small"
                                                                            color="blue-gray"
                                                                            className="font-semibold"
                                                                        >
                                                                            {name}
                                                                        </Typography>
                                                                    </div>
                                                                </div>
                                                            </td>
                                                            <td className={className}>
                                                                <Typography className="text-xs font-semibold text-blue-gray-600">
                                                                    {queue}
                                                                </Typography>
                                                            </td>
                                                            <td className={className}>
                                                                <Chip
                                                                    variant="gradient"
                                                                    color={getColorOfStatus(status)}
                                                                    value={status}
                                                                    className="py-0.5 px-2 text-[11px] font-medium w-fit"
                                                                />
                                                            </td>
                                                            <td className={className}>
                                                                {requireHelp ? <ExclamationCircleIcon className="h-6 w-6 text-red-500" /> : <CheckCircleIcon className="h-6 w-6 text-green-500" />}
                                                            </td>
                                                            <td className={className}>
                                                                <Typography
                                                                    as="a"
                                                                    href="#"
                                                                    className="text-xs font-semibold text-blue-gray-600"
                                                                >
                                                                    View
                                                                </Typography>
                                                            </td>
                                                        </tr>
                                                    );
                                                }
                                            )
                                        )
                                    )
                                }
                            </tbody>
                        </table>
                        {/* Pagination */}
                        <div>
                            <div className={`flex items-center justify-between border-t border-gray-200 ${getBgColor("background-cards")} px-4 py-3 sm:px-6`}>
                                <div className="flex flex-1 justify-between sm:hidden">
                                    <a
                                        href="#"
                                        className="relative inline-flex items-center rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"
                                    >
                                        Previous
                                    </a>
                                    <a
                                        href="#"
                                        className="relative ml-3 inline-flex items-center rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"
                                    >
                                        Next
                                    </a>
                                </div>
                                <div className="hidden sm:flex sm:flex-1 sm:items-center sm:justify-between">
                                    <div>
                                        <p className={`text-sm ${getTextColor("gray")}`}>
                                            Showing <span className="font-medium">{(pagination_currentPage - 1) * pagination_itemsPerPage + 1}</span> to <span className="font-medium">{pagination_currentPage * pagination_itemsPerPage}</span> of{' '}
                                            <span className="font-medium">{pagination_totalItems}</span> results
                                        </p>
                                    </div>
                                    <div>
                                        <nav className="isolate inline-flex -space-x-px rounded-md shadow-sm" aria-label="Pagination">
                                            <a
                                                href="#"
                                                onClick={() => { !(pagination_currentPage - 1 === 0) ? updateData(pagination_currentPage - 1) : null }}
                                                className="relative inline-flex items-center rounded-l-md px-2 py-2 text-gray-400 ring-1 ring-inset ring-gray-300 hover:bg-gray-50 focus:z-20 focus:outline-offset-0"
                                            >
                                                <span className="sr-only">Previous</span>
                                                <ChevronLeftIcon className="h-5 w-5" aria-hidden="true" />
                                            </a>

                                            {([...Array(pagination_totalPages)].map((e, i) => {
                                                return (i + 1 == pagination_currentPage) ? (
                                                    <a
                                                        key={i}
                                                        href="#"
                                                        onClick={() => updateData(i + 1)}
                                                        aria-current="page"
                                                        className={`relative z-10 inline-flex items-center ${getBgColor(navColor)} px-4 py-2 text-sm font-semibold ${getTextColor("contrast")} focus:z-20 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600`}
                                                    >
                                                        {i + 1}
                                                    </a>
                                                ) : (
                                                    <a
                                                        key={i}
                                                        href="#"
                                                        onClick={() => updateData(i + 1)}
                                                        aria-current="page"
                                                        className={`relative z-10 inline-flex items-center px-4 py-2 text-sm font-semibold ${getTextColor("dark")} focus:z-20 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600`}
                                                    >
                                                        {i + 1}
                                                    </a>
                                                )
                                            }))}
                                            <a
                                                href="#"
                                                onClick={() => { !(pagination_currentPage === pagination_totalPages) ? updateData(pagination_currentPage + 1) : null }}
                                                className="relative inline-flex items-center rounded-r-md px-2 py-2 text-gray-400 ring-1 ring-inset ring-gray-300 hover:bg-gray-50 focus:z-20 focus:outline-offset-0"
                                            >
                                                <span className="sr-only">Next</span>
                                                <ChevronRightIcon className="h-5 w-5" aria-hidden="true" />
                                            </a>
                                        </nav>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </CardBody>
                </Card>
            </div>
        </div>
    );
}

export default Teams;
