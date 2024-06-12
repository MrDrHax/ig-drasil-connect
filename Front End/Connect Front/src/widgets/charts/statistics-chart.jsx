import {
  Card,
  CardHeader,
  CardBody,
  CardFooter,
  Typography,
  tooltip,
} from "@material-tailwind/react";
import PropTypes from "prop-types";
import Chart from "react-apexcharts";
import { 
  getBgColor,
  getTextColor,
  useMaterialTailwindController, 
  getTypography,
} from "@/context";

import { chartsConfig } from "@/configs";
import { propTypesLabelProps } from "@material-tailwind/react/types/components/input";

export function StatisticsChart({ color, chart, title, description, footer }) {

  const controller = useMaterialTailwindController();
  const theme = controller;

  // Fix the bar chart
  if (chart.type === 'bar' && chart.series.length > 1) {
    // Fix the series data to be a single dictionary named data
    let data = chart.series.map((item) => item.data[0])
    chart.series = []
    chart.series[0] = {
      data : data,
      name : title,
    } 
  }

  chart = {
    ...chart,
    options: {
      ...chartsConfig.options,
      ...chart.options,
      xaxis: {
        ...chartsConfig.options.xaxis,
        ...chart.options.xaxis,
        labels: {
          ...chartsConfig.options.xaxis.labels,
          style: {
            colors: "#777777",
          },
        },
      },
    },
  };

  return (
    <Card className={`border border-blue-gray-100 shadow-sm ${getBgColor("background-cards")} ${getTypography()} `}>
      <CardHeader variant="gradient" color={color} floated={false} shadow={false}>
        <Chart {...chart} className={` ${getBgColor("background-cards")} ${getTextColor("dark")}`}/>
      </CardHeader>
      <CardBody className="px-6 pt-0">
        <Typography variant="h6" color="blue-gray" className={`${getTypography()} ${getTextColor("dark")}`}>
          {title}
        </Typography>
        <Typography variant="small" className={`${getTypography()} ${getTextColor("dark")}`}>
          {description}
        </Typography>
      </CardBody>
      {footer && (
        <CardFooter className={`${getTypography()}  border-t border-blue-gray-50 px-6 py-5`}>
          {footer}
        </CardFooter>
      )}
    </Card>
  );
}

StatisticsChart.defaultProps = {
  color: "blue",
  footer: null,
};

StatisticsChart.propTypes = {
  color: PropTypes.oneOf([
    "white",
    "blue-gray",
    "gray",
    "brown",
    "deep-orange",
    "orange",
    "amber",
    "yellow",
    "lime",
    "light-green",
    "green",
    "teal",
    "cyan",
    "light-blue",
    "blue",
    "indigo",
    "deep-purple",
    "purple",
    "pink",
    "red",
  ]),
  chart: PropTypes.object.isRequired,
  title: PropTypes.node.isRequired,
  description: PropTypes.node.isRequired,
  footer: PropTypes.node,
};

StatisticsChart.displayName = "/src/widgets/charts/statistics-chart.jsx";

export default StatisticsChart;
