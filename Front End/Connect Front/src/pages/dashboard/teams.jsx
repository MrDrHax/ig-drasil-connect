import {
  Card,
  CardHeader,
  CardBody,
  Typography,
  Input,
  Chip,
  Button,
  Checkbox,
  Select,
  Option
} from "@material-tailwind/react";
// import { EllipsisVerticalIcon } from "@heroicons/react/24/outline";
// import { authorsTableData, projectsTableData } from "@/data";
import { AgentList, JoinCall, ChangeStatus, StatusList, AgentCards } from "@/data/agents-data";
import { StatisticsCard } from "@/widgets/cards";
import { StatisticsChart } from "@/widgets/charts";
import { UsersIcon, CogIcon, ClockIcon, CheckCircleIcon, ExclamationCircleIcon, ChevronLeftIcon, ChevronRightIcon, ArrowPathIcon } from "@heroicons/react/24/solid";
import { parsePaginationString } from "@/configs/api-tools";
import React, { useEffect, useState } from 'react';
import { Link } from "react-router-dom";
import { getBgColor, getBorderColor, getTextColor, useMaterialTailwindController, getTypography, getTypographybold } from "@/context";
import { getIcon } from "@/pages/dashboard/home";
import { useAlert } from "@/context/alerts";

function getColorOfStatus(status) {
  switch (status) {
    // Statuses while not in a call
    case "Available":
      return "green";
    case "Training":
      return "blue";
    case "On break":
      return "purple";
    case "Busy":
      return "orange";
    case "Needs Assistance":
      return "red";
    case "Offline":
      return "gray";
    // Statuses while in a call are shown as pink
    default:
      return "pink";
  }
}


export function Teams() {
  const [controller, dispatch] = useMaterialTailwindController();
  const { navColor } = controller;

  const [dataToDisplay, setData] = useState([]);
  const [cards, setCards] = useState([]);
  const [graphs, setGraphs] = useState([]);
  const [status_list, setStatusList] = useState([]);

  const [isLoaded, setIsLoaded] = useState(false);
  const [isCardLoaded, setIsCardLoaded] = useState(false);
  const [isTimeoutScheduled, setIsTimeoutScheduled] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [searchQuery_status, setSearchQuery_status] = useState('');
  const [helpFilter, setHelpFilter] = useState(false);

  const [changed, setChanged] = useState(false);

  // pagination vars
  const [pagination_currentPage, pagination_setCurrentPage] = useState(0);
  const [pagination_totalPages, pagination_setTotalPages] = useState(0);
  const [pagination_itemsPerPage, pagination_setItemsPerPage] = useState(0);
  const [pagination_totalItems, pagination_setTotalItems] = useState(0);

  function handleSearch(event) {
    setSearchQuery(event.target.value.toLowerCase());
  }

  function handleSearchStatus(event) {
    setSearchQuery_status(event.target.value.toLowerCase());
  }

  function handleHelpFilter(event) {
    setHelpFilter(event.target.checked);
  }

  const { showAlertWithMessage } = useAlert();

  /**
   * A function to change the status of an agent.
   *
   * @param {type} agentId - The ID of the agent to change the status of.
   * @param {type} status - The new status of the agent.
   * @return {type} No return value.
   */
  function handleChangeStatus(agentId, status, current) {
    if (current == status)
      return;

    ChangeStatus(agentId, status).then(result => {
      setChanged(!changed);
      if (result && result.message == "Status changed")
        showAlertWithMessage("green", "Status changed. It might take a few seconds to reflect changes.", 5000);
      else
        showAlertWithMessage("red", "Failed to change status", 5000);
    });

    updateData();
  }

  /**
   * A function to barge into a call with a specified agent ID.
   *
   * @param {type} agentId - The ID of the agent to barge in on.
   * @return {type} No return value.
   */
  function bargeIn(agentId) {
    let result = JoinCall(agentId);

    setChanged(!changed);
    if (result.status == 200)
      showAlertWithMessage("green", "Barging in to call with agent", 5000);
    else
      showAlertWithMessage("red", "Failed to barge in to call with agent", 5000);
    //console.log("Barging in to call with agent " + agentId);
  }

  /**
   * Updates the data on the page based on the provided page number.
   *
   * @param {number} [page=1] - The page number to fetch data for. Defaults to 1.
   * @return {Promise<void>} A promise that resolves when the data has been updated.
   */
  function updateData(page = 1, background = false) {
    // search by name
    let search = searchQuery ? `name=${searchQuery}` : '';

    // search by status
    if (searchQuery_status) {
      search += search ? `,status=${searchQuery_status}` : `status=${searchQuery_status}`;
    }
    if (helpFilter) {
      search += search ? `,requireHelp=false` : `requireHelp=true`;
    }
    let skip = (page - 1) * 10;

    if (!background)
      setIsLoaded(false);

    // get statuses
    StatusList().then((data) => {
      let statuses = [];
      for (let i = 0; i < data.length; i++) {
        statuses.push(data[i].Name);
      }
      statuses.sort();
      setStatusList(statuses);
    }).catch((error) => {
      // showAlertWithMessage("red", "Could not load possible status", 10000);
      console.error(error);
    });

    // get agents
    AgentList(skip, 10, search, "name", "asc").then((data) => {
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

    if (background) {
      setIsTimeoutScheduled(false);
    }

    if (!isTimeoutScheduled) // run task every 5 seconds only if not already scheduled
    {
      setIsTimeoutScheduled(true);
      setTimeout(() => {
        updateData(page, true);
      }, 5000);
    }
  }

  function updateSecondary() {
    // get cards
    AgentCards().then((data) => {
      setCards(data.cards);
      setGraphs(data.graphs);
    }).catch((error) => {
      showAlertWithMessage("red", "Could not load cards", 10000);
      console.error(error);
    });

    setIsCardLoaded(true);

    // update cards every 30 seconds

    setTimeout(() => {
      updateSecondary();
    }, 30000);
  }

  useEffect(() => {
    updateData();
  }, [searchQuery, searchQuery_status, helpFilter, changed]);

  useEffect(() => {
    updateSecondary();
  }, []);

  return (
    <div>
      {/*<!-- Cards -->*/}
      <div className="mb-12 grid gap-y-10 gap-x-6 md:grid-cols-2 xl:grid-cols-4">
        {!isCardLoaded ? (
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

      {/*<!-- Table -->*/}
      <div className="mt-12 mb-8 flex flex-col gap-12">
        <Card className={`${getTypography()} ${getBgColor("background-cards")}`}>
          <CardHeader variant="gradient" color="gray" className={`mb-8 p-6 flex ${getBgColor("search-bar")}`}>
            <Typography variant="h6" color="white" className={`text-[1.54rem] flex-none ${getTypography()}`}>
              Agents
            </Typography>

            <div className="flex-grow"></div>

            <div className="mr-auto md:mr-4 md:w-56">
              {/* Search bar by name*/}
              <Input
                color="white"
                label="Search by name"
                value={searchQuery}
                onChange={handleSearch}
              />
            </div>

            <div className="mr-auto md:mr-4 md:w-56">
              {/* Search bar by status*/}
              <Input
                color="white"
                label="Search by status"
                value={searchQuery_status}
                onChange={handleSearchStatus}
              />
            </div>
            <div className="mr-auto md:mr-4 md:w-56 flex items-center space-x-2">
              {/* Needs help filter*/}
              <Checkbox
                color="white"
                label="Needs Help"
                labelProps={{ className: "text-white" }}
                checked={helpFilter}
                onChange={handleHelpFilter}
              />
              {/* Update agents list button*/}
              <Button onClick={() => updateData()} className="ml-2" color="gray" variant="gradient">
                <ArrowPathIcon className="h-5 w-5" />
              </Button>
            </div>
          </CardHeader>
          <CardBody className={`overflow-x-scroll px-0 pt-0 pb-2 ${getBgColor("background-cards")}`}>
            {/* List */}
            <table className="w-full min-w-[640px] table-auto">
              <thead>
                <tr>
                  {["name", "Routing Profile", "", "needs help", ""].map((el, i) => (
                    <th
                      key={i}
                      className="border-b border-blue-gray-50 py-3 px-5 text-left"
                    >
                      <Typography
                        variant="small"
                        className={`text-[0.6rem] font-bold uppercase ${getTypography()} ${getTextColor('dark')}`}
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
                          <span className={`animate-spin rounded-full h-32 w-32 border-t-2 border-b-2 ${getBorderColor(navColor)}`}></span>
                        </span>
                        <Typography className={`text-base ${getTypography()}  ${getTextColor('dark')}`}>
                          Agents are now loading...
                        </Typography>
                      </td>
                    </tr>
                  ) : (
                    dataToDisplay.length === 0 ? (
                      <tr key="empty">
                        <td className="py-3 px-5 border-b border-blue-gray-50 text-center" colSpan="5">
                          <Typography
                            variant="small"
                            className={`text-[0.8em] ${getTypographybold()} ${getTextColor('dark')}`}
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
                              {/* Name indicator*/}
                              <td className={className}>
                                <div className="flex items-center gap-4">
                                  {/* <Avatar src={avatar} alt={name} size="sm" variant="rounded" /> */}
                                  <div>
                                    <Typography
                                      variant="small"
                                      className={`text-[0.7rem]${getTypographybold()} ${getTextColor('dark')}`}
                                    >
                                      {name}
                                    </Typography>
                                  </div>
                                </div>
                              </td>
                              {/* Queue indicator*/}
                              <td className={className}>
                                <Typography className={`text-xs ${getTypographybold()} ${getTextColor('dark')}`}>
                                  {queue}
                                </Typography>
                              </td>
                              {/* Status indicator*/}
                              <td className={className}>
                                {/*
                                <Chip
                                    variant="gradient"
                                    color={getColorOfStatus(status)}
                                    value={status}
                                    className={`py-0.5 px-2 text-[0.8rem] font-medium w-fit ${getTypographybold()}`}
                                />
                                */}
                                {/* <Select value={status}
                                  className={`text-[0.8rem] ${getTypographybold()} ${status === "Offline" ? getTextColor('dark') : getTextColor('white2')} ${getBgColor(getColorOfStatus(status))}`}
                                  color={getColorOfStatus(status)}
                                  onChange={(val) => handleChangeStatus(agentID, val, status)}>
                                  <Option key={status} value={status}>{status}</Option>
                                  {status_list.map((status_option) => status_option == status ? <></> : <Option key={status_option} value={status_option}>{status_option}</Option>)}
                                </Select> */}

                                <form class="max-w-sm mx-auto w-fit">
                                  <label for="status_select" class="sr-only">Status</label>
                                  <select
                                    id="status_select"
                                    onChange={(val) => handleChangeStatus(agentID, val.target.value, status)}
                                    class={`block rounded-full py-2.5 px-5 w-full text-center text-sm border-0 border-b-2 border-gray-200 appearance-none ${getTypographybold()} ${status === " Offline" ? getTextColor('dark') : getTextColor('white2')} ${getBgColor(getColorOfStatus(status))} focus:outline-none focus:ring-0 focus:border-gray-200 peer`}
                                  >
                                    <option key={status} value={status} selected>{status.toUpperCase()}</option>
                                    <optgroup label="Change to">
                                      {status_list.map((status_option) => status_option == status ? <></> : <option key={status_option} value={status_option}>{status_option.toUpperCase()}</option>)}
                                    </optgroup>
                                  </select>
                                </form>

                              </td>
                              {/* Needs help indicator*/}
                              <td className={className}>
                                {requireHelp ? <ExclamationCircleIcon className="h-6 w-6 text-red-500" /> : getColorOfStatus(status) == 'pink' ? <ExclamationCircleIcon className="h-6 w-6 text-pink-300" /> : <CheckCircleIcon className="h-6 w-6 text-green-500" />}
                              </td>
                              {/* View Agent Profile */}
                              <td className={className}>
                                <Link to={"/dashboard/profile?profile=" + agentID} className={`text-xs font-semibold ${getTextColor('dark')}`}>
                                  View
                                </Link>
                              </td>
                              {/* Barge-In If needed*/}
                              {requireHelp || getColorOfStatus(status) == 'pink' ?
                                <td className={className}>
                                  <Button onClick={() => bargeIn(agentID)}
                                    variant="gradient" color="red" className="py-0.5 px-2 text-[11px] font-medium w-fit">
                                    Monitor Call
                                  </Button>
                                </td> : null
                              }
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
      {/*<!-- Graphs -->*/}
      <div className="mb-12 grid gap-y-10 gap-x-6 md:grid-cols-2">
        {!isCardLoaded ? (
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

export default Teams;
