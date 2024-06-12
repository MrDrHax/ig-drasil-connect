import {
  Typography,
  Card,
  CardHeader,
  CardBody,
  IconButton,
  Menu,
  MenuHandler,
  MenuList,
  MenuItem
} from "@material-tailwind/react";
import { StatisticsCard } from "@/widgets/cards";
import { StatisticsChart } from "@/widgets/charts";
import { RecomendationCard } from "@/widgets/cards";
import { CheckCircleIcon, ClockIcon, ArrowUpIcon, BookOpenIcon, UserGroupIcon, FaceSmileIcon, ScissorsIcon, PhoneArrowDownLeftIcon, PhoneXMarkIcon} from "@heroicons/react/24/solid";
import {NotificationsCard} from "../dashboard/notifications.jsx";
import { getBgColor, getTextColor, getBorderColor, useMaterialTailwindController, getTypography,getTypographybold } from "@/context";

import React, { useState, useEffect } from 'react';
import { SupervisorHomeData } from "@/data/supervisor-home-data";
import { AgentId } from "@/data";

export function getIcon(icon) {
  switch (icon) {
    case "Arrow":
      return ArrowUpIcon;
    case "Book":
      return BookOpenIcon;
    case "Clock":
      return ClockIcon;
    case "Person":
      return UserGroupIcon;
    case "Face":
      return FaceSmileIcon;
    case "Scissors":
      return ScissorsIcon;
    case "Phone":
      return PhoneXMarkIcon;
    case "PhoneArrow":
      return PhoneArrowDownLeftIcon;
    default:
      return CheckCircleIcon;
  }
}

export function Home() {
  const [open, setOpen] = React.useState(1);
 
  const handleOpen = (value) => setOpen(open === value ? 0 : value);

  const [controller, dispatch] = useMaterialTailwindController();
  const { navColor} = controller;

  const [cards, setCards] = useState([]);
  const [graphs, setGraphs] = useState([]);
  const [isLoaded, setIsLoaded] = useState(false);

  const [agent_id, setAgent_id] = useState("");


  function updateData() {

    SupervisorHomeData().then((data) => {
      setCards(data.cards);
      setGraphs(data.graphs);
      setIsLoaded(true);
    }).catch((error) => {
      setIsLoaded(true);
    });
  }

  useEffect(() => {
    AgentId().then((data) => {
      setAgent_id(data);
    });
  }, []);

  //Call the function to recieve data once the agent_id is set
  useEffect(() => {
    updateData();
  }, [agent_id]);

  return (
    <div className="mt-4">
      <div className="mb-6 grid grid-cols-1 gap-y-12 gap-x-6 md:grid-cols-2 xl:grid-cols-3">
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

      <div className="mb-6 grid grid-cols-1 gap-y-12 gap-x-6 md:grid-cols-2 xl:grid-cols-2">
        {!isLoaded ? (
          <div className="py-3 px-5 border-b border-blue-gray-50 text-center col-span-full">
            <span className="flex justify-center items-center">
            <span className={`animate-spin rounded-full h-32 w-32 border-t-2 border-b-2 ${getBorderColor(navColor)}`}></span>
            </span>
            <Typography className={`text-base ${getTypography()} ${getTextColor('dark')}`}>
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


      {/* Notifications */}
       <div id="notifications" className="mb-4 grid grid-cols-1 gap-6 xl:grid-cols-1">
        <NotificationsCard is_supervisor={true} agent_id={agent_id}/>

      </div> 
    </div>
  );
}

export default Home;
