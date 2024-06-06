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
  Select,
  Option
} from "@material-tailwind/react";
import { AgentList, QueueList, agentQueue } from "@/data";
import { getBgColor, getTextColor, getBorderColor, useMaterialTailwindController, getTypography,getTypographybold } from "@/context";

import React, { useEffect, useState } from 'react';
import { useAlert } from "@/context/alerts";

// Pagination imports
import { parsePaginationString } from "@/configs/api-tools";
import { UsersIcon, CogIcon, CheckCircleIcon, ExclamationCircleIcon, ChevronLeftIcon, ChevronRightIcon } from "@heroicons/react/24/solid";


export function Queues() {
  const [controller, dispatch] = useMaterialTailwindController();
  const { navColor } = controller;

  const [dataToDisplay, setData] = useState([]);
  const [isLoaded, setIsLoaded] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');

  const [desc_queue, setDesc_queue] = useState({});

  // pagination vars
  const [pagination_currentPage, pagination_setCurrentPage] = useState(0);
  const [pagination_totalPages, pagination_setTotalPages] = useState(0);
  const [pagination_itemsPerPage, pagination_setItemsPerPage] = useState(0);
  const [pagination_totalItems, pagination_setTotalItems] = useState(0);

  const { showAlertWithMessage } = useAlert();

  function moveAgentToRoutingProfile(queueName) {
    showAlertWithMessage("yellow", "Moved agent to routing profile: " + queueName, 5000);

/*     if (result.status == 200)
      showAlertWithMessage("green", "Barging in to call with agent", 5000);
    else
      showAlertWithMessage("red", "Failed to barge in to call with agent", 5000); */
  }

  function showDesc(queueName) {
    // Set the description to true for the queue that was clicked

    setDesc_queue({ ...desc_queue, [queueName]: !desc_queue[queueName] });
  }

  function updateData(page = 1) {
    let query = searchQuery ? "name=" + searchQuery : null;
    let skip = (page - 1) * 10;

    setIsLoaded(false);

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
}, []);

  return (
    <div className="mt-12 mb-8 flex flex-col gap-12">
      <Card className={`w-full ${getBgColor("background-cards")}`}>
        <CardHeader variant="gradient" color="gray" className={`mb-8 p-6 ${getTypography()} ${getBgColor("search-bar")}`}>
          <Typography variant="h6" className={`text-[1.45rem] ${getTextColor("white3")} ${getTypographybold()}`}>
            Agent Queues
          </Typography>
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
                          <span className={"animate-spin rounded-full h-32 w-32 border-t-2 border-b-2" + getBorderColor(navColor)}></span>
                      </span>
                  </td>
                </tr> 
                : dataToDisplay.map(
                ({ name, description, usage, averageWaitTime, maxContacts }, key) => {
                  const className = `py-3 px-5 ${key === dataToDisplay.length
                      ? ""
                      : "border-t border-blue-gray-50"
                    }`;

                  return (
                    <>
                      <tr key={name} onClick={() => showDesc(name)} >
                        {/* Name */}
                        <td className={className}>
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
                        <td className={className}>
                          <Typography className={`text-[0.7rem] ${getTypography()} ${getTextColor('black')}`}>
                            {usage}
                          </Typography>
                          {/*<Typography className="text-xs font-normal text-blue-gray-500">
                              {ongoingCalls[1]}
                            </Typography>*/}
                        </td>

                        {/* Average Wait Time */}
                        <td className={className}>
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
                        <td className={className}>
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
                              color={usage / maxContacts * 100 <= 50 ? "green" : usage / maxContacts * 100 > 50 && usage / maxContacts * 100 <= 80 ? "orange" : "red"}
                              className="h-1"
                            />
                          </div>
                        </td>

                        {/* Status */}
                        <td className={className}>
                          <Chip
                            variant="gradient"
                            color={usage / maxContacts * 100 <= 80 ? "green" : usage / maxContacts * 100 > 80 && usage / maxContacts * 100 <= 100 ? "orange" : "red"}
                            value={usage / maxContacts * 100 <= 80 ? "Free" : usage / maxContacts * 100 > 80 && usage / maxContacts * 100 <= 100 ? "Stressed" : "Exceeded"}
                            className={`py-0.5 px-2 text-[8px] ${getTypography()}  w-fit`}
                          />
                        </td>

                        {/* Move Agent to this Queue in case of not free usage */}
                        { usage / maxContacts * 100 < 80 ? null :
                          <td className="w-20" >
                            <Select label="Move Agent" className="w-full">
                              data
                              <option value="Option 1">{getAgentList(name)}</option>
                            </Select>
                          </td>
                        }

                      </tr>
                      { !desc_queue[name] ? null :

                      <tr key={name + "desc"} className="border-b border-blue-gray-50">
                        <td colSpan="10" className="py-3 px-5">
                          <Typography
                            className={`text-[0.8rem] center ${getTypography()} ${getTextColor('black')}`}
                          >
                            {description}
                          </Typography>
                        </td>
                      </tr>
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
  );
}

export default Queues;
