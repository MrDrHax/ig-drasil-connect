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
// import { EllipsisVerticalIcon } from "@heroicons/react/24/outline";
// import { authorsTableData, projectsTableData } from "@/data";
import { AgentList, AgentsSummary } from "@/data/agents-data";
import { StatisticsCard } from "@/widgets/cards";
import { StatisticsChart } from "@/widgets/charts";
import { UsersIcon, CogIcon } from "@heroicons/react/24/solid";
import { chartsConfig } from "@/configs";


function getColorOfStatus(status) {
    switch (status) {
        case "connected":
            return "green";
        case "disconected":
            return "red";
        case "on-call":
            return "orange";
    }
}

export function Teams() {
    var data = AgentList();
    var summaryData = AgentsSummary();

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
                    icon={<UsersIcon class="h-6 w-6 text-white-500" />}
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
                    icon={<CogIcon class="h-6 w-6 text-white-500" />}
                    footer={
                        <Typography className="font-normal text-blue-gray-600">
                            <strong className="text-green-500">3/5</strong>
                            &nbsp; agents on call
                        </Typography>
                    }
                />
                {/* <StatisticsChart
                    key="Usage"
                    title="Usage"
                    description="TODO: add description"
                    type="pie"
                    height={220}
                    color="gray"
                    series={[
                        {
                            name: "Views",
                            data: [50, 20, 10, 22, 50, 10, 40],
                        },
                    ]}
                    options={{
                        ...chartsConfig,
                        colors: "#388e3c",
                        plotOptions: {
                            pie: {
                                columnWidth: "16%",
                                borderRadius: 5,
                            },
                        },
                        xaxis: {
                            ...chartsConfig.xaxis,
                            categories: ["M", "T", "W", "T", "F", "S", "S"],
                        },
                    }}
                    footer={
                        <Typography
                            variant="small"
                            className="flex items-center font-normal text-blue-gray-600"
                        >
                            updated 1 second ago
                        </Typography>
                    }
                /> */}
            </div>
            <div className="mt-12 mb-8 flex flex-col gap-12">
                <Card>
                    <CardHeader variant="gradient" color="gray" className="mb-8 p-6">
                        <Typography variant="h6" color="white">
                            Agents
                        </Typography>

                        <Typography variant="body2" color="white">
                            TODO: add search and filters
                        </Typography>
                    </CardHeader>
                    <CardBody className="overflow-x-scroll px-0 pt-0 pb-2">
                        <table className="w-full min-w-[640px] table-auto">
                            <thead>
                                <tr>
                                    {["author", "queue", "status", ""].map((el) => (
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
                                    ))}
                                </tr>
                            </thead>
                            <tbody>
                                {data.map(
                                    ({ avatar, name, queue, status, id }, key) => {
                                        const className = `py-3 px-5 ${key === data.length - 1
                                            ? ""
                                            : "border-b border-blue-gray-50"
                                            }`;

                                        return (
                                            <tr key={id}>
                                                <td className={className}>
                                                    <div className="flex items-center gap-4">
                                                        <Avatar src={avatar} alt={name} size="sm" variant="rounded" />
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
                                )}
                            </tbody>
                        </table>
                    </CardBody>
                </Card>
            </div>
        </div>
    );
}

export default Teams;
