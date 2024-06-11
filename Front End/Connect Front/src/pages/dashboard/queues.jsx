import {
  Card,
  CardHeader,
  CardBody,
  Typography,
  Avatar,
  Chip,
  Tooltip,
  Progress,
  Button,
  Menu,
  MenuHandler,
  MenuList,
  MenuItem,
  Input,
} from "@material-tailwind/react";
import { AgentList, QueueList, ChangeRoutingProfile, QueueCards } from "@/data";
import { getBgColor, getTextColor, getBorderColor, useMaterialTailwindController, getTypography,getTypographybold } from "@/context";

import React, { useEffect, useState } from 'react';
import { useAlert } from "@/context/alerts";

import { StatisticsCard } from "@/widgets/cards";
import { StatisticsChart } from "@/widgets/charts";

// Pagination imports
import { parsePaginationString } from "@/configs/api-tools";
import { UsersIcon, CogIcon, CheckCircleIcon, ExclamationCircleIcon, ClockIcon, ChevronLeftIcon, ChevronRightIcon } from "@heroicons/react/24/solid";


export function Queues() {
  const [controller, dispatch] = useMaterialTailwindController();
  const { navColor } = controller;

  const [dataToDisplay, setData] = useState([]);
  const [cards, setCards] = useState([]);
  const [graphs, setGraphs] = useState([]);
  const [agents, setAgentList] = useState([]);

  const [isLoaded, setIsLoaded] = useState(false);
  const [filterStatus, setFilterStatus] = useState('');
  const [searchQuery, setSearchQuery] = useState('');

  const [desc_queue, setDesc_queue] = useState({});

  // pagination vars
  const [pagination_currentPage, pagination_setCurrentPage] = useState(0);
  const [pagination_totalPages, pagination_setTotalPages] = useState(0);
  const [pagination_itemsPerPage, pagination_setItemsPerPage] = useState(0);
  const [pagination_totalItems, pagination_setTotalItems] = useState(0);

  const { showAlertWithMessage } = useAlert();

  function handleSearchStatus(event) {
    setFilterStatus(event.target.value.toLowerCase());
  }

  /**
   * Moves the agent to the given routing profile.
   *
   * @param {string} agentID - The ID of the agent.
   * @param {string} agentName - The name of the agent.
   * @param {string} routingProfileName - The name of the routing profile.
   * @return {void} This function does not return anything.
   */
  function moveAgentToRoutingProfile(agentID, agentName, routingProfiles) {
    ChangeRoutingProfile(agentID, routingProfiles).then(result => {
      if (result && result.message == "Routing profile changed")
        showAlertWithMessage("green", `${agentName}'s routing profile changed to ${routingProfiles}`, 5000);
      else
        showAlertWithMessage("red", "Failed to change routing profile", 5000);
    });
  }

  /**
   * Returns a Menu element for the given agent name and queue ID with the possible routing profiles.
   *
   * @param {string} agentName - The name of the agent.
   * @param {array} queueList - The list of queues the agent is in.
   * @param {number} queueID - The ID of the queue.
   * @param {array} possibleRoutingProfiles - The list of possible routing profiles to move the agent to.
   * @return {JSX.Element} The Menu element.
   */
  function getOptions(agentName, agentID, queueList, queueID, possibleRoutingProfiles) {
    // Check if the agent is already in the queue
    if (!queueList.includes(queueID)) {
      return (
        // Show a menu with the possible routing profiles for each agent
        <Menu placement="left" allowHover offset={15}>
          <MenuHandler>
            <MenuItem>  
             {agentName}
            </MenuItem>
          </MenuHandler>
          <MenuList>
          {possibleRoutingProfiles.map((profile) => (
            <MenuItem
              key={profile}
              onClick={() => {
                moveAgentToRoutingProfile(agentID, agentName, profile);
              }}
            >
              {profile}
            </MenuItem>
          ))}
          </MenuList>
        </Menu>
      );
    }
    else {
      return (<></>)
    }
  }

  /**
   * Updates the description state for the given queue name.
   *
   * @param {string} queueName - The name of the queue.
   * @return {void} This function does not return anything.
   */
  function showDesc(queueName) {
    // Set the description to true for the queue that was clicked

    setDesc_queue({ ...desc_queue, [queueName]: !desc_queue[queueName] });
  }

  /*
   * Updates the data to be displayed in the table.
   *
   * @param {number} page - The page number to get data for.
   * @return {void} This function does not return anything.
   */
  function updateData(page = 1) {
    let query = searchQuery ? "name=" + searchQuery : null;
    if (filterStatus) {
      query = query ? `${query}&status=${filterStatus}` : `status=${filterStatus}`;
    }
    let skip = (page - 1) * 10;

    setIsLoaded(false);

    // Get the list of available agents
    AgentList(0, 50, "status=Available", "name", "asc").then((data) => {
        setAgentList(data.data);
    })

    // Get the list of cards
    QueueCards().then((data) => {
        setCards(data.cards);
        setGraphs(data.graphs);
    })

    // Get the list of queues
    QueueList(skip, 10, query, "name", "asc").then((data) => {
        const { currentPage, itemsPerPage, totalItems } = parsePaginationString(data.pagination);
        const totalPages = Math.ceil(totalItems / itemsPerPage);

        pagination_setCurrentPage(currentPage);
        pagination_setItemsPerPage(itemsPerPage);
        pagination_setTotalItems(totalItems);

        pagination_setTotalPages(totalPages);

        setData(data.data);
        setIsLoaded(true);
    }).catch((error) => {
        setIsLoaded(true);

        showAlertWithMessage("red", "" + error, 10000);

        console.error(error);
    });
}

useEffect(() => {
    updateData();
}, [filterStatus]);

  return (
    <div>
    {/*<!-- Cards -->
    <div className="mb-12 grid gap-y-10 gap-x-6 md:grid-cols-2 xl:grid-cols-4">
        {!isLoaded ? (
        <div className="py-3 px-5 border-b border-blue-gray-50 text-center col-span-full">
        <span className="flex justify-center items-center">
        <span className={`animate-spin rounded-full h-32 w-32 border-t-2 border-b-2 ${getBorderColor(navColor)}`}></span>
        </span>
        <Typography className={`text-base ${getTypography()}  ${getTextColor('dark')}`}>
            Cards are now loading...
        </Typography>
        </div>
        ) : (
        cards.map(({ icon, title, footer, ...rest }) => (
            <StatisticsCard
            key={title}
            {...rest}
            title={title}
            icon={React.createElement(getIcon(icon), {
                className: "w-6 h-6 text-white",
            })}
            footer={
                <Typography className={`text-base ${getTypography()}  ${getTextColor('dark')}`}>
                <strong className={footer.color}>{footer.value}</strong>
                &nbsp;{footer.label}
                </Typography>
            }
            />
        ))
        )}
      </div>
    */
    }

    {/*<!-- Table -->*/}
    <div className="mt-12 mb-8 flex flex-col gap-12">
      <Card className={`${getTypography()} ${getBgColor("background-cards")}`}>
        <CardHeader variant="gradient" color="gray" className={`mb-8 p-6 ${getTypography()} ${getBgColor("search-bar")} flex justify-between items-center`}>
          <Typography variant="h6" className={`text-[1.45rem] flex-none ${getTextColor("white3")} ${getTypographybold()}`}>
            Agent Queues
          </Typography>
          <div className="mr-auto md:mr-4 md:w-56">
            {/* Search bar by name*/}
            <Input
             color="white"
             label="Search by status"
             value={filterStatus}
             onChange={handleSearchStatus}
            />
          </div>

        </CardHeader>
        <CardBody className={`overflow-x-scroll px-0 pt-0 pb-2 ${getBgColor("background-cards")}`}>
          <table className={`w-full min-w-[640px] table-auto ${getTypography()} `}>
            <thead>
              <tr>
                {["Name", "Ongoing Calls", "Average Wait Time", "Usage", "Status"].map((el) => (
                  <th
                    key={el}
                    className="border-b border-blue-gray-50 py-3 px-5 text-left"
                  >
                    <Typography
                      variant="small"
                      className={`text-[0.68rem] ${getTypographybold()} uppercase ${getTextColor('black')}`}
                    >
                      {el}
                    </Typography>
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              { !isLoaded ?
                // Loading
                <tr key="loading">
                  <td className="py-3 px-5 border-b border-blue-gray-50 text-center" colSpan="5">
                      <span className="flex justify-center items-center">
                          <span className={`animate-spin rounded-full h-32 w-32 border-t-2 border-b-2 ${getBorderColor(navColor)}`}></span>
                      </span>
                      <Typography className={`text-base ${getTypography()}  ${getTextColor('dark')}`}>
                        Queues are now loading...
                    </Typography>
                  </td>
                </tr> 
                : dataToDisplay.length === 0 ?
                // No data
                <tr key="no-data">
                  <td className="py-3 px-5 border-b border-blue-gray-50 text-center" colSpan="5">
                    <Typography className={`text-base ${getTypography()}  ${getTextColor('dark')}`}>
                      No queues found
                    </Typography>
                  </td>
                </tr>
                : dataToDisplay.map(
                ({ queueID, name, description, usage, averageWaitTime, maxContacts, routingProfiles, status }, key) => {
                  const className = `py-3 px-5 ${key === dataToDisplay.length
                      ? ""
                      : "border-t border-blue-gray-50"
                    }`;

                  return (
                    <>
                      <tr key={name} >
                        {/* Name */}
                        <td key="Name" className={className} onClick={() => showDesc(name)}>
                          <div className="flex items-center gap-4">

                            <div>
                              <Typography
                                variant="small"
                                color="blue-gray"
                                className={`text-[0.8rem] ${getTypographybold()} ${getTextColor('black')}`}
                              >
                                {name}
                              </Typography>

                            </div>
                          </div>
                        </td>

                        {/* Ongoing Calls */}
                        <td key="Ongoing Calls" className={className} onClick={() => showDesc(name)}>
                          <Typography className={`text-[0.7rem] ${getTypography()} ${getTextColor('black')}`}>
                            {usage}
                          </Typography>
                          {/*<Typography className="text-xs font-normal text-blue-gray-500">
                              {ongoingCalls[1]}
                            </Typography>*/}
                        </td>

                        {/* Average Wait Time */}
                        <td key="Average Wait Time" className={className} onClick={() => showDesc(name)}>
                          <Typography
                            className={`text-[0.7rem] ${getTypography()} ${averageWaitTime <= 1 ? "text-green-600" : averageWaitTime <= 2.30 ? "text-orange-600" : "text-red-600"
                              }`}
                          >
                            {averageWaitTime}
                          </Typography>

                          {/*<Typography className="text-xs font-normal text-blue-gray-500">
                              {ongoingCalls[1]}
                            </Typography>*/}
                        </td>

                        {/* Usage */}
                        <td key="Usage" className={className} onClick={() => showDesc(name)}>
                          <div className="w-10/12">
                            <Typography
                              variant="small"
                              className={`mb-1 block text-[0.7rem] font-medium ${getTextColor('black')}`}
                            >
                              {usage / maxContacts * 100}%
                            </Typography>
                            <Progress
                              value={usage / maxContacts * 100}
                              variant="gradient"
                              color={status === "Free" ? "green" : status === "Stressed" ? "orange" : "red"}
                              className="h-1"
                            />
                          </div>
                        </td>

                        {/* Status */}
                        <td key="Status" className={className} onClick={() => showDesc(name)}>
                          <Chip
                            variant="gradient"
                            color={status === "Free" ? "green" : status === "Stressed" ? "orange" : "red"}
                            value={status}
                            className={`py-0.5 px-2 text-[0.8rem] ${getTypography()}  w-fit`}
                          />
                        </td>

                        {/* Move Agent to this Queue in case of not free usage */}
                          <td key="Move Agent" className="border-t border-blue-gray-50">
                            <Menu allowHover>
                            <MenuHandler>
                              <Chip value="Move Agent" variant="gradient" color={status === "Free" ? "green" : status === "Stressed" ? "orange" : "red"} className=" text-[0.8rem] w-fit"/>
                            </MenuHandler>
                            <MenuList className="w-20">
                              {agents.map(({ name, queueList, agentID }) => getOptions(name, agentID, queueList, queueID, routingProfiles))}
                            </MenuList>
                            </Menu>
                          </td>
                      </tr>

                      {/* Open More Info */}
                      { !desc_queue[name] ? null :
                      <>
                      <tr key={name + "desc"} className="border-b border-blue-gray-50">
                        {/* Description */}
                        <td key="Description" colSpan="6" className={getBgColor("gray") + " py-3 px-5"}>
                          <Typography className={`text-[0.8rem] center ${getTypography()} ${getTextColor('black')}`}>
                            {description}
                          </Typography>
                        </td>
                      </tr>
                      {/* Routing Profiles Associated with this Queue */}
                      <tr key={name + "routingProfiles"} className="border-b border-blue-gray-50">
                        <td key="Routing Profiles" colSpan="1" className={getBgColor("gray") + " py-3 px-5 " + getTextColor('black')}>
                          <Typography className={`text-[1rem] center ${getTypography()} ${getTextColor('black')}`}>
                            {routingProfiles.length} routing profile{routingProfiles.length != 1 ? "s" : ""}:
                          </Typography>
                        </td>
                        { routingProfiles.map((routingProfile) =>
                          <td key={routingProfile} colSpan="1" className={getBgColor("gray") + " py-3 px-5 " + getTextColor('black')}>
                            <Typography className={`text-[0.8rem] center ${getTypography()} ${getTextColor('black')}`}>
                            {routingProfile}
                            </Typography>
                          </td>)}
                        <td key="Padding" colSpan="6" className={getBgColor("gray")}></td>
                      </tr>
                      </>
                      }
                    </>
                  );
                }
              )}
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
                        <p className={`text-[0.8rem] ${getTextColor("gray")}`}>
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

    {/*<!-- Graphs -->*/}
      <div className="mb-12 grid gap-y-10 gap-x-6 md:grid-cols-2">
        {!isLoaded ? (
        <div className="py-3 px-5 border-b border-blue-gray-50 text-center col-span-full">
        <span className="flex justify-center items-center">
        <span className={`animate-spin rounded-full h-32 w-32 border-t-2 border-b-2 ${getBorderColor(navColor)}`}></span>
        </span>
        <Typography className={`text-base ${getTypography()}  ${getTextColor('dark')}`}>
            Graphs are now loading...
        </Typography>
        </div>
        ) : (
        graphs.map((props) => (
            <StatisticsChart
                key={props.title}
                {...props}
                footer={
                <Typography className={`flex items-center text-base ${getTypography()}  ${getTextColor('dark')}`}>
                    <ClockIcon strokeWidth={2} className={`h-4 w-4 text-blue-gray-400`} />
                    &nbsp;{props.footer}
                </Typography>
                }
            />
            ))
        )}
      </div>

    </div>
  );
}

export default Queues;
