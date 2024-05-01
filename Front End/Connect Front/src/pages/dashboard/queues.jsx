import {
    Card,
    CardHeader,
    CardBody,
    Typography,
    Avatar,
    Chip,
    Tooltip,
    Progress,
    
  } from "@material-tailwind/react";
  import { EllipsisVerticalIcon } from "@heroicons/react/24/outline";
  import { agentQueue, projectsTableData } from "@/data";

  import { getBgColor, getTextColor, useMaterialTailwindController } from "@/context";

  
  export function Queues() {
    const controller = useMaterialTailwindController();

    return (
      <div className="mt-12 mb-8 flex flex-col gap-12">
        <Card className={`w-full ${getBgColor("background-cards")}`}>
          <CardHeader variant="gradient" color="gray" className={`mb-8 p-6 ${getBgColor("search-bar")}`}>
            <Typography variant="h6" color="white">
              Agent Queue
            </Typography>
          </CardHeader>
          <CardBody className={`overflow-x-scroll px-0 pt-0 pb-2 ${getBgColor("background-cards")}`}>
            <table className="w-full min-w-[640px] table-auto">
              <thead>
                <tr>
                  {["Name", "Ongoing Calls", "Avg Response Time", "Usage", "Status"].map((el) => (
                    <th
                      key={el}
                      className="border-b border-blue-gray-50 py-3 px-5 text-left"
                    >
                      <Typography
                        variant="small"
                        className={`text-[11px] font-bold uppercase ${getTextColor('black')}`}
                      >
                        {el}
                      </Typography>
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {agentQueue.map(
                  ({  name,  ongoingCalls, avg, online, usage }, key) => {
                    const className = `py-3 px-5 ${
                      key === agentQueue.length - 1
                        ? ""
                        : "border-b border-blue-gray-50"
                    }`;
  
                    return (
                      <tr key={name}>
                        <td className={className}>
                          <div className="flex items-center gap-4">
                            
                            <div>
                              <Typography
                                variant="small"
                                color="blue-gray"
                                className={`font-semibold ${getTextColor('black')}`}
                              >
                                {name}
                              </Typography>
                             
                            </div>
                          </div>
                        </td>
                        <td className={className}>
                          <Typography className={`text-xs font-semibold ${getTextColor('black')}`}>
                            {ongoingCalls}
                          </Typography>
                           {/*<Typography className="text-xs font-normal text-blue-gray-500">
                            {ongoingCalls[1]}
                           </Typography>*/}
                        </td>
                        <td className={className}>
                          <Typography
                            className={`text-xs font-semibold ${
                              avg <= 1 ? "text-green-600" : avg <= 2.30 ? "text-orange-600" : "text-red-600"
                            }`}
                          >
                            {avg}
                          </Typography>
                         
                           {/*<Typography className="text-xs font-normal text-blue-gray-500">
                            {ongoingCalls[1]}
                           </Typography>*/}
                        </td>
                        
                        
                        <td className={className}>
                          <div className="w-10/12">
                            <Typography
                              variant="small"
                              className={`mb-1 block text-xs font-medium ${getTextColor('black')}`} 
                            >
                              {usage}%
                            </Typography>
                            <Progress
                              value={usage}
                              variant="gradient"
                              color={usage <= 50 ? "green" : usage > 50 && usage <= 80 ? "orange" : "red"}
                              className="h-1"
                            />
                          </div>
                        </td>
                        <td className={className}>
                          <Chip
                            variant="gradient"
                            color={usage <= 80 ? "green" : usage > 80 && usage <= 100 ? "orange" : "red"}
                            value={usage <= 80 ? "Free" : usage > 80 && usage <= 100 ? "Stressed" : "Exceeded"}
                            className="py-0.5 px-2 text-[11px] font-medium w-fit"
                          />
                        </td>
                        
                      </tr>
                    );
                  }
                )}
              </tbody>
            </table>
          </CardBody>
        </Card>
        
        {/* Projects Table 
        <Card>
          <CardHeader variant="gradient" color="gray" className="mb-8 p-6">
            <Typography variant="h6" color="white">
              Projects Table
            </Typography>
          </CardHeader>
          <CardBody className="overflow-x-scroll px-0 pt-0 pb-2">
            <table className="w-full min-w-[640px] table-auto">
              <thead>
                <tr>
                  {["companies", "members", "budget", "completion", ""].map(
                    (el) => (
                      <th
                        key={el}
                        className="border-b border-blue-gray-50 py-3 px-5 text-left"
                      >
                        <Typography
                          variant="small"
                          className="text-[11px] font-bold uppercase text-blue-gray-400"
                        >
                          {el}
                        </Typography>
                      </th>
                    )
                  )}
                </tr>
              </thead>
              <tbody>
                {projectsTableData.map(
                  ({ img, name, members, budget, completion }, key) => {
                    const className = `py-3 px-5 ${
                      key === projectsTableData.length - 1
                        ? ""
                        : "border-b border-blue-gray-50"
                    }`;
  
                    return (
                      <tr key={name}>
                        <td className={className}>
                          <div className="flex items-center gap-4">
                            <Avatar src={img} alt={name} size="sm" />
                            <Typography
                              variant="small"
                              color="blue-gray"
                              className="font-bold"
                            >
                              {name}
                            </Typography>
                          </div>
                        </td>
                        <td className={className}>
                          {members.map(({ img, name }, key) => (
                            <Tooltip key={name} content={name}>
                              <Avatar
                                src={img}
                                alt={name}
                                size="xs"
                                variant="circular"
                                className={`cursor-pointer border-2 border-white ${
                                  key === 0 ? "" : "-ml-2.5"
                                }`}
                              />
                            </Tooltip>
                          ))}
                        </td>
                        <td className={className}>
                          <Typography
                            variant="small"
                            className="text-xs font-medium text-blue-gray-600"
                          >
                            {budget}
                          </Typography>
                        </td>
                        <td className={className}>
                          <div className="w-10/12">
                            <Typography
                              variant="small"
                              className="mb-1 block text-xs font-medium text-blue-gray-600"
                            >
                              {completion}%
                            </Typography>
                            <Progress
                              value={completion}
                              variant="gradient"
                              color={completion === 100 ? "green" : "gray"}
                              className="h-1"
                            />
                          </div>
                        </td>
                        <td className={className}>
                          <Typography
                            as="a"
                            href="#"
                            className="text-xs font-semibold text-blue-gray-600"
                          >
                            <EllipsisVerticalIcon
                              strokeWidth={2}
                              className="h-5 w-5 text-inherit"
                            />
                          </Typography>
                        </td>
                      </tr>
                    );
                  }
                )}
              </tbody>
            </table>
          </CardBody>
        </Card>
        */}
      </div>
    );
  }
  
  export default Queues;
  