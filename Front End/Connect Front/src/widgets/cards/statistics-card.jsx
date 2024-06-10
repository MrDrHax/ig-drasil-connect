import {
  Card,
  CardHeader,
  CardBody,
  CardFooter,
  Typography,
  Rating
} from "@material-tailwind/react";
import PropTypes from "prop-types";
import { 
  getBgColor,
  getTextColor,
  useMaterialTailwindController,
  getTypography,
} from "@/context";

export function StatisticsCard({ color, icon, title, value, footer }) {

  const controller = useMaterialTailwindController();
  const theme = controller;

  return (
    <Card className={`border border-blue-gray-100 shadow-sm ${getBgColor("background-cards")}`} >
      <CardHeader
        variant="gradient"
        color={color}
        floated={false}
        shadow={false}
        className="absolute grid h-12 w-12 place-items-center mr-[1rem]"
      >
        {icon}
      </CardHeader>
      <CardBody className="p-4 text-right">
      <Typography className={`text-[1rem] ml-10 ${getTypography()} ${getTextColor("dark")}`}>
          {title}
        </Typography>
         <Typography className={`text-[1.5rem] ml-20 ${getTypography()} ${getTextColor("dark")}`}>
          {value}
        </Typography>
      </CardBody>
      {footer && (
        <CardFooter className={`${getTypography()} border-t border-blue-gray-50 p-4`}>
          {footer}
        </CardFooter>
      )}
    </Card>
  );
}

StatisticsCard.defaultProps = {
  color: "blue",
  footer: null,
};

StatisticsCard.propTypes = {
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
  icon: PropTypes.node.isRequired,
  title: PropTypes.node.isRequired,
  value: PropTypes.node.isRequired,
  footer: PropTypes.node,
};

StatisticsCard.displayName = "/src/widgets/cards/statistics-card.jsx";

export default StatisticsCard;
