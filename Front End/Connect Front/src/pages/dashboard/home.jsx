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
import { CheckCircleIcon, ClockIcon, ArrowUpIcon, BookOpenIcon, UserGroupIcon, FaceSmileIcon} from "@heroicons/react/24/solid";
import {NotificationsCard} from "../dashboard/notifications.jsx";
import { getBgColor, getTextColor, getBorderColor, useMaterialTailwindController, getTypography,getTypographybold } from "@/context";

import React, { useState, useEffect } from 'react';
import { SupervisorHomeData } from "@/data/supervisor-home-data";

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

  let agent_id = localStorage.getItem("userID");

  function updateData() {

    SupervisorHomeData().then((data) => {
      setCards(data.cards);
      setGraphs(data.graphs);
      setIsLoaded(true);
      //console.log(data);
    });
  }

  //Call the function to recieve data just once
  useEffect(() => {
    updateData();
  }, []);

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

      <div className="mb-6 grid grid-cols-1 gap-y-12 gap-x-6 md:grid-cols-2 xl:grid-cols-3">
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


      {/*Aqui es sobre el sistema de alerta del home page */}
       <div className="mb-4 grid grid-cols-1 gap-6 xl:grid-cols-3">
        <NotificationsCard is_supervisor={true} agent_id={agent_id}/>

        {/* Aquí esta para cambiar el Card de recomendaciones*/}
        <Card className={`border border-blue-gray-100 shadow-sm ${getBgColor("background-cards")}`}>
          <CardHeader
            floated={false}
            shadow={false}
            color="transparent"
            className="m-0 p-6"
          >
             <Typography variant="h6" color="blue-gray" className={`text-xl ${getTypographybold()} ${getTextColor("white3")} text-[1.5rem] pb-1`}>
              Recommendations
            </Typography>
            <Typography
              //variant="small"
              className={`flex items-center gap-1 font-normal text-base ${getTypography()} ${getTextColor("white3")}`}
            >
              Next, a list of recommendations for you:
            </Typography>
          </CardHeader>
          <CardBody className="pt-0">
            <RecomendationCard 
              title={<h2>Check Metrics</h2>} 
              content={<p>Check the client information and metrics.</p>}
              id={1}
              openID={open}
              openhandler={() => handleOpen(1)}/>
      <RecomendationCard 
              title={<h2>De-escalate the call</h2>} 
              content={<p>Try to calm the client and understand his situation.</p>}
              id={2}
              openID={open}
              openhandler={() => handleOpen(2)}/>
      <RecomendationCard 
              title={<h2>Average time response</h2>} 
              content={<p>Try to pay attention to incoming calls, time is valuable for our clients.</p>}
              id={3}
              openID={open}
              openhandler={() => handleOpen(3)}/>
          </CardBody>
        </Card>
      </div> 
    </div>
  );
}

export default Home;
