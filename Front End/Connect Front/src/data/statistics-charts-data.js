import { chartsConfig } from "@/configs";
import { data } from "autoprefixer";

const websiteViewsChart = {
  type: "bar",
  height: 220,
  series: [
    {
      name: "Capacity",
      data: [50, 20, 10, 22, 50],
    },
  ],
  options: {
    ...chartsConfig,
    colors: "#388e3c",
    plotOptions: {
      bar: {
        columnWidth: "16%",
        borderRadius: 5,
      },
    },
    xaxis: {
      ...chartsConfig.xaxis,
      categories: ["Sales", "Delivery", "My Tickets Profile", "Reinbursements", "Transfers" ],
      labels: {
        style: {
          fontSize: "12px",
          colors: "#777777",
        },
      }
    },
  },
};

const dailySalesChart = {
  type: "line",
  height: 220,
  series: [
    {
      name: "Rating",
      data: [60, 40, 50, 70, 60, 70, 80, 90, 80],
    },
    {
      name: "KPIs",
      data: [80, 70, 60, 55, 86, 70, 40, 30, 60],
    },
  ],
  options: {
    ...chartsConfig,
    colors: ["#0288d1", "#ff5722"],
    stroke: {
      lineCap: "round",
      curve: "smooth",
    },
    markers: {
      size: 0,
    },
    xaxis: {
      ...chartsConfig.xaxis,
      categories: [
        "-1h",
        "-50m",
        "-40m",
        "-30m",
        "-20m",
        "-10m",
        "-5m",
        "-2m",
        "NOW",
      ],
    },
  },
};

const averageRatingChart = {
  type: "line",
  height: 220,
  series: [
    {
    name: "Rating",
    data: [3, 5, 5, 4, 5, 3, 4, 3, 5, 5],
    },
  ],
  options: {
    ...chartsConfig,
    colors: ["#ff5722"],
    stroke: {
      lineCap: "round",
    },
    markers: {
      size: 0,
    },
    xaxis: {
      ...chartsConfig.xaxis,
      categories: [
        "Jan",
        "Feb",
        "March",
        "Apr",
        "May",
        "June",
        "July",
        "Aug",
        "Sep",
      ],
    },
  }
}

const completedTaskChart = {
  type: "line",
  height: 220,
  series: [
    {
      name: "Sales",
      data: [50, 40, 300, 320, 500, 350, 200, 230, 500],
    },
  ],
  options: {
    ...chartsConfig,
    colors: ["#a020F0"],
    stroke: {
      lineCap: "round",
    },
    markers: {
      size: 5,
    },
    xaxis: {
      ...chartsConfig.xaxis,
      categories: [
        "-1h",
        "-50m",
        "-40m",
        "-30m",
        "-20m",
        "-10m",
        "-5m",
        "-2m",
        "NOW",
      ],
    },
  },
};
const completedTasksChart = {
  ...completedTaskChart,
  series: [
    {
      name: "Tasks",
      data: [5, 4, 30, 32, 50, 35, 20, 23, 10],
    },
  ],
};

export const statisticsChartsData = [
  {
    color: "white",
    title: "Queues",
    description: "Table showing queue capacity",
    footer: "Updated 2 min ago",
    chart: websiteViewsChart,
  },
  {
    color: "white",
    title: "Average call rating",
    description: "What did clients think about the call? + important KPIs",
    footer: "updated 1 min ago",
    chart: dailySalesChart,
  },
  {
    color: "white",
    title: "Unfinished calls",
    description: "Shows amount of unfinished calls in the last hour",
    footer: "just updated",
    chart: completedTasksChart,
  },
  {
    color: "yellow",
    title: "Average rating over the months",
    description: "The clients rated the agent with the following stars",
    footer: "Updated 2 min ago",
    chart: averageRatingChart,
  }
];

export default statisticsChartsData;
